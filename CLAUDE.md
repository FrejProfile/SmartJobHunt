# SmartJobSearch — Claude Code Guide

## Project Overview
This is an automated job application pipeline. Your role is to rank job listings
and write cover letters based on the candidate's competences and profile.

## Goal
The pipeline has one forward path. Always prefer the transition that moves
the state forward over resets. The forward path is:

idle → scraping → phase1_ranking → phase2_ranking → creating_folders → writing_letters → done

Only move backwards if explicitly asked to by the user.

## Responsibilities
Your job is to move the pipeline forward. After checking state with `get_state`,
you should always be working towards the next state transition. Do not stop between
states unless you have run out of allowed tools or are waiting for user input.

If you are mid-task (e.g. ranking jobs) and your context window is getting full,
complete the current job, call the relevant tool to save progress, then let the
user know they can restart your context and you will continue from where you left off.

## How to Orient Yourself
Always start by checking the current pipeline state:
```bash
./tools/get_state/get_state.sh
```
This tells you the current state, allowed tools and their transitions.

## Folder Structure
Every folder you interact with has the same structure:
- `index.md` is always the entry point
- Subfolders contain the actual content

The three folders you interact with:
- `tools/` — tools you can call, read `tools/index.md` first
- `competences/` — your candidate context, read `competences/index.md` first
- `claude_tasks/` — task instructions, read `claude_tasks/index.md` first

## Workflow
1. Check state with `get_state`
2. Read `claude_tasks/index.md` to find the relevant task
3. Follow the task instructions, using tools from `tools/index.md`
4. Load competences lazily from `competences/index.md` only when needed

## Key Files
- `profile.md` — candidate background, tone and preferences
- `examples/` — reference cover letters, read `examples/index.md` before writing any letter
- `temp/` — ephemeral state files, message passing between tools and Claude
- `jobs_data/potential/<id>/` — per job folder with `job.json` and `cover_letter.md`

## Tone Corrections
- Do not hedge excessively — "I wouldn't claim deep production experience" reads
  as weak. Instead frame honestly but positively: "Docker is something I have been
  actively building experience with through real projects"
- Do not split experience into short disconnected fragments — weave competences
  into flowing paragraphs that tell a coherent story
- Letters should read confident and grounded, not apologetic

## Rules
- Always read an `index.md` before entering any subfolder
- Never call anything under `tools/internal/`
- Load competences lazily — only fetch what is relevant to the current job
- Language match cover letters to the job posting language
- Never overclaim experience — read `profile.md` for honest framing guidelines
- Always prefer forward transitions over resets