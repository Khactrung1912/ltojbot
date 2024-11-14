import aiohttp
from settings import *

async def get_list_problem():
    async with aiohttp.ClientSession() as session:  
        async with session.get(f"{site}/api/problem/list") as response:  
            list_problem = []
            for problem in await response.json(): 
                list_problem.append(problem)
            return list_problem  

