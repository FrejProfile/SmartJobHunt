#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate
source "$PROJECT_ROOT/tools/internal/guard.sh" "scrape_overview"
python manage.py scrape_overview
source "$PROJECT_ROOT/tools/internal/update_state.sh" "scrape_overview"