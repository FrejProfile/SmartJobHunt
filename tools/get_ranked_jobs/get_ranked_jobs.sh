#!/bin/bash
# Usage: ./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

source "$PROJECT_ROOT/tools/internal/guard.sh" "get_ranked_jobs"

python manage.py get_ranked_jobs --threshold ${1:-6}

source "$PROJECT_ROOT/tools/internal/update_state.sh" "get_ranked_jobs"