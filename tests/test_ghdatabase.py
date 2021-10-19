from ghtesting.ghdatabase import GHDatabase
import logging as log

def test_repos_count():
    # basically test that the repo is accessible
    db = GHDatabase()
    count = db.repos_count()
    log.warning(f'repo count: {count}')
    assert count >= 0
