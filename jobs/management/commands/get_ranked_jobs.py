import os
import json
from django.core.management.base import BaseCommand
from jobs.models import RankedJob

RANKED_JOBS_FILE = 'temp/ranked_jobs.json'

class Command(BaseCommand):
    help = "Dump ranked jobs above threshold to temp/ranked_jobs.json"

    def add_arguments(self, parser):
        parser.add_argument('--threshold', type=int, default=6)

    def handle(self, *args, **options):
        threshold = options['threshold']

        jobs = (
            RankedJob.objects
            .filter(score__gte=threshold, job__status='ranked')
            .select_related('job')
            .order_by('-score')
        )

        if not jobs.exists():
            self.stdout.write(self.style.WARNING(
                f"No ranked jobs found above threshold {threshold}."
            ))
            return

        output = []
        for ranked in jobs:
            output.append({
                "id":       ranked.job.id,
                "title":    ranked.job.title,
                "employer": ranked.job.employer,
                "url":      ranked.job.visited.url,
                "score":    ranked.score,
                "html":     ranked.html,
            })

        with open(RANKED_JOBS_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(
            f"Wrote {len(output)} jobs above score {threshold} to {RANKED_JOBS_FILE}"
        ))