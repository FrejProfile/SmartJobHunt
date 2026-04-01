#!/bin/bash
# Usage: source tools/internal/guard.sh <tool_name>
# Returns 0 if allowed, exits 1 if not

TOOL=$1
STATE_FILE="temp/state.json"

# Dev mode bypass
if [ "$DEV_MODE" = "1" ]; then
    echo "[DEV_MODE] Skipping guard for $TOOL"
    return 0
fi

# Always allowed tools
ALWAYS_ALLOWED=("get_state" "scrape_overview")
for t in "${ALWAYS_ALLOWED[@]}"; do
    if [ "$TOOL" = "$t" ]; then
        return 0
    fi
done

# Read current state
if [ ! -f "$STATE_FILE" ]; then
    echo "[GUARD] No state file found. Run scrape_overview first."
    exit 1
fi

CURRENT_STATE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['state'])")

# State order for hierarchy checks
declare -A STATE_ORDER
STATE_ORDER["idle"]=0
STATE_ORDER["scraping"]=1
STATE_ORDER["phase1_ranking"]=2
STATE_ORDER["fetching_html"]=3
STATE_ORDER["phase2_ranking"]=4
STATE_ORDER["creating_folders"]=5
STATE_ORDER["writing_letters"]=6
STATE_ORDER["done"]=7

CURRENT_ORDER=${STATE_ORDER[$CURRENT_STATE]}

# Tier 2 reset - allowed from scraping+
TIER2_TOOLS=("get_potential_jobs")
for t in "${TIER2_TOOLS[@]}"; do
    if [ "$TOOL" = "$t" ]; then
        if [ "$CURRENT_ORDER" -ge 1 ]; then
            return 0
        else
            echo "[GUARD] $TOOL requires state scraping or later. Current: $CURRENT_STATE"
            exit 1
        fi
    fi
done

# Tier 3 reset - allowed from phase2_ranking+
TIER3_TOOLS=("get_ranked_jobs")
for t in "${TIER3_TOOLS[@]}"; do
    if [ "$TOOL" = "$t" ]; then
        if [ "$CURRENT_ORDER" -ge 4 ]; then
            return 0
        else
            echo "[GUARD] $TOOL requires state phase2_ranking or later. Current: $CURRENT_STATE"
            exit 1
        fi
    fi
done

# Strict forward transitions
declare -A REQUIRED_STATE
REQUIRED_STATE["process_phase1"]="phase1_ranking"
REQUIRED_STATE["fetch_job_html"]="phase1_ranking"
REQUIRED_STATE["rank_job"]="phase2_ranking"
REQUIRED_STATE["create_job_folders"]="creating_folders"

if [ -n "${REQUIRED_STATE[$TOOL]}" ]; then
    REQUIRED="${REQUIRED_STATE[$TOOL]}"
    if [ "$CURRENT_STATE" != "$REQUIRED" ]; then
        echo "[GUARD] $TOOL requires state $REQUIRED. Current: $CURRENT_STATE"
        exit 1
    fi

    # Extra file checks for conditional transitions
    if [ "$TOOL" = "fetch_job_html" ] && [ -f "temp/potential_jobs.json" ]; then
        echo "[GUARD] fetch_job_html requires potential_jobs.json to be empty. Finish process_phase1 first."
        exit 1
    fi

    if [ "$TOOL" = "get_ranked_jobs" ] && [ -f "temp/jobs_html.json" ]; then
        echo "[GUARD] get_ranked_jobs requires jobs_html.json to be empty. Finish rank_job first."
        exit 1
    fi

    return 0
fi

echo "[GUARD] Unknown tool: $TOOL"
exit 1