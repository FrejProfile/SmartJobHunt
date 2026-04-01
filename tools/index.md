# Tools Index

Always run `check_health` first to determine current pipeline state and next step.

## Tools

### check_health
Check current pipeline state and get recommended next step.
Usage: `./tools/check_health/check_health.sh`

### get_potential_jobs
Dumps all potential jobs to `temp/potential_jobs.json` with id, title, employer and snippet.
Run before phase 1 ranking.
Usage: `./tools/get_potential_jobs/get_potential_jobs.sh`

### process_phase1
Process a pass or fail decision for a single job based on title and snippet.
- pass: keeps job in DB, ready for HTML fetch
- fail: removes job from DB, stays in Visited so it is never revisited
Job is popped from `temp/potential_jobs.json` either way.
Usage: `./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>`

### scrape_jobs
Fetches full HTML for all jobs that passed phase 1.
Run once after all phase 1 decisions are made.
Usage: `./tools/scrape_jobs/scrape_jobs.sh`

### get_ranked_jobs
Dumps all ranked jobs above a score threshold to `temp/ranked_jobs.json`.
Run after phase 2 scoring.
Usage: `./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>`

### create_job_folder
Creates folder structure and saves cover letter for a specific job.
Run after Claude has written the cover letter content.
Usage: `./tools/create_job_folder/create_job_folder.sh <job_id>`

### fetch_job_html
Fetches full HTML for all jobs in `temp/potential_jobs.json` and writes to `temp/jobs_html.html`.
Run after phase 1 ranking is complete.
Usage: `./tools/fetch_job_html/fetch_job_html.sh`