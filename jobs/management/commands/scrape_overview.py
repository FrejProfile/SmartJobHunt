import re
import json
import requests
from django.core.management.base import BaseCommand
from jobs.models import Job, Visited

def parse_markdown_list(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    return [
        line.strip().lstrip('-').split('#')[0].strip()
        for line in lines
        if line.strip().startswith('-')
    ]
def extract_employer_tracker_url(html):
    match = re.search(r'class="btn btn-sm btn-primary seejobdesktop"[^>]*href="([^"]+)"', html)
    if match:
        url = match.group(1)
        return url if url.startswith("http") else "https://www.jobindex.dk" + url
    match = re.search(r'data-click="(/c\?t=[^"]+)"', html)
    if match:
        return "https://www.jobindex.dk" + match.group(1)
    return None

def strip_html(html):
    from html.parser import HTMLParser
    class Stripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
        def handle_data(self, data):
            self.text.append(data)
    p = Stripper()
    p.feed(html)
    return re.sub(r'\s+', ' ', ' '.join(p.text)).strip()

def fetch_page(session, query, page):
    r = session.get(
        "https://www.jobindex.dk/jobsoegning",
        params={"q": query, "page": page, "lang": "da"},
    )
    match = re.search(r'var Stash = ({.*?});\s*\n', r.text, re.DOTALL)
    stash = json.loads(match.group(1))
    store = stash["jobsearch/result_app"]["storeData"]
    response = store["searchResponse"]
    return response

class Command(BaseCommand):
    help = "Scrape Jobindex overview and store new jobs in the database"

    def add_arguments(self, parser):
        parser.add_argument('--search-words', default='scripts/search_words.md')
        parser.add_argument('--filters', default='scripts/filters.md')
        parser.add_argument('--verbose', action='store_true', help='Print filtered out jobs to CLI')

    def handle(self, *args, **options):
        search_words = parse_markdown_list(options['search_words'])
        blacklist    = parse_markdown_list(options['filters'])

        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        query = " ".join(search_words)
        self.stdout.write(f"Query: '{query}'")
        self.stdout.write(f"Blacklist: {blacklist}")

        # Compile blacklist into single regex pattern
        blacklist_pattern = re.compile(
            '|'.join(re.escape(word) for word in blacklist),
            re.IGNORECASE
        )

        new_count      = 0
        filtered_count = 0
        visited_count  = 0
        page           = 1

        while True:
            self.stdout.write(f"  Page {page}...")
            response = fetch_page(session, query, page)

            if not response["results"]:
                self.stdout.write("  No results, stopping.")
                break

            for job in response["results"]:
                card_html = job.get("html", "")
                title     = job.get("headline", "")
                company   = job.get("companytext") or ""
                tracker   = extract_employer_tracker_url(card_html)
                url       = job.get("share_url") or tracker

                if not url:
                    continue

                # Always record as visited
                if Visited.objects.filter(url=url).exists():
                    visited_count += 1
                    continue

                visited = Visited.objects.create(url=url)

                # Apply blacklist filter
                if blacklist_pattern.search(title):
                    filtered_count += 1
                    if options['verbose']:
                        self.stdout.write(f"  [FILTERED] {title} | {company}")
                    continue

                # Create job for survivors
                Job.objects.create(
                    visited  = visited,
                    employer = company,
                    title    = title,
                    snippet  = strip_html(card_html)[:400],
                    employer_url = tracker or "",
                )
                new_count += 1

            if page >= response["max_page"]:
                break
            page += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {new_count} new jobs added, {filtered_count} filtered out, {visited_count} already visited."
        ))