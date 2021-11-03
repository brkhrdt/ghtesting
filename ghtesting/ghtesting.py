#!/usr/bin/env python3

from ghquery import GHQuery
from ghdatabase import GHDatabase
import datetime
import os
import logging as log
log.basicConfig(
    format='%(asctime)s %(levelname)-5s  | %(message)s  (%(filename)s:%(lineno)d)',
    encoding='utf-8',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
log.addLevelName(log.WARNING, 'WARN')
log.addLevelName(log.FATAL, 'FATAL')

tokens = os.environ['GITHUB_TOKENS'].split(' ')

# Locally store github repo data
ghdb = GHDatabase('github', 'webframework_repos')


seen_repos = {}

log.info('Beginning to query GitHub repositories...')

dateranges = [
    "2008-01-01..2008-06-01", "2008-06-01..2009-01-01",
    "2009-01-01..2009-06-01", "2009-06-01..2010-01-01",
    "2010-01-01..2010-06-01", "2010-06-01..2011-01-01",
    "2011-01-01..2011-06-01", "2011-06-01..2012-01-01",
    "2012-01-01..2012-06-01", "2012-06-01..2013-01-01",
    "2013-01-01..2013-06-01", "2013-06-01..2014-01-01",
    "2014-01-01..2014-06-01", "2014-06-01..2015-01-01",
    "2015-01-01..2015-06-01", "2015-06-01..2016-01-01",
    "2016-01-01..2016-06-01", "2016-06-01..2017-01-01",
    "2017-01-01..2017-06-01", "2017-06-01..2018-01-01",
    "2018-01-01..2018-06-01", "2018-06-01..2019-01-01",
    "2019-01-01..2019-06-01", "2019-06-01..2020-01-01",
    "2020-01-01..2020-06-01", "2020-06-01..2021-01-01",
    "2021-01-01..2021-06-01", "2021-06-01..2022-01-01",
    ]

topics = ['angular', 'react', 'vue']

def queryRepos(search: dict):
    ghq = GHQuery(search, tokens[0])
    hasNextPage = True
    while hasNextPage:
        # if there was a cursor from previous run then it gets used inside run_query()
        ret, jsondata = ghq.run_query()
        num_repos_found = jsondata['data']['search']['repositoryCount']
        if num_repos_found > 1000:
            raise Exception("Query exceeds the maximum repos returnable in one query (1000 repos).")

        queriedAt = datetime.datetime.now().replace(microsecond=0).isoformat()+'Z'
        for reponode in jsondata['data']['search']['edges']:
            repo = reponode['node']
            reponame = repo['nameWithOwner']
            repo['_id'] = reponame
            repo['queriedAt'] = queriedAt
            seen_repos[reponame] = True
            log.debug(repo)
            log.info(f'Inserting {repo["_id"]}')
            ghdb.update_repo(repo)
        log.info(f'Total repos seen: {len(seen_repos)}')

        rateLimit = jsondata['data']['rateLimit']
        hasNextPage = jsondata['data']['search']['pageInfo']['hasNextPage']
        log.info(f'Rate: {rateLimit["remaining"]}/{rateLimit["limit"]} NodeCount: {rateLimit["nodeCount"]}, ResetsAt: {rateLimit["resetAt"]}')
        log.info(f'hasNextPage: {hasNextPage}')

for topic in topics:
    for daterange in dateranges:
        log.info(f'Querying repos within {daterange}')

        searchparams = {
            'topic': topic,
            'stars': '>100',
            'created': daterange
        }

        queryRepos(searchparams)

exit()
