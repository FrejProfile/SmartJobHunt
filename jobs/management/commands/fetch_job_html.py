import os
import json
import requests
from django.core.management.base import BaseCommand

POTENTIAL_JOBS_FILE = 'temp/potential_jobs.json'
JOBS_HTML_FILE      = 'temp/jobs_html.json'

def fetch_html(url, session):
    try:
        r = session.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        return r.text
    except Exception as e:
        return None

class Command(BaseCommand):
    help = "Fetch full HTML for jobs that passed phase 1 and store in temp/jobs_html.json"

    def handle(self, *args, **options):
        if not os.path.exists(POTENTIAL_JOBS_FILE):
            self.stdout.write(self.style.ERROR(
                "temp/potential_jobs.json not found. Run get_potential_jobs first."
            ))
            return

        with open(POTENTIAL_JOBS_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)

        if not jobs:
            self.stdout.write(self.style.ERROR(
                "temp/potential_jobs.json is empty. Nothing to fetch."
            ))
            return

        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        output  = []
        fetched = 0
        failed  = 0

        for job in jobs:
            url = job.get('employer_url')
            self.stdout.write(f"Fetching: {job['title']} | {job['employer']}")

            if not url:
                self.stdout.write(self.style.WARNING(f"  No employer URL, skipping."))
                failed += 1
                continue

            html = fetch_html(url, session)

            if not html:
                self.stdout.write(self.style.WARNING(f"  Failed to fetch {url}"))
                failed += 1
                continue

            output.append({
                "id":       job["id"],
                "title":    job["title"],
                "employer": job["employer"],
                "url":      url,
                "html":     html,
            })
            fetched += 1

        with open(JOBS_HTML_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        # Pop successfully fetched jobs from potential_jobs.json
        fetched_ids = {job["id"] for job in output}
        remaining   = [j for j in jobs if j["id"] not in fetched_ids]

        if remaining:
            with open(POTENTIAL_JOBS_FILE, 'w', encoding='utf-8') as f:
                json.dump(remaining, f, indent=2, ensure_ascii=False)
            self.stdout.write(f"{len(remaining)} jobs remaining in potential_jobs.json")
        else:
            os.remove(POTENTIAL_JOBS_FILE)
            self.stdout.write("potential_jobs.json empty, deleted.")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {fetched} fetched, {failed} failed. Written to {JOBS_HTML_FILE}"
        ))