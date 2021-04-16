import discord
from discord.ext import commands
from discord.utils import get
from global_functions import prefix, em


class Basic(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		await self.client.change_presence(activity=discord.Game(f'{prefix}help'))
		print(f'Logged in as {self.client.user}')

	@commands.command()
	async def ping(self, ctx):
		await em(ctx, f'{round(self.client.latency * 1000)}ms')


def setup(client):
	client.add_cog(Basic(client))