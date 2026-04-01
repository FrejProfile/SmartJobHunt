import json
import os
from django.core.management.base import BaseCommand
from jobs.models import Job


"""
Desciption:
-   Processes jobs listed in POTENTIAL_JOBS_FILE it when processed its deleted from json
    and if job didnt pass requirement its deleted from db
"""

POTENTIAL_JOBS_FILE = 'temp/potential_jobs.json'

class Command(BaseCommand):
    help = "Process phase 1 pass/fail decision for a job"

    def add_arguments(self, parser):
        parser.add_argument('--job-id', type=int, required=True)
        parser.add_argument('--decision', choices=['pass', 'fail'], required=True)

    def handle(self, *args, **options):
        job_id   = options['job_id']
        decision = options['decision']

        # Check if json exist before trying to open it
        if not os.path.exists(POTENTIAL_JOBS_FILE):
            self.stdout.write(self.style.ERROR(
                "temp/potential_jobs.json not found. Run get_potential_jobs first."
            ))
            return

        # Load current potential jobs
        with open(POTENTIAL_JOBS_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)

        # Pop the job from the list
        jobs = [j for j in jobs if j['id'] != job_id]

        if not jobs:
            os.remove(POTENTIAL_JOBS_FILE)
            self.stdout.write("potential_jobs.json empty, deleted.")
        else:
            with open(POTENTIAL_JOBS_FILE, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)    

        # Handle decision
        try:
            job = Job.objects.get(id=job_id)
            if decision == 'fail':
                job.delete()
                self.stdout.write(self.style.WARNING(
                    f"Deleted job {job_id} from database"
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Job {job_id} passed, ready for HTML fetch"
                ))
        except Job.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"Job {job_id} not found in database"
            ))