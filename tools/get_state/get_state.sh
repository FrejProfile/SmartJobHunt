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
    print('  echo \'{\"state\": \"idle\", \"history\": []}\' > temp/state.json')
    exit(1)

with open(STATE_FILE) as f:
    data = json.load(f)

state = data['state']
history = data['history']

# Allowed tools and their next state per current state
TRANSITIONS = {
    'idle': [
        ('scrape_overview', 'scraping', 'always allowed'),
    ],
    'scraping': [
        ('scrape_overview',    'scraping',       'run again to add more jobs'),
        ('get_potential_jobs', 'phase1_ranking', 'when ready to start ranking'),
    ],
    'phase1_ranking': [
        ('process_phase1',  'phase1_ranking', 'while temp/potential_jobs.json not empty'),
        ('fetch_job_html',  'phase2_ranking', 'only when temp/potential_jobs.json is empty'),
        ('scrape_overview', 'scraping',       'reset — adds more jobs'),
    ],
    'fetching_html': [
        ('rank_job', 'phase2_ranking', 'always allowed'),
    ],
    'phase2_ranking': [
        ('rank_job',        'phase2_ranking',   'while temp/jobs_html.json not empty'),
        ('get_ranked_jobs', 'creating_folders', 'only when temp/jobs_html.json is empty'),
        ('get_potential_jobs', 'phase1_ranking', 'reset — redo phase 1'),
        ('scrape_overview', 'scraping',          'reset — adds more jobs'),
    ],
    'creating_folders': [
        ('create_job_folders', 'writing_letters', 'always allowed'),
        ('get_ranked_jobs',    'creating_folders', 'reset — change threshold'),
    ],
    'writing_letters': [
        ('get_ranked_jobs', 'creating_folders', 'reset — change threshold'),
    ],
    'done': [
        ('scrape_overview',    'scraping',       'start over with new jobs'),
        ('get_potential_jobs', 'phase1_ranking', 'reprocess existing jobs'),
    ],
}

print(f'\n=== Pipeline State ===')
print(f'Current state: {state}')

if history:
    last = history[-1]
    print(f'Last event:    {last[\"event\"]} ({last[\"timestamp\"]})')

print(f'\n=== Allowed Tools ===')
allowed = TRANSITIONS.get(state, [])
if allowed:
    for tool, next_state, condition in allowed:
        print(f'  {tool}')
        print(f'    → next state : {next_state}')
        print(f'    → condition  : {condition}')
        print(f'    → usage      : ./tools/{tool}/{tool}.sh')
        print()
else:
    print('  No tools available for this state.')

print(f'=== History ===')
for entry in history[-5:]:
    print(f'  {entry[\"timestamp\"]} | {entry[\"event\"]}')
"
