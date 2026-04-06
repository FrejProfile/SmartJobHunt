# Task: Write Cover Letters

## Overview
Write a cover letter for each ranked job. Letters must be honest, direct and
natural — no cover letter voice, no sycophantic closings.

## Before You Start
1. Read `profile.md` for candidate background, tone preferences and honest framing rules
2. Read `examples/index.md` and load relevant examples to calibrate tone and structure
3. Read `competences/index.md` to know what competences are available to lazy load
4. Check `jobs_data/potential/` for folders — each has a `job.json` and `cover_letter.md`

## Process
For each job folder in `jobs_data/potential/<id>/`:
1. Check if `cover_letter.md` already has content — if yes skip it
2. Read `job.json` for job details and full HTML
3. Identify relevant competences and lazy load from `competences/`
4. Write the cover letter directly into `cover_letter.md`

## Cover Letter Guidelines
- Language match the job posting — Danish posting gets a Danish letter
- Length: approximately one page
- Tone: direct and natural, first person, no corporate filler phrases
- Structure: why this role, what you bring, brief closing
- Only include competences that are genuinely relevant to this specific role
- Never overclaim — if experience is small scale say so and frame it honestly
- No sycophantic closing lines

## Competence Loading
Only load competences that are directly relevant to the job requirements.
Check `competences/index.md` first, then load only the summaries you need.
Do not load all competences for every letter.

## Notes
- If context window is getting full, finish the current letter, save it, then
  let the user know to restart context — remaining jobs are still in their folders
- Each letter is independent — restarting context does not affect completed letters