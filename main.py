import os
import asyncio
import aiohttp
from gidgethub.aiohttp import GitHubAPI
from datetime import datetime, date

USER = "tp4348"
REPOSITORY = "Branchbot"

async def main():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, USER, oauth_token=os.getenv("GH_TOKEN"))
        print(dir(gh))
        branches = await gh.getitem(f'/repos/{USER}/{REPOSITORY}/branches')
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
            if (delta.days > 60) and name != 'main':
                deletion = await gh.delete(f'/repos/{USER}/{REPOSITORY}/git/refs/heads/{name}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
