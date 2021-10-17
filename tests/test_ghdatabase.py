from ghtesting.ghdatabase import GHDatabase
import logging as log

def test_repos_count():
    db = GHDatabase()
    count = db.repos_count()
    log.warn(f'repo count: {count}')
    assert count >= 0
    assert False
