#!/bin/bash
# Usage: ./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

source "$PROJECT_ROOT/tools/internal/guard.sh" "process_phase1"

python manage.py process_phase1 --job-id $1 --decision $2

source "$PROJECT_ROOT/tools/internal/update_state.sh" "process_phase1"