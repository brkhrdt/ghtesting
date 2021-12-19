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

### Connecting to database
Run the following in your terminal before starting a jupyter notebook

```sh
export CONNECTION_STRING="<connectionString>"
```

## Running the Query

Main script is in `./ghtesting/ghtesting.py`.
All the data requested from github is hardcoded in a graphql query file: `ghtesting/queries/github/repos.graphql`
The repos obtained are determined by the search parameters that are provided to this query in the form of graphql variables.

### Building GraphQL queries for GitHub

Using the explorer to build and test queries is helpful: <https://docs.github.com/en/graphql/overview/explorer>


## Getting data from the local database

The `GHRepo` class defines some functions to extract features from the json but not all features are coded right now.
The script `./ghtesting/dumpdb.py` is an example of iterating through all the repos in the database.


## Determining CI services used by project

It would take too long to interact and authenticate with all the different CI services, so instead we just look at the badges on the README.
Most services allow you to copy the badge markdown/html to paste into your README, so we think most people who take the time to setup CI will probably take this small step to add the badge.

The `./ghtesting/scrape_ci_badges.py` uses the Python requests and BeautifulSoup packages to scrape the README section of the GitHub page for each project.
It specifically grabs all the img tags, regardless of whether or not the element is actually one of the badges.
After obtaining all the images, the URLs were incrementally analyzed to filter out the badges and the regexes for the URLs were added to GHRepo.

## Notebooks

Using Jupyter Notebook to analyze the data.

``` sh
pip install jupyter
pip install matplotlib
pip install pandas
pip install matplotlib-venn #for one plot
```

`

## Testing
Set environment variable with Github API tokens (generated in your profile) and then run pytest.
``` sh
# Only need 1 token
export GITHUB_TOKENS="token1 token2"
pytest
```

