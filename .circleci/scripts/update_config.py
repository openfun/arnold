#!/usr/bin/env python3

import os
import re
import subprocess
import textwrap
import yaml


CI_PATH = '.circleci'
CI_ROOT = CI_PATH + '/templates'
CI_CONFIG = CI_PATH + '/config.yml'
APPS_ROOT = 'apps'
ROOT_FILES = [  # If any of those file/folder content changed, build all known jobs
    'env.d/',
    'filter_plugins/',
    'group_vars/',
    'lookup_plugins/',
    'tasks/',
    'templates/',
    'tests/',
    # + any file that is root
]
IGNORE_FILES = [  # Changes in those file don't trigger a global rebuilt
    'CHANGELOG.md',
    'CODE_OF_CONDUCT.md',
    'CONTRIBUTING.md',
    'LICENSE',
    'README.md',
    'VERSION',
]

# List all known jobs in .circleci/templates folders
known_jobs = set([d for d in os.listdir(CI_ROOT) if os.path.isdir('{}/{}'.format(CI_ROOT, d))])
# List all apps in apps/
apps = set(['test-bootstrap-{}'.format(d) for d in os.listdir(APPS_ROOT)])
# List all changes compare to master
what_changed = set([line.decode('UTF-8') for line in subprocess.check_output([
        'git',
        'whatchanged',
        '--name-only',
        '--pretty=',
        'origin/master..HEAD']).split()
    ]
)

# Set to contain all the jobs to do
required_jobs = set()

# Check what file were changed.
# If they are in the "ROO_FILES" list, then all the job must be started
# Else, only add job for apps/
for change in what_changed:
    # Test if the change address a "global" folder
    for path in ROOT_FILES:
        if change.startswith(path):
            required_jobs |= known_jobs
            break  # No need to keep checking, everything is here already
    # If we changed any root file
    if ('/' not in change) and (change not in IGNORE_FILES):
        required_jobs |= known_jobs
        break  # No need to keep checking, everything is here already
    # We have changed an app
    if change.startswith('apps/'):
        app = 'test-bootstrap-{}'.format(change.split('/')[1])
        if app in known_jobs:
            required_jobs.add(app)

# Remove apps from known_jobs and then add required_jobs
jobs_to_run = (known_jobs - apps) | required_jobs

# Get the current branch and tag to check jobs filters
current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']) \
                           .strip() \
                           .decode('UTF-8')
current_tag = subprocess.check_output(['git', 'tag', '--points-at', 'HEAD']) \
                        .strip() \
                        .decode('UTF-8')

# Go through all required jobs to find dependencies
for job in jobs_to_run:
    # Load this job workflow details...
    config = yaml.load(open('{}/{}/workflow.yml'.format(CI_ROOT, job)), Loader=yaml.FullLoader)
    # ... to check its filter
    if 'filters' in config[0][job]:
        # Skip this job and its requirement if the current branch is not targeted
        if 'branches' in config[0][job]['filters']:
            if 'only' in config[0][job]['filters']['branches'] and \
               config[0][job]['filters']['branches']['only'] != current_branch:
                continue
            if 'ignores' in config[0][job]['filters']['branches'] and \
               config[0][job]['filters']['branches']['ignores'] == current_branch:
                continue
        # Skip this job and its requirement if the current tag is not targeted
        if 'tags' in config[0][job]['filters'] and current_tag:
            if 'only' in config[0][job]['filters']['tags']:
                pattern = config[0][job]['filters']['tags']['only'][1:-1]
                if not re.match(pattern, current_tag):
                    continue
            if 'ignore' in config[0][job]['filters']['tags']:
                pattern = config[0][job]['filters']['tags']['ignore'][1:-1]
                if re.match(pattern, current_tag):
                    continue
    # If the job was not skipped, then add it and add its requirements
    required_jobs.add(job)
    # All all the "required" job to the list
    if 'requires' in config[0][job]:
        for req in config[0][job]['requires']:
            required_jobs.add(req)

# Build the output for the job part and the workflow part of the config.yml
jobs_output = '\n'.join(
    [open('{}/{}/job.yml'.format(CI_ROOT, f)).read() for f in required_jobs]
)
workflow_jobs_output = '\n'.join(
    [open('{}/{}/workflow.yml'.format(CI_ROOT, f)).read() for f in required_jobs]
)

jobs_output = textwrap.indent(jobs_output, ' ' * 4)
workflow_jobs_output = textwrap.indent(workflow_jobs_output, ' ' * 6)

# Build the final config.yml file
output = ''
with open('{}/main.yml.tpl'.format(CI_ROOT), 'r') as template:
    output = template.read() \
                     .replace(r'{{ jobs }}', jobs_output) \
                     .replace(r'{{ workflow_jobs }}', workflow_jobs_output)

if not output:
    print('Error while generating output')

with open(CI_CONFIG, 'w') as config:
    config.write('#####################################\n')
    config.write('##   THIS FILE IS AUTO-GENERATED   ##\n')
    config.write('##  Run bin/update to generate it  ##\n')
    config.write('#####################################\n')
    config.write('\n')
    config.write(output)
