# Task: Phase 1 Ranking

## Overview
Quick pass/fail evaluation of all potential jobs based on title and snippet.
Goal is to filter out clearly irrelevant jobs before fetching full HTML.
When in doubt pass — it is cheaper to fetch HTML for a borderline job than to miss a good one.

## Before You Start
1. Read `profile.md` to understand the candidate background and target roles
2. Read `temp/potential_jobs.json` to see all jobs to evaluate

## Process
For each job in `temp/potential_jobs.json`:
1. Read the title and snippet
2. Ask: is this plausibly relevant to the candidate?
3. Call:
```bash
./tools/process_phase1/process_phase1.sh <job_id> <pass|fail>
```
4. Continue until `temp/potential_jobs.json` is empty and deleted

## When to Fail a Job
- Clearly wrong domain (cooking, retail, healthcare etc.)
- Requires qualifications the candidate does not have and cannot argue for
- Purely sales, management or administrative role with no technical component

## When to Pass a Job
- Right domain even if not a perfect match
- Unclear from snippet alone — give it the benefit of the doubt
- Adjacent domain where candidate skills could transfer

## After Phase 1
When `temp/potential_jobs.json` is empty call:
```bash
./tools/fetch_job_html/fetch_job_html.sh
```
This fetches full HTML for all passed jobs and writes to `temp/jobs_html.json`.
State will move to `phase2_ranking`.