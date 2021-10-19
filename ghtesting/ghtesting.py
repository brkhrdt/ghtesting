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
ghdb = GHDatabase()


seen_repos = {}

log.info('Beginning to query GitHub repositories...')

dateranges = [] # fill in

for daterange in dateranges:
    log.info(f'Querying repos within {daterange}')

    ghq = GHQuery(daterange, tokens[0])
    hasNextPage = True
    while hasNextPage:
        # if there was a cursor from previous run then it gets used inside run_query()
        ret, jsondata = ghq.run_query()

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

exit()
