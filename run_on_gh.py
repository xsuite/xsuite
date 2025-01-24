"""Run Xsuite tests from a CLI using GitHub Actions.

This script requires `gh` to be installed.
On macOS this can be obtained with `brew install gh`.
Afterwards it is necessary to authenticate with GitHub:

$ gh auth login

and select `xsuite/xsuite` as the default repository:

$ gh repo set-default xsuite/xsuite

Run `python run_on_gh.py --help` for usage information.
"""

import click
import json
import subprocess

ABBRV = {
    'xo': 'xobjects',
    'xd': 'xdeps',
    'xp': 'xpart',
    'xt': 'xtrack',
    'xf': 'xfields',
    'xm': 'xmask',
    'xc': 'xcoll',
    'xw': 'xwakes',
}

def make_flag(pkg):
    full_name = ABBRV[pkg].title()

    return click.option(
        f'--{pkg}',
        default='xsuite:main',
        help=f'{full_name} ref.',
        show_default=True,
    )

@click.command()
@make_flag('xo')
@make_flag('xd')
@make_flag('xp')
@make_flag('xt')
@make_flag('xf')
@make_flag('xm')
@make_flag('xc')
@make_flag('xw')
@click.option(
    '--platform',
    default='self-hosted',
    help='A label of the runner that should take this job.',
    show_default=True,
)
@click.option(
    '--ctx',
    default='cpu,omp,cuda,cl',
    help=(
        'Contexts on which to run tests. Comma separated '
        'list of cpu, omp, cuda, or cl with arguments '
        'passed after the colon, e.g. cpu:auto (equivalent '
        'to omp).'
    ),
    show_default=True,
)
@click.option(
    '--suites',
    default='xo,xd,xp,xt,xf,xc,xw',
    help='Test suites to run.',
    show_default=True,
)
@click.option(
    '--wf',
    default='manual_test_sh.yaml',
    help='The workflow file to use.',
    show_default=True,
)
@click.option(
    '--branch',
    default='main',
    help='The branch of the workflow.',
    show_default=True,
)
@click.option(
    '--pytest-opts',
    default='',
    help='Commandline options to pass to pytest.',
    show_default=True,
)
def run(xo, xd, xp, xt, xf, xm, xc, xw, platform, ctx, suites, wf, branch, pytest_opts):
    """Schedule a test run of Xsuite on a self-hosted runner.

    Example:

    python run_on_gh.py --suites xf,xd --platform pcbe-abp-gpu001-1 --xo xsuite:release/0.2.10 --xf xd:release/v0.5.0 --xt xsuite:release/0.46.2 --xf xsuite:release/0.14.1 --ctx cuda:3
    """
    try:
        subprocess.run(('gh', '--version'))
    except FileNotFoundError:
        print(__doc__)
        return 1

    ctx = ctx.replace('cl', 'ContextPyopencl')
    ctx = ctx.replace('cuda', 'ContextCupy')
    ctx = ctx.replace('cpu', 'ContextCpu')
    ctx = ctx.replace('omp', 'ContextCpu:auto')
    fmt_contexts = ctx.split(',')

    fmt_suites = [ABBRV[x.strip()] for x in suites.split(',')]

    parameters = {
        'locations' :json.dumps({
            'xobjects_location': xo,
            'xdeps_location': xd,
            'xpart_location': xp,
            'xtrack_location': xt,
            'xfields_location': xf,
            'xmask_location': xm,
            'xcoll_location': xc,
            'xwakes_location': xw,
        }) ,
        'pytest_options': pytest_opts,
        'test_contexts': ';'.join(fmt_contexts),
        'platform': platform,
        'suites': json.dumps(fmt_suites),
    }

    print('Scheduling')
    print(json.dumps(parameters, indent=2))

    workflow_command = f'gh workflow run {wf} --json --ref {branch}'

    res = subprocess.run(
        workflow_command.split(),
        input=json.dumps(parameters).encode(),
    )
    res.check_returncode()


if __name__ == '__main__':
    run()
