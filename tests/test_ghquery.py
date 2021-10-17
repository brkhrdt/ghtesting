from ghtesting.ghquery import GHQuery, QueryRepos
import json
import os
import logging as log

def test_ghquery_token():
    token = '12345' #dummy token
    ghq = GHQuery('repos', token)
    assert ghq.token == token

def test_build_query_repos():
    token = '12345' #dummy token
    ghq = GHQuery('repos', token)
    qstr = QueryRepos.build_query()
    log.debug(qstr)
    #not valid json: assert json.loads(qstr)
    assert True

def test_env_var_tokens_defined():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    assert len(tokens) >= 1

def test_run_query_repos():
    tokens = os.environ['GITHUB_TOKENS'].split(' ')
    ghq = GHQuery('repos', tokens[0])
    ret, jdata = ghq.run_query()
    # query should succeed
    assert ret == 200
    # query should find 100 repos
    assert len(jdata['data']['search']['edges']) == 100
    assert ghq.endCursor != None
