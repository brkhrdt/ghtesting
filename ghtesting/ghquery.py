import json
import requests
import time
import logging as log

class GHQueryResponse:
    def __init__(self, response):
        self.response = response

class QueryRepos:
    def __init__(self):
        pass

    @staticmethod
    def build_query(endCursor=None) -> str:
        '''
        Search for repos with >100 stars
        Retuns max repos and cursor to continue search
        '''
        searchstr = 'query: "stars:>100", type: REPOSITORY, first: 100'
        if endCursor != None:
            log.debug(f"Using endCursor {endCursor}")
            searchstr = f'query: "stars:>100", type: REPOSITORY, first: 100, after:"{endCursor}"'

        # Insert searchstr into query
        query_repos_str = '''
        {
        rateLimit {
            limit
            cost
            remaining
            nodeCount
            resetAt
        }
        search(%s) {
            repositoryCount
            pageInfo {
            startCursor
            hasNextPage
            endCursor
            }
            edges {
            node {
                ... on Repository {
                nameWithOwner
                url
                description
                createdAt
                updatedAt
                isFork
                parent {
                    id
                }
                isMirror
                stargazers {
                    totalCount
                }
                languages(first: 100) {
                    edges {
                    node {
                        name
                    }
                    size
                    }
                    totalSize
                }
                repositoryTopics(first: 100) {
                    edges {
                    node {
                        topic {
                        name
                        }
                    }
                    }
                }
                object(expression: "HEAD:") {
                    ... on Tree {
                    entries {
                        name
                        type
                    }
                    }
                }
                }
            }
            }
        }
        }
        ''' % searchstr
        log.debug(f"Query to be run: {query_repos_str}")
        return query_repos_str


class GHQuery:
    def __init__(self, token, endCursor=None):
       self.token = token
       self.headers = {"Authorization": "bearer {}".format(self.token)}
       self.api = 'https://api.github.com/graphql'
       self.endCursor = endCursor# pagination, start next query on next page

    def run_query(self):
        gql = QueryRepos.build_query(self.endCursor)
        if self.endCursor:
            log.info(f'Query from cursor "{self.endCursor}"')
        else:
            log.info("Query from beginning (no cursor)")

        # response = requests.post(self.api, json={'query': gql}, headers=self.headers)

        response = None
        retries = 0
        while response is None or response.status_code != 200:
            try:
                response = requests.post(self.api, json={'query': gql}, headers=self.headers)
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


        # retries = 1
        # while response.status_code == 502:
        #     sleeptime = retries * 2
        #     time.sleep(sleeptime)
        #     log.warning(f"Query failed (code 502). Sleeping {sleeptime} sec and retrying... (retry {retries})")
        #     retries = retries + 1
        #     response = requests.post(self.api, json={'query': gql}, headers=self.headers)

        # Code 200 is success
        # if response.status_code != 200:
        #     raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, gql))

        log.info("Query successful.")
        jsondata = response.json()
        # Update cursor to start next query here
        self.endCursor = jsondata['data']['search']['pageInfo']['endCursor']
        return (response.status_code, jsondata)
