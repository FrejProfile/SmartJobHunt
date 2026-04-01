#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
source .venv/bin/activate

python3 -c "
import json, os

ranked_jobs_file = 'temp/ranked_jobs.json'

if not os.path.exists(ranked_jobs_file):
    print('temp/ranked_jobs.json not found. Run get_ranked_jobs first.')
    exit(1)

with open(ranked_jobs_file) as f:
    jobs = json.load(f)

for job in jobs:
    folder = f'jobs_data/potential/{job[\"id\"]}'
    os.makedirs(folder, exist_ok=True)

    with open(f'{folder}/job.json', 'w', encoding='utf-8') as f:
        json.dump(job, f, indent=2, ensure_ascii=False)

    cover_letter = f'{folder}/cover_letter.md'
    if not os.path.exists(cover_letter):
        open(cover_letter, 'w').close()

    print(f'Created folder for job {job[\"id\"]}: {job[\"title\"]} | {job[\"employer\"]}')

os.remove(ranked_jobs_file)
print('ranked_jobs.json deleted.')
"