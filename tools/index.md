# Tools

## get_potential_jobs
Dumps all potential jobs to `temp/potential_jobs.json` with id, title, employer and snippet.
Run before phase 1 ranking.
Usage: `./tools/get_potential_jobs/get_potential_jobs.sh`

## process_phase1
Process a pass or fail decision for a job from phase 1 ranking.
- pass: keeps job in database, ready for HTML fetch
- fail: removes job from database, stays in Visited
Job is popped from temp/potential_jobs.json either way.
Usage: `./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>`