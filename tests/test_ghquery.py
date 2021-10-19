from ghtesting.ghquery import GHQuery, QueryRepos
import json
import os
import logging as log

daterange = "2021-01-01..2021-02-01"
def test_ghquery_token():
    token = '12345' #dummy token
    daterange = "2018-01-01..2020-01-01"
    ghq = GHQuery(daterange, token)
    assert ghq.token == token

def test_env_var_tokens_defined():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    assert len(tokens) >= 1

def test_run_query_repos():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    daterange = "2018-01-01..2020-01-01"
    ghq = GHQuery(daterange, tokens[0])
    ret, jdata = ghq.run_query()
    log.warning(jdata)
    # query should succeed
    assert ret == 200
    # query should find 100 repos
    assert len(jdata['data']['search']['edges']) == 100
    assert ghq.endCursor != None
