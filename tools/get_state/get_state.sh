#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

python3 -c "
import json, os

STATE_FILE = 'temp/state.json'

if not os.path.exists(STATE_FILE):
    print('No state file found. Initialize with:')
    print('  echo \'{\"state\": \"0\", \"history\": []}\' > temp/state.json')
    exit(1)

with open(STATE_FILE) as f:
    data = json.load(f)

state = data['state']
history = data['history']

TRANSITIONS = {
    '0': {
        'description': 'Idle — pipeline not started',
        'tools': [
            ('scrape_overview', 'Scrape Jobindex for new jobs → state 1'),
        ]
    },
    '1': {
        'description': 'Jobs scraped and stored in DB',
        'tools': [
            ('scrape_overview', 'Scrape again to add more jobs → state 1'),
            ('get_potential_jobs', 'Dump potential jobs to temp/potential_jobs.json → state 2'),
        ]
    },
    '2': {
        'description': 'Phase 1 ranking — process potential_jobs.json pass/fail',
        'tools': [
            ('process_phase1 <job_id> <pass|fail>', 'Process one job → stay 2 or move 3 when empty'),
            ('get_potential_jobs', 'Repopulate potential_jobs.json → state 2'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
    '3': {
        'description': 'Phase 1 done — potential_jobs.json empty',
        'tools': [
            ('get_potential_jobs', 'Repopulate potential_jobs.json → state 3.1'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
    '3.1': {
        'description': 'Phase 1 done — potential_jobs.json recreated, ready to fetch HTML',
        'tools': [
            ('fetch_job_html', 'Fetch full HTML for passed jobs → state 4'),
            ('get_potential_jobs', 'Repopulate potential_jobs.json → state 3.1'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
    '4': {
        'description': 'Phase 2 ranking — score jobs in jobs_html.json',
        'tools': [
            ('rank_job <job_id> <score>', 'Score one job → stay 4 or move 5 when empty'),
            ('get_potential_jobs', 'Reset to phase 1 → state 2'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
    '5': {
        'description': 'Phase 2 done — jobs_html.json empty',
        'tools': [
            ('get_ranked_jobs <threshold>', 'Dump ranked jobs above threshold → state 6'),
            ('get_potential_jobs', 'Reset to phase 1 → state 2'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
    '6': {
        'description': 'Ranked jobs dumped — ready to create job folders',
        'tools': [
            ('create_job_folders', 'Create folder structure for each ranked job → state 7'),
            ('get_ranked_jobs <threshold>', 'Re-dump with different threshold → state 6'),
        ]
    },
    '7': {
        'description': 'Folders created — write cover letters',
        'tools': [
            ('get_ranked_jobs <threshold>', 'Re-dump with different threshold → state 6'),
            ('scrape_overview', 'Reset — scrape more jobs → state 1'),
        ]
    },
}

info = TRANSITIONS.get(state, {})
print(f'\n=== Pipeline State ===')
print(f'Current state: {state} — {info.get(\"description\", \"unknown\")}')

if history:
    last = history[-1]
    print(f'Last event:    {last[\"event\"]} ({last[\"timestamp\"]})')

print(f'\n=== Allowed Tools ===')
tools = info.get('tools', [])
if tools:
    for tool, description in tools:
        print(f'  ./tools/{tool.split()[0]}/{tool.split()[0]}.sh {\" \".join(tool.split()[1:])}')
        print(f'    → {description}')
        print()
else:
    print('  No tools available for this state.')

print(f'=== History (last 5) ===')
for entry in history[-5:]:
    print(f'  {entry[\"timestamp\"]} | {entry[\"event\"]}')
"