# Tools Index

# Tools Index

Always run `get_state` first to determine current pipeline state and next step.
Never call anything under `tools/internal/` — these are infrastructure scripts.

## Normal Flow
Follow this exact sequence of tool calls to move the pipeline forward:

1. `./tools/scrape_overview/scrape_overview.sh`
2. `./tools/get_potential_jobs/get_potential_jobs.sh`
3. Call `./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>` for each job in `temp/potential_jobs.json`
4. `./tools/fetch_job_html/fetch_job_html.sh`
5. Call `./tools/rank_job/rank_job.sh <job_id> <score>` for each job in `temp/jobs_html.json`
6. `./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>`
7. `./tools/create_job_folders/create_job_folders.sh`
8. For each folder in `jobs_data/potential/` read `job.json` and write `cover_letter.md`

Steps 3 and 5 repeat until their respective temp files are empty and deleted.
Always call `get_state` if unsure which step you are on.

## get_state
Check current pipeline state, allowed tools and their transitions.
Always allowed from any state. Read only, no state change.
Usage: `./tools/get_state/get_state.sh`

## scrape_overview
Scrape Jobindex for new job listings using search words and blacklist filters.
Always allowed from any state. Resets to `scraping`.
Usage: `./tools/scrape_overview/scrape_overview.sh`

## get_potential_jobs
Dumps all potential jobs to `temp/potential_jobs.json` with id, title, employer and snippet.
Allowed from `scraping` and later. Resets to `phase1_ranking`.
Usage: `./tools/get_potential_jobs/get_potential_jobs.sh`

## process_phase1
Process a pass or fail decision for a single job based on title and snippet.
- pass: keeps job in DB, ready for HTML fetch
- fail: removes job from DB, stays in Visited so it is never revisited
Job is popped from `temp/potential_jobs.json` either way.
Only allowed from `phase1_ranking`.
Usage: `./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>`

## fetch_job_html
Fetches full HTML for all jobs that passed phase 1.
Writes to `temp/jobs_html.json`.
Only allowed from `phase1_ranking` when `temp/potential_jobs.json` is empty.
Usage: `./tools/fetch_job_html/fetch_job_html.sh`

## rank_job
Ranks a single job with a score from 1-10 and writes to RankedJob table.
Pops job from `temp/jobs_html.json`, deletes file if empty.
Only allowed from `phase2_ranking`.
Usage: `./tools/rank_job/rank_job.sh <job_id> <score>`

## get_ranked_jobs
Dumps all ranked jobs above a score threshold to `temp/ranked_jobs.json`.
Ordered by score descending.
Allowed from `phase2_ranking` and later. Resets to `creating_folders`.
Usage: `./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>`

## create_job_folders
Creates a folder for every job in `temp/ranked_jobs.json`.
Each folder contains `job.json` and an empty `cover_letter.md`.
Deletes `temp/ranked_jobs.json` when done.
Only allowed from `creating_folders`.
Usage: `./tools/create_job_folders/create_job_folders.sh`