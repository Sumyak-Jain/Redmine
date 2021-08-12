import json
import embeds
import os
import datetime
import discord
import requests
import redmine_api
from discord.ext import commands
from discord.ext.tasks import loop
import discord
from discord import client
from discord.ext import commands
import function
from urllib import parse, request
from discord.ext import commands
from discord.utils import get




logger = embeds.Logger("kourage-operations")

bot = commands.Bot(command_prefix="~")

## Change the webpage accordingly.
webpage = "https://kore.koders.in/"
#webpage="http://sumyak.m.redmine.org/"


hdr1 = {'X-Redmine-API-Key' : os.environ.get('REDMINE_KEY'),
        'Content-Type': 'application/json'}


@bot.event
async def on_ready():
    logger.info("Kourage is running at version {0}".format("0.1.0"))



@bot.command()
async def show_issues(ctx):
    logger.info("~show_issues called by "+str(ctx.author.name))
    await ctx.channel.purge(limit = 1)

    project_dict,project_list,project_id=function.project_list()
    
    if(str(ctx.channel.name) in project_dict.values()): 
        project_name=str(ctx.channel.name)
        logger.info("~show_issues called from same channel as project name")  
          
    else:
     logger.info("~show_issues called from another channel")
     initial_embed=embeds.simple_embed(title="This is the current list of project", description=project_list)
     initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
     message  = await ctx.send(embed = initial_embed,delete_after=60)


     due_embed=discord.Embed(title="Enter the s.no of the project of which you want to see issues", description="Please just give a number only eg: 1",colour=0x11806a)
     message=await ctx.send(embed=due_embed,delete_after=70)
     project_number = await embeds.ctx_input(ctx, bot, message)
     if not project_number:
        return

     project_name=str(project_dict[int(project_number)])
     
     
    logger.info("project name is: "+str(project_name))
    response=function.issues(project_name)
    due_embed=embeds.simple_embed(title="List of issues", description=response)
    await ctx.send(embed=due_embed,delete_after=90)
    logger.info("List of issues shown to: "+str(ctx.author.name))

# Channel creation
@bot.command()
async def channel(ctx, name):
    logger.info("channel created: "+str(name))
    await ctx.guild.create_text_channel(name=name)

@commands.has_any_role("Kore")
@bot.command()
async def new_project(ctx):
    logger.info("new_project command called by "+ctx.author.name)
    await ctx.channel.purge(limit = 1)

    initial_embed=embeds.simple_embed(title="New project bot", description="")
    initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    message  = await ctx.send(embed = initial_embed,delete_after=60)


    due_embed=discord.Embed(title="", description="Enter the name of the project", colour=0x11806a)
    message=await ctx.send(embed=due_embed,delete_after=70)
    name = await embeds.ctx_input(ctx, bot, message)

    if not name:
        return
   
    response=function.new_project(name)
   
    if(response=="CONGRATS 🤩"+"\nProject created successfully!"):
     await ctx.guild.create_text_channel(name=str(name.replace(" ","-")))
    due_embed=discord.Embed(title="", description=response, color=0x11806a)
    await ctx.send(embed=due_embed,delete_after=60)



@commands.has_any_role("Kore")
@bot.command()
async def add_user(ctx):
    logger.info("add_user called by "+ctx.author.name)
    project_dict,project_list,project_id_dict=function.project_list()
    if(str(ctx.channel.name) in project_dict.values()): 
        project_name=str(ctx.channel.name)
        project_id=str(project_id_dict[project_name])
        logger.info("~add_user called from same channel as project name")
    else:
     logger.info("~add_user called from another channel")
     initial_embed=embeds.simple_embed(title="This is the current list of project", description=project_list)
     initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
     message  = await ctx.send(embed = initial_embed,delete_after=30)


     due_embed=discord.Embed(title="Enter the s.no of the project in which you want to add members", description="Please just give a number only eg: 1",colour=0x11806a)
     message=await ctx.send(embed=due_embed,delete_after=70)
     project_number = await embeds.ctx_input(ctx, bot, message)
     if not project_number:
        return

    
     project_name=str(project_dict[int(project_number)])
     project_id=str(project_id_dict[project_name])
   
    logger.info("project name is: "+str(project_name))
    await function.add_person(ctx,bot,project_id,project_name)
  


@commands.has_any_role("Kore")
@bot.command()
async def remove_user(ctx):
    logger.info("remove_user called by "+ctx.author.name)
    project_dict,project_list,project_id_dict=function.project_list()
    if(str(ctx.channel.name) in project_dict.values()): 
        project_name=str(ctx.channel.name)
        project_id=str(project_id_dict[project_name])
        logger.info("remove_user called from same channel as project name")
    else:
     logger.info("remove_user called from another channel")
     initial_embed=embeds.simple_embed(title="This is the current list of project", description=project_list)
     initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
     message  = await ctx.send(embed = initial_embed,delete_after=30)


     due_embed=discord.Embed(title="Enter the s.no of the project of which you want to remove members", description="Please just give a number only eg: 1",colour=0x11806a)
     message=await ctx.send(embed=due_embed,delete_after=70)
     project_number = await embeds.ctx_input(ctx, bot, message)

     if not project_number:
        return

     project_name=str(project_dict[int(project_number)])
     project_id=str(project_id_dict[project_name])
     
    logger.info("project name is :"+str(project_name))
    await function.remove_mem(ctx,bot,project_id,project_name)
    






if __name__ == "__main__":
    try:
        bot.run((os.environ.get('TOKEN')))
    except Exception as _e:
        logger.error("Exception found at main worker.\n" + str(_e))
