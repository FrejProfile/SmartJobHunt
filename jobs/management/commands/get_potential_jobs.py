import json
from django.core.management.base import BaseCommand
from jobs.models import Job

"""
Description:
-   Retrieves Jobs listed as potential from the Job table in the db
    and stores the meta data in ROOT/temp/potential_jobs.json that claude can process
"""

class Command(BaseCommand):
    help = "Dump potential jobs to temp/potential_jobs.json"

    def handle(self, *args, **options):
        jobs = Job.objects.filter(status='potential').values(
            'id', 'title', 'employer', 'snippet', 'employer_url'
        )

        output = list(jobs)

        with open('temp/potential_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(
            f"Wrote {len(output)} jobs to temp/potential_jobs.json"
        ))