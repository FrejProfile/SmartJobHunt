#!/bin/bash
# Usage: ./tools/rank_job/rank_job.sh <job_id> <score>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate
python manage.py rank_job --job-id $1 --score $2