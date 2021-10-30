from ghtesting.ghquery import GHQuery
import json
import os
import logging as log

daterange = "2021-01-01..2021-02-01"
def test_ghquery_token():
    token = '12345' #dummy token
    daterange = "2018-01-01..2020-01-01"
    searchparam = {
        'created': daterange
    }
    ghq = GHQuery(searchparam, token)
    assert ghq.token == token

def test_env_var_tokens_defined():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    log.info("GITHUB_TOKENS environment variable must be set.")
    assert len(tokens) >= 1

def test_run_query_repos():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    daterange = "2010-01-01..2011-01-01"
    searchparam = {
        'created': daterange,
        'stars': '>1000'
    }
    ghq = GHQuery(searchparam, tokens[0])
    ret, jdata = ghq.run_query()
    log.warning(jdata)

    # query should succeed
    assert ret == 200

    # query should find 100 repos
    assert len(jdata['data']['search']['edges']) == 100

    # query should have multiple pages
    assert ghq.endCursor != None

    # query should have found so many repos
    assert jdata['data']['search']['repositoryCount'] == 878
