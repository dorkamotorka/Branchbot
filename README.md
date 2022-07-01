# Branchbot

GitHub bot to delete unactive branches after 2 months of no commit. As a backbone it uses **gidgethub** library that interacts with [GitHub REST API](https://docs.github.com/en/rest).

I have deployed it on Heroku and ran it on one of my private repositories to test it. 

The downside of this bot is that the GitHub REST API doesn't exposes the branch creation time, consequently if you create a new branch 
from e.g. master branch whose last commit is older than 2 months, your branch would get immediatelly deleted in case you don't do that locally and
push a new branch to the remote with a fresh commit.

## Trigger

Bot get's triggered on every new branch creation.
