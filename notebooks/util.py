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

def get_contributors(repo, report):
    git = Repo(get_repository_path(repo))
    branch = git.active_branch.name
    print(report['commitid'])
    git.git.checkout(report['commitid'])
    log = git.git.log()
    authors = [i.strip() for i in re.findall(r'Author: (.*)?<.*?>\n', log)]
    git.git.checkout(branch)
    return Counter(authors)

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