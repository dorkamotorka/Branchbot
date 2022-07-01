import os
import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from datetime import datetime, date

router = routing.Router()
routes = web.RouteTableDef()

USER = "tp4348"
REPOSITORY = "DemoPrivateRepository"

@routes.post("/")
async def main(request):
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, USER, oauth_token=os.getenv("GH_AUTH"))
        branches = await gh.getitem(f'/repos/{USER}/{REPOSITORY}/branches')
        '''
        # For each branch
        for b in branches:
            name = b['name']
            branch = await gh.getitem(f'/repos/{USER}/{REPOSITORY}/branches/{name}')
            timedate = branch['commit']['commit']['author']['date']
            dateoflastcommit,_  = timedate.split("T")
            today = str(date.today())
            dateoflastcommit = datetime.strptime(dateoflastcommit, "%Y-%m-%d")
            today = datetime.strptime(today, "%Y-%m-%d")
            delta = today - dateoflastcommit
            if (delta.days > 1) and name != 'main':
                deletion = await gh.delete(f'/repos/{USER}/{REPOSITORY}/git/refs/heads/{name}')
                print(f"Delete branch {name} in repository {REPOSITORY}. {user} made me do it, I'm sorry :(")
            else:
                print("I was called, but I didn't do shiet")
        '''

    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
