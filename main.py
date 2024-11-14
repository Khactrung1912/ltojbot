import discord
from settings import *
from user import *
from problem import *
import random
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)



@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

@tree.command(
    name="identify",
    description="Xác thực tài khoản LTOJ"
)
async def identify(interaction,handle:str):
    user = await get_info_user(handle)
    if (user[0]['status']==404): 
        await interaction.response.send_message('Người dùng không tồn tại')
    else:
        list_problem = await get_list_problem()
        problem_auth = random.choice(list_problem)
        await interaction.response.send_message(f'Vui lòng nộp mã nguồn dịch lỗi ở [bài này]({site}/problem/{problem_auth}) trong vòng một phút')
        await asyncio.sleep(10)
        list_submissions = ((await get_submissons_user(handle))[0]['data'])
      
        finish = 0
        ma = 0

        for id_submission in list_submissions:
            if (int(id_submission)<int(ma)): continue
            ma=id_submission
            submission = list_submissions[id_submission]
            finish = (submission['problem']==problem_auth and submission['result']=='CE')
            
        if (finish):
            rating = await get_name_rating(user[0]['data']['contests']['current_rating'])
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=rating))
            await add_user(interaction.user.id,handle,rating)
            await interaction.edit_original_response(content=f"Xác thực tài khoản {handle} thành công")
        else: await interaction.edit_original_response(content="Xác thực thất bại")

@tree.command(
    name="createrole",
    description="Tạo role tương ứng với các rating trên OJ"
)
@commands.has_permissions(administrator=True)
async def CreateRole(interaction):
    name  = ['Newbie','Pupil','Specialist','Expert','Candidate Master','Master','GrandMaster']
    color = [discord.Color(0x999999),discord.Color(0x00a900),discord.Color(0x008B8B),discord.Color.blue(),discord.Color(0xaa00aa),discord.Color(0xff8c00),discord.Color(0xee0000)]
    await interaction.response.send_message("Đang tạo các vai trò")
    for i in range(6,-1,-1):
        role  = await interaction.guild.create_role(name=name[i], color=color[i], permissions=discord.Permissions.none(),hoist=1)
    await interaction.edit_original_response(content="Đã tạo thành công~")
@tree.command(
    name="update_rating",
    description="Cập nhật rating cho các người dùng"
)
@commands.has_permissions(administrator=True)
async def update_rating(interaction):
    list_users = await get_list_user()
    for user in list_users:
        member_discord = await interaction.guild.fetch_member(user[0])
        rating = await get_name_rating(await get_rating(user[1]))
        await member_discord.remove_roles(discord.utils.get(interaction.guild.roles, name=user[2]))
        await member_discord.add_roles(discord.utils.get(interaction.guild.roles, name=rating))
        await edit_user(user[0],"rating",rating)
    await interaction.response.send_message("Đã cập nhật thành công")
client.run(token)