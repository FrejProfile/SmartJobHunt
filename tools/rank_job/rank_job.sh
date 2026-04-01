#!/bin/bash
# Usage: ./tools/rank_job/rank_job.sh <job_id> <score>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

source "$PROJECT_ROOT/tools/internal/guard.sh" "rank_job"

python manage.py rank_job --job-id $1 --score $2

source "$PROJECT_ROOT/tools/internal/update_state.sh" "rank_job"