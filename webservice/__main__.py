import os
import aiohttp
from aiohttp import web
from gidgethub import aiohttp as gh_aiohttp
from datetime import datetime, date

routes = web.RouteTableDef()

@routes.post("/")
async def main(request):
    token = os.getenv("GH_AUTH")
    owner = os.getenv("OWNER")
    repo = os.getenv("REPOSITORY")
    master = os.getenv("MASTER_BRANCH")

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, owner, oauth_token=token)
        branches = await gh.getitem(f'/repos/{owner}/{repo}/branches')
        # For each branch
        for b in branches:
            name = b['name']
            branch = await gh.getitem(f'/repos/{owner}/{repo}/branches/{name}')
            timedate = branch['commit']['commit']['author']['date']
            dateoflastcommit,_  = timedate.split("T")
            today = str(date.today())
            dateoflastcommit = datetime.strptime(dateoflastcommit, "%Y-%m-%d")
            today = datetime.strptime(today, "%Y-%m-%d")
            delta = today - dateoflastcommit
            if (delta.days > 60) and name != master:
                deletion = await gh.delete(f'/repos/{owner}/{repo}/git/refs/heads/{name}')
                print(f"Delete branch {name} in repository {repo}. tp4348 made me do it, I'm sorry :(")
            elif name == master:
                print("I don't delete master branch. I just don't :)")
            else:
                print(f"I was called, but I didn't do shiet since {name} is only {delta.days} days old.")

    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.getenv("PORT")
    web.run_app(app, port=int(port))
