import discord
from discord.ext import commands
import os
from global_functions import get_emo, embed_color

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents, help_command = None)

@client.command()
async def help(ctx):
	embed = discord.Embed(title='<a:blue_fire:830753110594289684> Help! <a:blue_fire:830753110594289684>', description='Gonne Add More Commands Soon, Please Give Suggestions In <#829731563428118617>', color=embed_color)
	embed.add_field(name='Administration:', value='`add_reaction` `ban` `ce` `chperms` `create_embed` `create_role` `emo` `kick list_roles` `nick_all` `poll` `purge` `purgeu` `reset_nick_all` `whois`', inline=False)
	embed.add_field(name='Levels:', value='`add_exp` `add_user` `delete_user` `change_exp` `change_exp_amount` `leaderboard` `profile` `level_up_channel`', inline=False)
	embed.add_field(name='Application:', value='`accept` `apply`', inline=False)
	embed.add_field(name='Basic:', value='`ping`', inline=False)
	embed.add_field(name='Covid:', value='`covid_countries` `covid_pakistan_stats` `covid_stats`', inline=False)
	embed.add_field(name='Fun:', value='`dare` `emojify` `truth` `enable` `disable`', inline=False)
	embed.add_field(name='Images:', value='`av` `img` `meme` `slap` `wanted`', inline=False)
	embed.add_field(name='Music:', value='`play` `leave` `pause` `resume` `stop` `say`', inline=False)
	await ctx.send(embed=embed)

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
    

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename != 'global_functions.py':
		client.load_extension(f'cogs.{filename[:-3]}')



client.run('ODI5NzM5MDQyNjU1Njk4OTY1.YG8gsw.ZwZywjA43Dwnv4ckuaoZFlri-wY')





