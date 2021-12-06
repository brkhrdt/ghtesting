import sys
sys.path.insert(0, '../ghtesting')

import pickle
import os
import re
from collections import Counter
from git import Repo
from ghdatabase import GHDatabase
from ghrepo import GHRepo

with open('../data/final_reports.pickle', 'rb') as f:
    final_reports = pickle.load(f)

service_urls = {
    r'.*travis-ci.(?:org|com).*': 'travisci',
    r'.*img.shields.io/travis.*': 'travisci',
    r'.*circleci.com.*': 'circleci',
    r'.*img.shields.io/circleci.*': 'circleci',
    r'.*github.com/.*/workflows/.*': 'github',
    r'.*img.shields.io/github/workflow.*': 'github',
    r'.*ci.appveyor.com.*': 'appveyorci',
    r'.*img.shields.io/appveyor/ci/.*': 'appveyorci',
    r'.*saucelabs.com.*': 'saucelabs',
    r'.*dev.azure.com.*': 'azure_pipelines',
    r'.*visualstudio.com/.*/build.*': 'azure_pipelines',
    r'.*app.bitrise.io.*': 'bitrise',
    r'.*badge.buildkite.com.*': 'buildkite',
    r'.*codeship.com.*': 'codeship',
    r'.*img.shields.io/codeship/.*': 'codeship',
    r'.*gitlab.com/.*/badges/.*/pipeline.svg': 'gitlab',
    r'.*gitlab.com/.*/badges/.*/build.svg': 'gitlab',
    r'.*semaphoreci.com.*': 'semaphoreci',
    r'.*api.shippable.com.*': 'shippable',
    r'.*img.shields.io/shippable/.*': 'shippable',
    r'.*teamcity.jetbrains.com/.*/build.*': 'teamcity',
    r'.*app.wercker.com.*': 'wercker',
}
    
def get_repository_path(repo):
    return os.path.join('repositories', repo.name.split('/')[1])
    
def get_repos():
    # get list of repos
    db = GHDatabase('ecs260', 'webframework_repos', os.environ['CONNECTION_STRING'])
    repos = [GHRepo(i) for i in db.get_repos()]
    repos = [repo for repo in repos if repo.name in final_reports]
    return repos

def get_webframework(repo):
    if 'angular' in repo.topics:
        return 'Angular'
    if 'vue' in repo.topics:
        return 'Vue'
    if 'react' in repo.topics:
        return 'React'

def get_contributors_by_commit_id(git, commit_id):
    branch = git.active_branch.name
    git.git.checkout(commit_id)
    log = git.git.log()
    authors = [i.strip() for i in re.findall(r'Author: (.*)?<.*?>\n', log)]
    git.git.checkout(branch)
    return Counter(authors)
    
def get_contributors(repo, report):
    git = Repo(get_repository_path(repo))
    return get_contributors_by_commit_id(git, report['commitid'])

def get_branch(repo):
    return Repo(get_repository_path(repo)).active_branch.name

def get_reports(repo):
    # get reports only for the main branch
    main_branch = get_branch(repo)
    main_reports = [r for r in repo.codecov_reports if r['branch'] == main_branch]
        
    # sort by timestamp
    strptime = lambda x : datetime.strptime(x['timestamp'].split('.')[0], '%Y-%m-%d %H:%M:%S')
    return sorted(main_reports, key=strptime)

def get_earliest_report(repo):
    return final_reports[repo.name]['earliest']

def get_latest_report(repo):
    return final_reports[repo.name]['latest']

def get_metrics(report):
    metric_map = dict(
        coverage = 'c',
        files = 'f',
        lines = 'n',
        hits = 'h',
        missed = 'm',
        partials = 'p',
        branches = 'b',
        messages = 'M',
        sessions = 's'
    )
    totals = report['totals']
    metrics = {}
    for k, v in metric_map.items():
        metrics[k] = totals[v]
    return metrics