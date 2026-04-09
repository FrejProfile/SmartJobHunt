import os

from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Job, RankedJob, Visited

# ── Markdown file registry ──────────────────────────────────────────────────
# Maps slug → absolute path. Only files listed here can be edited via the UI.
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_REGISTRY = {
    'filters':      os.path.join(_BASE, 'scripts', 'filters.md'),
    'search_words': os.path.join(_BASE, 'scripts', 'search_words.md'),
    'profile':      os.path.join(_BASE, 'profile.md'),
}

# Groups of files shown together on one editor page
FILE_GROUPS = {
    'active_filters': [
        {'slug': 'filters',      'label': 'Exclude Filters'},
        {'slug': 'search_words', 'label': 'Search Words'},
    ],
}


def _read_file(slug):
    path = FILE_REGISTRY[slug]
    with open(path, 'r') as f:
        return f.read()


def _write_file(slug, content):
    path = FILE_REGISTRY[slug]
    with open(path, 'w') as f:
        f.write(content)


# ── Generic single-file editor ──────────────────────────────────────────────

def edit_markdown(request, slug):
    if slug not in FILE_REGISTRY:
        raise Http404
    if request.method == 'POST':
        _write_file(slug, request.POST.get('content_' + slug, ''))
        return redirect('jobs:edit_markdown', slug=slug)
    files = [{'slug': slug, 'label': slug.replace('_', ' ').title(), 'content': _read_file(slug)}]
    return render(request, 'jobs/markdown_editor.html', {
        'title': slug.replace('_', ' ').title(),
        'files': files,
        'save_url': reverse('jobs:edit_markdown', kwargs={'slug': slug}),
        'back_url': reverse('jobs:table_browser'),
    })


# ── Active filters grouped editor ───────────────────────────────────────────

def active_filters(request):
    group = FILE_GROUPS['active_filters']
    if request.method == 'POST':
        for item in group:
            _write_file(item['slug'], request.POST.get('content_' + item['slug'], ''))
        return redirect('jobs:active_filters')
    files = [{**item, 'content': _read_file(item['slug'])} for item in group]
    return render(request, 'jobs/markdown_editor.html', {
        'title': 'Active Filters',
        'files': files,
        'save_url': reverse('jobs:active_filters'),
        'back_url': reverse('jobs:table_browser'),
    })


# ── Table browser ────────────────────────────────────────────────────────────

def table_browser(request):
    visited_rows = list(Visited.objects.values('id', 'url', 'first_seen'))
    job_rows = list(Job.objects.values('id', 'employer', 'title', 'status', 'employer_url', 'snippet', 'scraped_at'))
    ranked_rows = list(
        RankedJob.objects.annotate(
            job_title=F('job__title'),
            job_employer=F('job__employer'),
            job_url=F('job__employer_url'),
            job_snippet=F('job__snippet'),
        ).values('id', 'job_title', 'job_employer', 'job_url', 'job_snippet', 'score', 'scored_at')
    )

    tables = [
        {
            'key': 'job',
            'label': 'Jobs',
            'columns': [
                {'header': 'ID',         'field': 'id',           'type': 'narrow',   'sortable': False},
                {'header': 'Employer',   'field': 'employer',     'type': 'wrap',     'sortable': False},
                {'header': 'Title',      'field': 'title',        'type': 'wrap',     'sortable': True},
                {'header': 'Status',     'field': 'status',       'type': 'narrow',   'sortable': True},
                {'header': 'URL',        'field': 'employer_url', 'type': 'url',      'sortable': False},
                {'header': 'Snippet',    'field': 'snippet',      'type': 'snippet',  'sortable': False},
                {'header': 'Scraped At', 'field': 'scraped_at',   'type': 'narrow',   'sortable': True},
            ],
            'rows': job_rows,
        },
        {
            'key': 'visited',
            'label': 'Visited URLs',
            'columns': [
                {'header': 'ID',         'field': 'id',         'type': 'text', 'sortable': False},
                {'header': 'URL',        'field': 'url',        'type': 'url',  'sortable': False},
                {'header': 'First Seen', 'field': 'first_seen', 'type': 'text', 'sortable': True},
            ],
            'rows': visited_rows,
        },
        {
            'key': 'rankedjob',
            'label': 'Ranked Jobs',
            'columns': [
                {'header': 'ID',        'field': 'id',           'type': 'text',    'sortable': False},
                {'header': 'Title',     'field': 'job_title',    'type': 'wrap',    'sortable': True},
                {'header': 'Employer',  'field': 'job_employer', 'type': 'wrap',    'sortable': False},
                {'header': 'Snippet',   'field': 'job_snippet',  'type': 'snippet', 'sortable': False},
                {'header': 'Score',     'field': 'score',        'type': 'text',    'sortable': True},
                {'header': 'Scored At', 'field': 'scored_at',    'type': 'text',    'sortable': True},
                {'header': 'URL',       'field': 'job_url',      'type': 'url',     'sortable': False},
            ],
            'rows': ranked_rows,
        },
    ]

    for table in tables:
        cols = table['columns']
        table['col_meta'] = [{'header': c['header'], 'sortable': c.get('sortable', False)} for c in cols]
        table['shaped_rows'] = [
            {
                'pk': row['id'],
                'cells': [{'value': row[c['field']], 'type': c['type']} for c in cols],
            }
            for row in table['rows']
        ]

    return render(request, 'jobs/table_browser.html', {'tables': tables})
