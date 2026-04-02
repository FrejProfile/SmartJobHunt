# Task: Phase 2 Ranking

## Overview
Score each job from 1-10 based on full HTML content and candidate competences.
This is the final ranking that determines which jobs get cover letters.

## Before You Start
1. Read `profile.md` to understand candidate background, tone and honest framing rules
2. Read `competences/index.md` to know what competences are available to lazy load
3. Read `temp/jobs_html.json` to see all jobs to score

## Process
For each job in `temp/jobs_html.json`:
1. Read the full HTML content
2. Identify which competences are relevant and lazy load their summaries
3. Score the job from 1-10
4. Call:
```bash
./tools/rank_job/rank_job.sh <job_id> <score>
```
5. Continue until `temp/jobs_html.json` is empty and deleted

## Scoring Criteria
- 8-10: Strong match — right domain, right level, directly uses candidate core skills
- 5-7:  Partial match — related domain, candidate could make a case for fit
- 1-4:  Weak match — tangentially related, poor fit with candidate background

## Notes
- Do not overscore out of optimism
- A job in Danish should not be scored differently than one in English
- If requirements are vague, lean towards a higher score
- Cross reference with competences before finalising score

## After Phase 2
When `temp/jobs_html.json` is empty call:
```bash
./tools/get_ranked_jobs/get_ranked_jobs.sh <threshold>
```
Default threshold is 6. Adjust if too many or too few jobs remain.
State will move to `creating_folders`.