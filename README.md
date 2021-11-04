[![Python application](https://github.com/brkhrdt/testing-on-github/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/brkhrdt/testing-on-github/actions/workflows/ci.yml)

# Testing on GitHub

## MongoDB
Saving data exactly as obtained from GitHub for later use.
We can use MongoDB to just immediately save the JSON document from the query as-is.
Start server:

``` sh
mongod --noauth --dbpath $PWD/mongo/data/db
```

GUI to view database: `mongodb-compass`


### Database Dumping and Restore

Dump:
``` sh
mongodump --db DataBaseName
```

Restore:
``` sh
# Copy json and bson files to /path/to/databasename
mongorestore --db DataBaseName /path/to/DataBaseName
```

[Source](   https://stackoverflow.com/questions/7232461/how-can-i-transfer-a-mongodb-database-to-another-machine-that-cannot-see-the-fir)


## Running the Query

Main script is in `./ghtesting/ghtesting.py`.
All the data requested from github is hardcoded in a graphql query file: `ghtesting/queries/github/repos.graphql`
The repos obtained are determined by the search parameters that are provided to this query in the form of graphql variables.


## Getting data from the local database

The `GHRepo` class defines some functions to extract features from the json but not all features are coded right now.
The script `./ghtesting/dumpdb.py` is an example of iterating through all the repos in the database.


## Testing
Set environment variable with Github API tokens (generated in your profile) and then run pytest.
``` sh
# Only need 1 token
export GITHUB_TOKENS="token1 token2"
pytest
```

