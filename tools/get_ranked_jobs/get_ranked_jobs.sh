#!/bin/bash
# Usage: ./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate
python manage.py get_ranked_jobs --threshold ${1:-6}