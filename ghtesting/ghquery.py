import os
import json
import requests
import time
import logging as log

class GHQuery:
    def __init__(self, searchparams: dict, token: str, endCursor: str=None):
       self.token = token
       self.headers = {"Authorization": "bearer {}".format(self.token)}
       self.api = 'https://api.github.com/graphql'

       # Graphql pagination, start next query where last query left off
       self.endCursor = endCursor

       # Stringify search parameters to insert into graphql variable
       self.searchparams = ''.join([f'{k}:{v} ' for k, v in searchparams.items()])
       log.info(f'Search query: {self.searchparams}')

    def run_query(self):

        # Read graphql query from file
        with open(os.path.join(os.path.dirname(__file__),
                               "queries/github/repos2.graphql")) as gqlfile:
            gql = gqlfile.read()
            log.debug(f'Read github repos graphql query:\n{gql}\n')

        gqlvars = {}
        if self.endCursor:
            log.info(f'Query from cursor "{self.endCursor}"')
            gqlvars['after'] = self.endCursor
        else:
            log.info("Query from beginning (no cursor)")

        # Search parameters, e.g. topics, number of stars
        gqlvars['search'] = self.searchparams

        response = None
        retries = 0
        while response is None or response.status_code != 200:
            try:
                response = requests.post(self.api, json={'query': gql, 'variables': gqlvars}, headers=self.headers)
            except:
                # 502 is random issue, keep trying and sleep between tries
                try:
                    code = response.status_code
                except:
                    code = '???'

                retries = retries + 1
                sleeptime = retries * 2
                log.warning(f'Query failed (code {code}). Sleeping {sleeptime} sec and retrying... (retry {retries})')
                time.sleep(sleeptime)

        log.info("Query successful.")
        jsondata = response.json()
        # Update cursor to start next query here
        self.endCursor = jsondata['data']['search']['pageInfo']['endCursor']
        return (response.status_code, jsondata)
