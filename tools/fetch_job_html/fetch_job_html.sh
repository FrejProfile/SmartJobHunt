#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

source "$PROJECT_ROOT/tools/internal/guard.sh" "fetch_job_html"

python manage.py fetch_job_html

source "$PROJECT_ROOT/tools/internal/update_state.sh" "fetch_job_html"