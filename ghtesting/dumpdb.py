#!/usr/bin/env python3

from ghdatabase import GHDatabase
from ghrepo import GHRepo

db = GHDatabase('github', 'webframework_repos')

for topic in ['react', 'vue', 'angular']:
    with open(topic+'.csv', 'w') as fh:
        fh.write('name,url,primarylanguage\n')
        for repojson in db.get_repos():
            repo = GHRepo(repojson)
            if topic in repo.topics:
                fh.write(','.join([repo.name, repo.url, repo.primarylanguage]) + '\n')
