import aiohttp
from settings import *
import mysql.connector

async def get_info_user(handle):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{site}/api/user/info/{handle}") as response:
            if response.status == 404:
                return [{'status': 404}]
            else:
                data = await response.json()
                return [{'status': 200, 'data': data}]

async def get_submissons_user(handle):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{site}/api/user/submissions/{handle}") as response:
            if response.status == 404:
                return [{'status': 404}]
            else:
                return [{'status': 200, 'data': await response.json()}]

async def get_name_rating(rating):
    if (rating>=2400): return "GrandMaster"
    elif (rating>=2100): return "Master"
    elif (rating>=1900): return "Candidate Master"
    elif (rating>=1700): return "Expert"
    elif (rating>=1400): return "Specialist"
    elif (rating>=1000): return "Pupil"
    else: return "Newbie"

async def add_user(id_discord,handle,rating):
    conn = mysql.connector.connect(
        host=host_db,        
        user=user_db,             
        password=password_db, 
        database=name_db,   
    )
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (id_discord, handle,rating) VALUES (%s, %s,%s)"
    cursor.execute(insert_query, (id_discord, handle,rating))
    conn.commit()
    cursor.close()
    conn.close()

async def get_list_user():
    conn = mysql.connector.connect(
        host=host_db,        
        user=user_db,             
        password=password_db, 
        database=name_db,   
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
async def edit_user(id_discord,column,data):
    conn = mysql.connector.connect(
        host=host_db,        
        user=user_db,             
        password=password_db, 
        database=name_db,   
    )
    cursor = conn.cursor()
    command = f"""
        UPDATE users 
        SET {column}=\"{str(data)}\"
        WHERE id_discord=\"{str(id_discord)}\"
    """
    cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()
async def get_rating(handle):
    user = await get_info_user(handle)
    return (user[0]['data']['contests']['current_rating'])