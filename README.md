[![Python application](https://github.com/brkhrdt/testing-on-github/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/brkhrdt/testing-on-github/actions/workflows/ci.yml)

# Testing on GitHub

## MongoDB
Save data obtained from GitHub locally for later use.
We can use MongoDB to just immediately save the JSON document from the query as-is.
Start server:

``` sh
mongod --noauth --dbpath $PWD/mongo/data/db
```

GUI to view database: `mongodb-compass`

## Testing
Set environment variable with Github API tokens and then run pytest.
``` sh
export GITHUB_TOKENS="token1 token2"
pytest
```

