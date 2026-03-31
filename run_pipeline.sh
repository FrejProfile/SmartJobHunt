#!/bin/bash
source .venv/bin/activate

echo "Step 1: Scraping job overview..."
python manage.py scrape_overview.py

echo "Step 2: Filtering jobs"
python manage.py filter_jobs.py

echo "Step 3: Fetching new job pages..."
python manage.py scrape_jobs.py

echo "Step 3: Ready for Claude Code"
echo "Run: claude and follow rank_jobs.md then write_letters.md"