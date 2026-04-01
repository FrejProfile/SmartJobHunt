#!/bin/bash
# Usage: source tools/internal/update_state.sh <tool_name> <note>
TOOL=$1
NOTE=$2
STATE_FILE="temp/state.json"

# Dev mode bypass
if [ "$DEV_MODE" = "1" ]; then
    echo "[DEV_MODE] Skipping state update for $TOOL"
    return 0
fi

# Next state map
declare -A NEXT_STATE
NEXT_STATE["scrape_overview"]="scraping"
NEXT_STATE["get_potential_jobs"]="phase1_ranking"
NEXT_STATE["process_phase1"]="phase1_ranking"
NEXT_STATE["fetch_job_html"]="phase2_ranking"
NEXT_STATE["rank_job"]="phase2_ranking"
NEXT_STATE["get_ranked_jobs"]="creating_folders"
NEXT_STATE["create_job_folders"]="writing_letters"

NEXT=${NEXT_STATE[$TOOL]}
if [ -z "$NEXT" ]; then
    echo "[UPDATE_STATE] Unknown tool: $TOOL"
    exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S")

python3 -c "
import json, os
state_file = '$STATE_FILE'
if os.path.exists(state_file):
    with open(state_file) as f:
        data = json.load(f)
else:
    data = {'state': 'idle', 'history': []}

data['state'] = '$NEXT'
data['history'].append({
    'event': '$TOOL',
    'timestamp': '$TIMESTAMP',
    'note': '$NOTE'
})

with open(state_file, 'w') as f:
    json.dump(data, f, indent=2)
print('[STATE] $TOOL → $NEXT')
"