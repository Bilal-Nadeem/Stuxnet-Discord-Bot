import discord
from discord.ext import commands
import random
from global_functions import prefix, em


class Fun(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['t',])
	async def truth(self, ctx):
	    with open('truths.txt', 'r') as f:
	        tr = random.choice(f.read().split('\n\n'))

	    await em(ctx, tr)

	@commands.command(aliases=['d',])
	async def dare(self, ctx):
	    with open('dares.txt', 'r') as f:
	        dr = random.choice(f.read().split('\n'))

	    await em(ctx, dr)

	@commands.command()
	async def emojify(self, ctx, *, msg):
	    d = {
	    "A": "🇦",
	    "B": "🇧",
	    "C": "🇨",
	    "D": "🇩",
	    "E": "🇪",
	    "F": "🇫",
	    "G": "🇬",
	    "H": "🇭",
	    "I": "🇮",
	    "J": "🇯",
	    "K": "🇰",
	    "L": "🇱",
	    "M": "🇲",
	    "N": "🇳",
	    "O": "🇴",
	    "P": "🇵",
	    "Q": "🇶",
	    "R": "🇷",
	    "S": "🇸",
	    "T": "🇹",
	    "U": "🇺",
	    "V": "🇻",
	    "W": "🇼",
	    "X": "🇽",
	    "Y": "🇾",
	    "Z": "🇿",
	    " ": "  "
	    }
	    msg = msg.upper()
	    print(msg)
	    l = []
	    s = ''
	    for m in msg:
	        try:
	            l.append(d[m] + '|')
	        except:
	            s = '***Only Letters***'
	            break
	    if s:
	        await ctx.send(s)
	    else:
	        l = ''.join(l)
	        await ctx.send(l)


def setup(client):
	client.add_cog(Fun(client))