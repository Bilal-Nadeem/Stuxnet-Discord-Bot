import discord
from discord.ext import commands
from discord.utils import get
from global_functions import prefix, em, embed_color


class Members(commands.Cog):

	def __init__(self, client):
		self.client = client



	@commands.Cog.listener()
	async def on_member_join(self, member):
	    global invitess
	    if not member.bot:
	        guild = self.client.get_guild(829709301630369862)
	        role = get(guild.roles, name="unverified")
	        channel = client.get_channel(829709301630369865)
	        embed = discord.Embed(title="Welcome To StuxNet!",description=f"Make sure to check out <#829745111109337088> and <#829745133913636894> <@!{member.id}>", color=discord.Color.blurple()) # Let's make an embed!
	        await channel.send(embed=embed)
	        await member.add_roles(role)

	        channel = self.client.get_channel(829800785084284979)
	        embed = discord.Embed(title=f"<@!{member.id}> Just Joined!", color=embed_color) # Let's make an embed!
	        await channel.send(embed=embed)
	        
	    else:
	        guild = self.client.get_guild(829709301630369862)
	        role = get(guild.roles, name="Bots")
	        await member.add_roles(role)
	            


	    channel = self.client.get_channel(830049096776548353)
	    n = len(guild.members)
	    await channel.edit(name=f'Members: {n}')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
	    channel = self.client.get_channel(829994884521918474)
	    embed = discord.Embed(title="A Member Just Left!", color=embed_color)
	    await channel.send(embed=embed)


def setup(client):
	client.add_cog(Members(client))