"""Generate markdown changelog of Xsuite.

This script requires `gh` to be installed.
On macOS this can be obtained with `brew install gh`.
Afterwards it is necessary to authenticate with GitHub:

$ gh auth login

Then, a changelog can be generated with:

$ python make_changelog.py --start [date] --end [date]

Run `python run_on_gh.py --help` for usage information.
"""
from dateutil.parser import isoparse

import click
import json
import subprocess


PACKAGES = ['xdeps', 'xobjects', 'xpart', 'xtrack', 'xfields', 'xmask']


def fetch_package_log_page(package, page_size, page):
    command = (
        'gh', 'api',
        '-H', 'Accept: application/vnd.github+json',
        '-H', 'X-GitHub-Api-Version: 2022-11-28',
        f'/repos/xsuite/{package}/releases?per_page={page_size}&page={page}'
    )
    p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if p.stderr:
        raise RuntimeError(p.stderr)

    return json.loads(p.stdout)


def fetch_package_log(package, end):
    page = 1
    full_log = []
    while log := fetch_package_log_page(package, 100, page):
        last_publish_date = isoparse(log[-1]['published_at'])

        if end and last_publish_date > end:
            # Skip pages that are too new
            break

        full_log += log
        page += 1

    return full_log


def print_entry(entry):
    date = isoparse(entry["published_at"])
    print(f'# [{entry["name"]}]({entry["url"]})')
    print()
    print(f'Published: {date.strftime("%Y-%m-%d %H:%M")}')
    print()
    print(entry['body'])
    print()


@click.command()
@click.option('--start', '-s',
              type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--end', '-e',
              type=click.DateTime(formats=["%Y-%m-%d"]))
def make_changelog(start, end):
    if start:
        start = start.astimezone()

    if end:
        end = end.astimezone()

    joint_log = []
    for pkg in PACKAGES:
        joint_log += fetch_package_log(pkg, end)

    joint_log = sorted(joint_log, key=lambda entry: entry['published_at'])

    for entry in joint_log:
        published_at = isoparse(entry['published_at'])

        if start and published_at < start:
            continue

        if end and published_at > end:
            continue

        print_entry(entry)


if __name__ == '__main__':
    make_changelog()
