import os
import json
from django.core.management.base import BaseCommand
from jobs.models import Job, RankedJob

class Command(BaseCommand):
    help = "Check pipeline health and current state"

    def handle(self, *args, **options):
        pass