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

ghq = GHQuery(tokens[0])

seen_repos = {}

log.info('Beginning to query GitHub repositories...')
ret, jsondata = ghq.run_query()
while ret == 200:
    rateLimit = jsondata['data']['rateLimit']
    hasNextPage = jsondata['data']['search']['pageInfo']['hasNextPage']
    log.info(f'Rate: {rateLimit["remaining"]}/{rateLimit["limit"]} NodeCount: {rateLimit["nodeCount"]}, ResetsAt: {rateLimit["resetAt"]}')
    log.info(f'hasNextPage: {hasNextPage}')

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
    ret, jsondata = ghq.run_query()

exit()
