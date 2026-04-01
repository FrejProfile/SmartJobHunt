import os
import json
from django.core.management.base import BaseCommand
from jobs.models import Job, RankedJob

JOBS_HTML_FILE = 'temp/jobs_html.json'

class Command(BaseCommand):
    help = "Rank a job and write to RankedJob table"

    def add_arguments(self, parser):
        parser.add_argument('--job-id', type=int, required=True)
        parser.add_argument('--score', type=int, required=True, choices=range(1, 11), metavar='[1-10]')

    def handle(self, *args, **options):
        job_id = options['job_id']
        score  = options['score']

        if not os.path.exists(JOBS_HTML_FILE):
            self.stdout.write(self.style.ERROR(
                "temp/jobs_html.json not found. Run fetch_job_html first."
            ))
            return

        with open(JOBS_HTML_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)

        # Find the job
        job_data = next((j for j in jobs if j['id'] == job_id), None)
        if not job_data:
            self.stdout.write(self.style.ERROR(
                f"Job {job_id} not found in jobs_html.json"
            ))
            return

        # Write to RankedJob table
        try:
            job = Job.objects.get(id=job_id)
            RankedJob.objects.update_or_create(
                job=job,
                defaults={
                    'score': score,
                    'html':  job_data['html'],
                }
            )
            self.stdout.write(self.style.SUCCESS(
                f"Ranked job {job_id} with score {score}"
            ))

            job.status = 'ranked'
            job.save()

        except Job.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"Job {job_id} not found in database"
            ))
            return

        # Pop from jobs_html.json
        jobs = [j for j in jobs if j['id'] != job_id]

        if not jobs:
            os.remove(JOBS_HTML_FILE)
            self.stdout.write("jobs_html.json empty, deleted.")
        else:
            with open(JOBS_HTML_FILE, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            self.stdout.write(f"{len(jobs)} jobs remaining in jobs_html.json")