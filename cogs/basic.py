import discord
from discord.ext import commands
from discord.utils import get
from global_functions import prefix, em
import re

with open('pokemons.txt', 'r') as f:
	pokemons = f.read()


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

	@commands.Cog.listener()
	async def on_message(self, message):
		m = ''
		for _ in message.content[15:-1]:
			if _ != '\\':
				m += _

		if message.content[:14] == "The pokémon is":
			ph = ''
			for a in m:
				if a != '_':
					ph += a
				else:
					ph += '.'
			print(ph)
			ph = ph.lower()
			c = re.compile(ph)
			l = list(set(c.findall(pokemons)))
			print(l)
			if len(l) < 6:
				await message.channel.send(' '.join(l))
			else:
				await message.channel.send('I was unable to find the hint')

def setup(client):
	client.add_cog(Basic(client))
