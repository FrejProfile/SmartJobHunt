import requests
import time
from datetime import datetime
from django.core.management.base import BaseCommand

"""
Script checks databse for jobs that havent been applied to but the application has been removed.
If website is blcoked with a 4xx it prompts the user to either check manual or delete the jobs.
"""


# ── Configuration ─────────────────────────────────────────────────────────────
JOBINDEX_HEALTH_URL = "https://www.jobindex.dk"
REQUEST_DELAY       = 1.0
TIMEOUT             = 10


# ── Helpers ───────────────────────────────────────────────────────────────────
def ping_jobindex(session):
    try:
        r = session.get(JOBINDEX_HEALTH_URL, timeout=TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False


def check_url(session, url):
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 200:
            return "alive", 200
        return "dead", r.status_code
    except requests.exceptions.Timeout:
        return "error", None
    except Exception:
        return "error", None


# ── Main cleanup logic ────────────────────────────────────────────────────────
def run_cleanup(db_jobs, stdout):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    stdout.write("Pinging Jobindex before starting...")
    if not ping_jobindex(session):
        stdout.write("✗ Jobindex unreachable at start. Aborting — nothing touched.")
        return None
    stdout.write("✓ Jobindex alive. Starting checks...\n")

    results = {
        "alive":   [],
        "removed": [],
        "skipped": [],
        "aborted": [],
    }
    aborted = False

    for i, job in enumerate(db_jobs, 1):
        url = job.get("employer_url")
        tag = f"[{i}/{len(db_jobs)}] {job['title'][:38]} ({job['employer'][:18]}) [{job['status']}]"

        if not url:
            stdout.write(f"  ? {tag} — no employer URL, skipping")
            results["skipped"].append(job)
            continue

        status, code = check_url(session, url)

        if status == "alive":
            stdout.write(f"  ✓ {tag} — live (200)")
            results["alive"].append(job)

        elif status == "dead":
            if ping_jobindex(session):
                stdout.write(f"  ✗ {tag} — dead ({code}), ping ok → queued for removal")
                results["removed"].append({**job, "_dead_status": code})
            else:
                stdout.write(f"  ! {tag} — dead ({code}) but ping FAILED → connection lost, aborting")
                results["aborted"].append(job)
                aborted = True
                break

        elif status == "error":
            if ping_jobindex(session):
                stdout.write(f"  ? {tag} — request error, ping ok → skipping (transient)")
                results["skipped"].append(job)
            else:
                stdout.write(f"  ! {tag} — request error + ping FAILED → connection lost, aborting")
                results["aborted"].append(job)
                aborted = True
                break

        time.sleep(REQUEST_DELAY)

    stdout.write(f"""
── Cleanup summary ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ──────────────
  Live:               {len(results['alive'])}
  Queued for removal: {len(results['removed'])}
  Skipped:            {len(results['skipped'])}
  Aborted:            {'yes — nothing deleted' if aborted else 'no'}
""")

    if aborted:
        results["removed"] = []

    return results


# ── Django management command ─────────────────────────────────────────────────
class Command(BaseCommand):
    help = "Check employer URLs for potential/ranked jobs and remove dead listings"

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Check URLs and print dead job IDs as JSON sentinel, without prompting or deleting.',
        )

    def handle(self, *args, **options):
        import json
        from jobs.models import Job

        db_jobs = list(
            Job.objects
            .filter(status__in=["potential", "ranked"])
            .values("id", "title", "employer", "status", "employer_url")
        )

        db_jobs = [
            {
                "job_id":       j["id"],
                "employer_url": j["employer_url"],
                "title":        j["title"],
                "employer":     j["employer"],
                "status":       j["status"],
            }
            for j in db_jobs
        ]

        if not db_jobs:
            self.stdout.write("No potential or ranked jobs to check.")
            if options['check_only']:
                self.stdout.write("__dead_jobs__:[]")
            return

        self.stdout.write(f"Checking {len(db_jobs)} jobs (potential + ranked)...\n")

        result = run_cleanup(db_jobs, self.stdout)
        if result is None or not result.get("removed"):
            self.stdout.write("Nothing to delete.")
            if options['check_only']:
                self.stdout.write("__dead_jobs__:[]")
            return

        # Show the dead jobs with their URLs for manual verification
        self.stdout.write("── Jobs queued for deletion ─────────────────────────────────────")
        for j in result["removed"]:
            self.stdout.write(f"  [{j['_dead_status']}] {j['title']}")
            self.stdout.write(f"         {j['employer']}")
            self.stdout.write(f"         {j['employer_url']}")
        self.stdout.write("")

        if options['check_only']:
            # Emit a machine-readable sentinel so the web UI can confirm before deleting
            dead = [
                {"id": j["job_id"], "title": j["title"], "employer": j["employer"], "url": j["employer_url"]}
                for j in result["removed"]
            ]
            self.stdout.write(f"__dead_jobs__:{json.dumps(dead)}")
            return

        # Ask for confirmation (interactive CLI use)
        confirm = input(f"Delete these {len(result['removed'])} job(s)? [y/N] ").strip().lower()
        if confirm != "y":
            self.stdout.write("Aborted — nothing deleted.")
            return

        job_ids = [j["job_id"] for j in result["removed"]]
        deleted, _ = Job.objects.filter(id__in=job_ids).delete()
        self.stdout.write(f"Deleted {deleted} job(s) from DB.")