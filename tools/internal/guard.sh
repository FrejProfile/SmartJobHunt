#!/bin/bash
# Usage: source tools/internal/guard.sh <tool_name>
# Returns 0 if allowed, exits 1 if not

TOOL=$1
STATE_FILE="tools/internal/state.json"

# Always allowed
if [ "$TOOL" = "get_state" ]; then return 0; fi

# Dev mode bypass
if [ "$DEV_MODE" = "1" ]; then
    echo "[DEV_MODE] Skipping guard for $TOOL"
    return 0
fi

# Read current state
if [ ! -f "$STATE_FILE" ]; then
    echo "[GUARD] No state file found. Initialize with:"
    echo "  echo '{\"state\": \"0\", \"history\": []}' > temp/state.json"
    exit 1
fi

CURRENT_STATE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['state'])")

# State 0: idle
if [ "$CURRENT_STATE" = "0" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    echo "[GUARD] State 0 (idle) | Allowed: scrape_overview"
    exit 1

# State 1: scraped jobs in db, ready to pull potential jobs
elif [ "$CURRENT_STATE" = "1" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    echo "[GUARD] State 1 (scraping) | Allowed: scrape_overview, get_potential_jobs"
    exit 1

# State 2: potential_jobs.json exists, process pass/fail
elif [ "$CURRENT_STATE" = "2" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "process_phase1" ]; then return 0; fi
    echo "[GUARD] State 2 (phase1 processing) | Allowed: scrape_overview, get_potential_jobs, process_phase1"
    exit 1

# State 3: potential_jobs.json empty, ai has filtered jobs
elif [ "$CURRENT_STATE" = "3" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    echo "[GUARD] State 3 (phase1 done) | Allowed: scrape_overview, get_potential_jobs"
    exit 1

# State 3.1: fetch_job_html called, jobs_html.json created
elif [ "$CURRENT_STATE" = "3.1" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "fetch_job_html" ]; then return 0; fi
    echo "[GUARD] State 3.1 (ready to fetch html) | Allowed: scrape_overview, get_potential_jobs, fetch_job_html"
    exit 1

# State 4: jobs_html.json exists, rank jobs
elif [ "$CURRENT_STATE" = "4" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "rank_job" ]; then return 0; fi
    echo "[GUARD] State 4 (phase2 processing) | Allowed: scrape_overview, get_potential_jobs, rank_job"
    exit 1

# State 5: jobs_html.json empty, ready to get ranked jobs
elif [ "$CURRENT_STATE" = "5" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "get_ranked_jobs" ]; then return 0; fi
    echo "[GUARD] State 5 (phase2 done) | Allowed: scrape_overview, get_potential_jobs, get_ranked_jobs"
    exit 1

# State 6: ranked_jobs.json exists, create job folders
elif [ "$CURRENT_STATE" = "6" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "create_job_folders" ]; then return 0; fi
    echo "[GUARD] State 6 (creating folders) | Allowed: scrape_overview, get_potential_jobs, create_job_folders"
    exit 1

# State 7: folders created, write cover letters
elif [ "$CURRENT_STATE" = "7" ]; then
    if [ "$TOOL" = "scrape_overview" ]; then return 0; fi
    if [ "$TOOL" = "get_potential_jobs" ]; then return 0; fi
    if [ "$TOOL" = "get_ranked_jobs" ]; then return 0; fi
    echo "[GUARD] State 7 (writing letters) | Allowed: scrape_overview, get_potential_jobs, get_ranked_jobs"
    exit 1

else
    echo "[GUARD] Unknown state: $CURRENT_STATE"
    exit 1
fi