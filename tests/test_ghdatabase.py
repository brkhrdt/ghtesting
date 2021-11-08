from ghtesting.ghdatabase import GHDatabase
import logging as log

def test_repos_count():
    # basically test that the repo is accessible
    db = GHDatabase('github', 'repos')
    count = db.repos_count()
    log.warning(f'repo count: {count}')
    assert count >= 0

def test_add_data_to_repo():
    db = GHDatabase('testdb', 'repos')
    db.update_repo({'_id': 'repoabc/repoabc',
                    'data': 'abc'})
    count = db.repos_count()
    log.warning(f'repo count: {count}')
    assert count == 1

    # new data should not have been added yet
    data = db.get_repos_by_name('repoabc/repoabc')
    assert 'newdata' not in data

    # add new data
    db.append_to_repo('repoabc/repoabc', {'newdata': 'xyz'})

    # new data should exist now
    data = db.get_repos_by_name('repoabc/repoabc')
    assert 'newdata' in data

    # drop database
    db.drop_database('testdb')
    count = db.repos_count()
    log.warning(f'repo count after drop: {count}')
    assert count == 0
