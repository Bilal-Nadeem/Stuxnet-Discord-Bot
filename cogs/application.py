import discord
from discord.ext import commands
from global_functions import prefix, em, embed_color

q_list = [
    'How much Experience do you have on discord?',
    'How will you handle abuse raid in the server?',
    'Would you invite people and be active in chat?'
]

a_list = []

class Application(commands.Cog):

	def __init__(self, client):
		self.client = client



	@commands.command()
	async def apply(self, ctx):

	    a_list = []
	    submit_channel = self.client.get_channel(830005339033829426)
	    channel = await ctx.author.create_dm()

	    await ctx.send(embed=await em(ctx, f'Application has been started by {ctx.message.author.name} Check Dms', r=True))

	    def check(m):
	        return m.content is not None and m.channel == channel and m.author.id != self.client.user.id

	    for question in q_list:
	        question = await em(ctx, question, r=True)
	        await channel.send(embed=question)
	        try:
	            msg = await self.client.wait_for('message', timeout=60.0, check=check)
	        except asyncio.TimeoutError:
	            await channel.send(embed=await em(ctx, 'Timeout, You didnt reply in 60 seconds', r=True))
	            return
	        a_list.append(msg.content)

	    await channel.send(embed=await em(ctx, 'End of questions - say "yes" to finish/submit it or "no" to leave it.', r=True))

	    try:
	        msg = await self.client.wait_for('message', timeout=60.0, check=check)
	    except asyncio.TimeoutError:
	        await channel.send(embed=await em(ctx, 'Timeout, You didnt reply in 60 seconds', r=True))
	        return

	    if "yes" in msg.content.lower():
	        embed = discord.Embed(
	            title='Application By:',
	            description=f'<@!{ctx.author.id}>',
	            color=embed_color
	        )
	        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

	        for n, answer in enumerate(a_list):
	            embed.add_field(name=f'{q_list[n]}',
	                            value=f'{answer}', inline=False)

	        await submit_channel.send(embed=embed)

	        embed = await em(ctx, 'Your application has been sent successfully!', r=True)
	        await channel.send(embed=embed)

	    elif "no" in msg.content.lower():
	        embed = await em(ctx, 'Discarded successfully', r=True)
	        await channel.send(embed=embed)

	    else:
	        embed = await em(ctx, 'You had to answer a yes or no, application wasn\'t sent!', r=True)
	        await channel.send(embed=embed)



	@commands.command()
	async def accept(self, ctx, user: discord.Member = None):
	    if ctx.message.author.guild_permissions.administrator:
	        channel = self.client.get_channel(830005385670033429)
	        embed = discord.Embed(
	            title='Application Accepted!',
	            description=f'<@!{user.id}> Your Application Has Been Accepted Contact Mr. Stark For Role',
	            color=embed_color
	        )
	        await channel.send(embed=embed)
	        await channel.send(f'<@!{user.id}>')
	    else:
	        await em(ctx, 'You Dont Have Perms!')



def setup(client):
	client.add_cog(Application(client))