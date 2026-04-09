import os
import re

from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from jobs.models import Job

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPETENCES_DIR = os.path.join(_BASE, 'competences')
JOBS_DATA_DIR   = os.path.join(_BASE, 'jobs_data', 'potential')
PROFILE_PATH    = os.path.join(_BASE, 'profile.md')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _safe_slug(name):
    return re.sub(r'[^a-z0-9_-]+', '_', name.lower().strip()).strip('_')


def _read(path):
    with open(path, 'r') as f:
        return f.read()


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def _assert_safe(path, root):
    """Raise Http404 if path escapes root."""
    if not os.path.realpath(path).startswith(os.path.realpath(root) + os.sep):
        raise Http404


def _scan_competences():
    """Return [{slug, label, subs:[{slug, label}]}] from the filesystem."""
    if not os.path.isdir(COMPETENCES_DIR):
        return []
    categories = []
    for cat in sorted(os.listdir(COMPETENCES_DIR)):
        cat_path = os.path.join(COMPETENCES_DIR, cat)
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
        if not os.path.exists(os.path.join(cat_path, 'summary.md')):
            continue
        subs = []
        for sub in sorted(os.listdir(cat_path)):
            sub_path = os.path.join(cat_path, sub)
            if not os.path.isdir(sub_path) or sub.startswith('.'):
                continue
            if os.path.exists(os.path.join(sub_path, 'summary.md')):
                subs.append({'slug': sub, 'label': sub.replace('_', ' ').title()})
        categories.append({
            'slug': cat,
            'label': cat.replace('_', ' ').title(),
            'subs': subs,
        })
    return categories


def _md_ctx(title, slug, content, save_url, back_url):
    return {
        'title': title,
        'files': [{'slug': slug, 'label': title, 'content': content}],
        'save_url': save_url,
        'back_url': back_url,
    }


# ── Profile ───────────────────────────────────────────────────────────────────

def edit_profile(request):
    if request.method == 'POST':
        _write(PROFILE_PATH, request.POST.get('content_profile', ''))
        return redirect('editor:edit_profile')
    return render(request, 'jobs/markdown_editor.html', _md_ctx(
        title='Profile',
        slug='profile',
        content=_read(PROFILE_PATH),
        save_url=reverse('editor:edit_profile'),
        back_url=reverse('jobs:table_browser'),
    ))


# ── Competences browser ───────────────────────────────────────────────────────

def competences(request):
    return render(request, 'editor/competences.html', {
        'active': 'competences',
        'tree': _scan_competences(),
        'has_index': os.path.exists(os.path.join(COMPETENCES_DIR, 'index.md')),
    })


def edit_index(request):
    path = os.path.join(COMPETENCES_DIR, 'index.md')
    if request.method == 'POST':
        _write(path, request.POST.get('content_index', ''))
        return redirect('editor:edit_index')
    return render(request, 'jobs/markdown_editor.html', _md_ctx(
        title='Competences Index',
        slug='index',
        content=_read(path) if os.path.exists(path) else '',
        save_url=reverse('editor:edit_index'),
        back_url=reverse('editor:competences'),
    ))


def edit_competence(request, category, sub=None):
    if sub:
        # Deepest level: subcategory summary
        path = os.path.join(COMPETENCES_DIR, category, sub, 'summary.md')
        slug = f'{category}__{sub}'
        title = f'{category.replace("_", " ").title()} / {sub.replace("_", " ").title()}'
        _assert_safe(path, COMPETENCES_DIR)
        if not os.path.exists(path):
            raise Http404
        if request.method == 'POST':
            _write(path, request.POST.get('content_' + slug, ''))
            return redirect(request.path)
        return render(request, 'jobs/markdown_editor.html', _md_ctx(
            title=title,
            slug=slug,
            content=_read(path),
            save_url=reverse('editor:edit_sub_competence', kwargs={'category': category, 'sub': sub}),
            back_url=reverse('editor:edit_competence', kwargs={'category': category}),
        ))
    else:
        # Second level: category hub — editable summary + subcategory list
        path = os.path.join(COMPETENCES_DIR, category, 'summary.md')
        slug = category
        _assert_safe(path, COMPETENCES_DIR)
        if not os.path.exists(path):
            raise Http404
        if request.method == 'POST':
            _write(path, request.POST.get('content_' + slug, ''))
            return redirect(request.path)
        cat_dir = os.path.join(COMPETENCES_DIR, category)
        subs = [
            {'slug': s, 'label': s.replace('_', ' ').title()}
            for s in sorted(os.listdir(cat_dir))
            if os.path.isdir(os.path.join(cat_dir, s))
            and not s.startswith('.')
            and os.path.exists(os.path.join(cat_dir, s, 'summary.md'))
        ]
        return render(request, 'editor/category.html', {
            'active': 'competences',
            'title': category.replace('_', ' ').title(),
            'slug': slug,
            'content': _read(path),
            'category_slug': category,
            'subs': subs,
        })


def new_competence(request, category=None):
    if request.method == 'POST':
        name = _safe_slug(request.POST.get('name', ''))
        if not name:
            return redirect(request.path)
        if category:
            path = os.path.join(COMPETENCES_DIR, category, name, 'summary.md')
            _assert_safe(path, COMPETENCES_DIR)
            _write(path, f'# {name.replace("_", " ").title()}\n')
            return redirect('editor:edit_sub_competence', category=category, sub=name)
        else:
            path = os.path.join(COMPETENCES_DIR, name, 'summary.md')
            _assert_safe(path, COMPETENCES_DIR)
            _write(path, f'# {name.replace("_", " ").title()}\n')
            return redirect('editor:edit_competence', category=name)

    return render(request, 'editor/new_competence.html', {
        'active': 'competences',
        'category': category,
        'parent_label': category.replace('_', ' ').title() if category else None,
    })


# ── Cover letters ─────────────────────────────────────────────────────────────

def cover_letters(request):
    entries = []
    if os.path.isdir(JOBS_DATA_DIR):
        for job_id_str in sorted(os.listdir(JOBS_DATA_DIR), key=lambda x: int(x) if x.isdigit() else x):
            letter_path = os.path.join(JOBS_DATA_DIR, job_id_str, 'cover_letter.md')
            if not os.path.exists(letter_path):
                continue
            try:
                job = Job.objects.get(pk=int(job_id_str))
            except (Job.DoesNotExist, ValueError):
                job = None
            entries.append({'id': job_id_str, 'job': job})
    return render(request, 'editor/cover_letters.html', {'active': 'letters', 'entries': entries})


def edit_cover_letter(request, job_id):
    path = os.path.join(JOBS_DATA_DIR, str(job_id), 'cover_letter.md')
    _assert_safe(path, JOBS_DATA_DIR)

    try:
        job = Job.objects.get(pk=job_id)
        label = f'{job.employer} — {job.title}'
    except Job.DoesNotExist:
        label = f'Job #{job_id}'

    if request.method == 'POST':
        _write(path, request.POST.get('content_letter', ''))
        return redirect('editor:edit_cover_letter', job_id=job_id)

    return render(request, 'editor/cover_letter_editor.html', {
        'title': 'Cover Letter',
        'label': label,
        'content': _read(path) if os.path.exists(path) else '',
        'save_url': reverse('editor:edit_cover_letter', kwargs={'job_id': job_id}),
        'back_url': reverse('editor:cover_letters'),
    })
