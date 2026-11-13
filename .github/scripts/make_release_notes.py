# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2026.                 #
# ######################################### #
"""Collate sub-package release notes into release notes for an xsuite tag.

Compares the pinned dependency versions in ``pyproject.toml`` at the given tag
against the previous release tag, and for every updated package gathers the
GitHub release pages of all versions published in between.

Usage:

    python .github/scripts/make_release_notes.py v0.67.2 > notes.md

Requires ``git``, ``gh`` (authenticated, or with GH_TOKEN set) and the
``packaging`` Python package.
"""
import json
import re
import subprocess
import sys
import tomllib
import urllib.request

from packaging.requirements import Requirement
from packaging.version import Version

RELEASE_TAG_RE = re.compile(r'^v\d+\.\d+\.\d+$')


def run(*cmd):
    return subprocess.run(
        cmd, check=True, capture_output=True, text=True,
    ).stdout


def previous_release_tag(tag):
    current = Version(tag)
    candidates = [
        t for t in run('git', 'tag', '--list', 'v*').split()
        if RELEASE_TAG_RE.match(t) and Version(t) < current
    ]
    if not candidates:
        raise RuntimeError(f'No release tag found before {tag}.')
    return max(candidates, key=Version)


def pinned_versions(tag):
    pyproject = tomllib.loads(run('git', 'show', f'{tag}:pyproject.toml'))
    pins = {}
    for dep in pyproject['project']['dependencies']:
        req = Requirement(dep)
        specs = list(req.specifier)
        if len(specs) == 1 and specs[0].operator == '==':
            pins[req.name] = Version(specs[0].version)
    return pins


def pypi_versions(package):
    url = f'https://pypi.org/pypi/{package}/json'
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    versions = []
    for version, files in data['releases'].items():
        if not files or all(f.get('yanked') for f in files):
            continue
        parsed = Version(version)
        if not parsed.is_prerelease:
            versions.append(parsed)
    return sorted(versions)


def github_releases(package):
    """Map of version -> release for published (non-draft) GitHub releases."""
    pages = run(
        'gh', 'api', '--paginate', '--slurp',
        f'/repos/xsuite/{package}/releases?per_page=100',
    )
    releases = {}
    for page in json.loads(pages):
        for release in page:
            if release['draft']:
                continue
            try:
                version = Version(release['tag_name'].lstrip('v'))
            except ValueError:
                continue
            releases[version] = release
    return releases


def package_section(package, old, new):
    repo_url = f'https://github.com/xsuite/{package}'
    lines = [f'## {package} {old} → {new}', '']

    in_range = [v for v in pypi_versions(package) if old < v <= new]
    if new not in in_range:
        # Should not happen if the pin is valid, but do not lose the entry
        in_range.append(new)

    releases = github_releases(package)
    for version in reversed(in_range):
        release = releases.get(version)
        if release is None:
            lines += [
                f'### {package} v{version}',
                '',
                f'> [!WARNING]',
                f'> No release notes found for {package} v{version}. '
                f'See the [changes since the previous version]'
                f'({repo_url}/compare/{_previous(in_range, version, old)}'
                f'...v{version}).',
                '',
            ]
            continue

        title = release['name'] or f'{package} v{version}'
        body = (release['body'] or '').replace('\r\n', '\n').strip()
        lines += [f'### [{title}]({release["html_url"]})', '']
        lines += [body or '_No description provided._', '']

    return lines


def _previous(versions, version, fallback):
    earlier = [v for v in versions if v < version]
    return f'v{max(earlier) if earlier else fallback}'


def make_release_notes(tag):
    if not RELEASE_TAG_RE.match(tag):
        raise RuntimeError(f'{tag} is not a release tag of the form vX.Y.Z.')

    previous_tag = previous_release_tag(tag)
    old_pins = pinned_versions(previous_tag)
    new_pins = pinned_versions(tag)

    changed = {
        pkg: (old_pins.get(pkg), new)
        for pkg, new in new_pins.items()
        if old_pins.get(pkg) != new
    }

    lines = [
        f'Install with `pip install xsuite=={tag.lstrip("v")}`.',
        '',
        '| Package | Previous | This release |',
        '|---|---|---|',
    ]
    for pkg, new in sorted(new_pins.items()):
        old = old_pins.get(pkg)
        if pkg in changed:
            lines.append(f'| **{pkg}** | {old or "—"} | **{new}** |')
        else:
            lines.append(f'| {pkg} | {old} | {new} |')
    lines.append('')

    if not changed:
        lines += ['No sub-package versions changed in this release.', '']

    for pkg, (old, new) in sorted(changed.items()):
        if old is None:
            lines += [f'## {pkg} {new}', '', f'Newly added dependency.', '']
        elif new < old:
            lines += [f'## {pkg} {old} → {new}', '', 'Downgraded.', '']
        else:
            lines += package_section(pkg, old, new)

    lines += [
        '---',
        '',
        f'**Full xsuite changes**: https://github.com/xsuite/xsuite/compare/'
        f'{previous_tag}...{tag}',
    ]
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f'Usage: {sys.argv[0]} vX.Y.Z')
    sys.stdout.write(make_release_notes(sys.argv[1]))
