#!/bin/bash
# Usage: source tools/internal/update_state.sh <tool_name>

TOOL=$1
STATE_FILE="temp/state.json"

# Dev mode bypass
if [ "$DEV_MODE" = "1" ]; then
    echo "[DEV_MODE] Skipping state update for $TOOL"
    return 0
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S")

# Read current state
CURRENT_STATE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['state'])")

# ─────────────────────────────────────────
# State 0: idle
# Event: scrape_overview → 1
# ─────────────────────────────────────────
if [ "$TOOL" = "scrape_overview" ]; then
    NEXT_STATE="1"

# ─────────────────────────────────────────
# State 1: scraping
# Event: get_potential_jobs → 2
#
# State 3: phase1 done
# Event: get_potential_jobs → 3.1
# ─────────────────────────────────────────
elif [ "$TOOL" = "get_potential_jobs" ]; then
    if [ "$CURRENT_STATE" = "3" ]; then
        NEXT_STATE="3.1"
    else
        NEXT_STATE="2"
    fi

# ─────────────────────────────────────────
# State 2: phase1 processing
# Event: process_phase1
#   → stay 2 if potential_jobs.json still exists
#   → move 3 if potential_jobs.json deleted
# ─────────────────────────────────────────
elif [ "$TOOL" = "process_phase1" ]; then
    if [ ! -f "temp/potential_jobs.json" ]; then
        NEXT_STATE="3"
    else
        NEXT_STATE="2"
    fi

# ─────────────────────────────────────────
# State 3.1: potential_jobs.json recreated
# Event: fetch_job_html → 4
# ─────────────────────────────────────────
elif [ "$TOOL" = "fetch_job_html" ]; then
    NEXT_STATE="4"

# ─────────────────────────────────────────
# State 4: phase2 processing
# Event: rank_job
#   → stay 4 if jobs_html.json still exists
#   → move 5 if jobs_html.json deleted
# ─────────────────────────────────────────
elif [ "$TOOL" = "rank_job" ]; then
    if [ ! -f "temp/jobs_html.json" ]; then
        NEXT_STATE="5"
    else
        NEXT_STATE="4"
    fi

# ─────────────────────────────────────────
# State 5: phase2 done, jobs_html empty
# Event: get_ranked_jobs → 6
# ─────────────────────────────────────────
elif [ "$TOOL" = "get_ranked_jobs" ]; then
    NEXT_STATE="6"

# ─────────────────────────────────────────
# State 6: ranked_jobs.json exists
# Event: create_job_folders → 7
# ─────────────────────────────────────────
elif [ "$TOOL" = "create_job_folders" ]; then
    NEXT_STATE="7"

# ─────────────────────────────────────────
# State 7: writing letters
# No tool transitions — Claude writes letters
# without tool calls, state stays at 7
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# get_state is read only, no state change
# ─────────────────────────────────────────
elif [ "$TOOL" = "get_state" ]; then
    return 0

else
    echo "[UPDATE_STATE] Unknown tool: $TOOL"
    exit 1
fi

# Write new state and append to history
python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
data['state'] = '$NEXT_STATE'
data['history'].append({
    'event': '$TOOL',
    'timestamp': '$TIMESTAMP',
})
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
print('[STATE] $TOOL → $NEXT_STATE')
"