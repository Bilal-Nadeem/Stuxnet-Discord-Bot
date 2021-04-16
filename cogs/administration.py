import discord
from discord.ext import commands
import typing
import aiohttp
from global_functions import prefix, em, embed_color, get_emo, fe


class Administration(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.eod = False


	@commands.Cog.listener()
	async def on_message(self, m):
	    if m.channel.id in [829728048781852713] and m.author.id != self.client.user.id:
	        if m.content.lower() == '.enable':
	            self.eod = True
	        elif m.content.lower() == '.disable':
	            self.eod = False

	        if self.eod:
	            querystring = {"bid":"178","key":"sX5A2PcYZbsN5EY6","uid":"mashape","msg":m.content}
	            headers = {
	            'x-rapidapi-key': "3f1e388716msh65e428495fb4fc7p1107ebjsne523fc561130",
	            'x-rapidapi-host': "acobot-brainshop-ai-v1.p.rapidapi.com"
	            }
	            async with aiohttp.ClientSession() as session:
	                async with session.get(f'https://acobot-brainshop-ai-v1.p.rapidapi.com/get',headers=headers, params=querystring) as r:
	                    r = await r.json()
	                    r = r['cnt']
	                    await m.channel.send(r)


	@commands.command()
	async def poll(self, ctx, *, message=None):
	    if message == None:
	        await em(self, ctx, "Please provide some text")
	    else:
	        embed = discord.Embed(title=message, color=embed_color)
	        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
	        m = await ctx.send(embed=embed)
	        await m.add_reaction('👍')
	        await m.add_reaction('👎')

	@commands.command()
	async def whois(self, ctx, member: typing.Union[int, discord.Member, None]):
		try:
			user_id = int(member)
			member = await self.client.fetch_user(user_id)
			embed = discord.Embed(colour=embed_color, timestamp=ctx.message.created_at,
			title=f"User Info - {member}")
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=f"Requested by {ctx.author}")
			embed.add_field(name="ID:", value=member.id)
			embed.add_field(name="Display Name:", value=member.display_name)
			embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
			await ctx.send(embed=embed)
		except:
			member = member or ctx.author
			embed = discord.Embed(colour=embed_color, timestamp=ctx.message.created_at,
			                      title=f"User Info - {member}")
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=f"Requested by {ctx.author}")
			embed.add_field(name="ID:", value=member.id)
			embed.add_field(name="Display Name:", value=member.display_name)
			embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
			embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
			embed.add_field(name="Roles:", value='@everyone' + ' '.join([_.mention for _ in member.roles if _.name != '@everyone']))
			print(dir(member.roles[2]))
			print(member.mention)
			await ctx.send(embed=embed)

	@commands.command()
	async def purge(self, ctx, num=1):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        if num < 1000:
	            a = await ctx.channel.purge(limit=num)
	            embed = discord.Embed(title='Deleted {} message(s)'.format(
	                len(a)), color=embed_color)
	            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	            await ctx.channel.send(embed=embed)

	        else:
	            await em(self, ctx, 'Max 999 messages can be deleted at a time')
	    else:
	        await em(self, ctx, 'You dont have perms!')


	@commands.command()
	async def purgeu(self, ctx, member: discord.Member, num=1):
		if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
			if num < 1000:
				a = await ctx.channel.purge(limit=num, check=lambda message: message.author.id == member.id)
				embed = discord.Embed(title=f'Deleted {len(a)} message(s)', description=f'**From:** <@!{member.id}>\n***In Last {num} messages*** ' ,color=embed_color)
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)


	@commands.command()
	async def nick_all(self, ctx, n, pos=None):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        for m in ctx.guild.members:
	            try:
	                if not pos:
	                	await m.edit(nick=n)
	                elif pos:
	                	if pos.lower() == 'r':
	                		await m.edit(nick=f'{m.name}{n}')
	                	elif pos.lower() == 'l':
	                		await m.edit(nick=f'{n}{m.name}')
	            except:
	                continue

	        await em(ctx, 'Done')



	@commands.command()
	async def reset_nick_all(self, ctx):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        for m in ctx.guild.members:
	            try:
	                await m.edit(nick="")
	            except:
	                continue

	        await em(ctx, 'Done')


	@commands.command()
	async def kick(self, ctx, member: discord.Member):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        try:
	            await member.kick()
	            await em(ctx, f'{member.name} was kicked')
	        except:
	            await em(ctx, f'I am not able to kick {member.name}')


	@commands.command()
	async def ban(self, ctx, member: discord.Member):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        try:
	            await member.ban()
	            await em(ctx, f'{member.name} was banned')
	        except:
	            await em(ctx, f'I am not able to ban {member.name}')

	@commands.command()
	async def create_embed(self, ctx, *, m):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        m = await get_emo(ctx, m)
	        await em(ctx, m)


	@commands.command()
	async def ce(self, ctx, t, *, m):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        t = await get_emo(ctx, t)
	        m = await get_emo(ctx, m)
	        embed = discord.Embed(title=t, description=f'**{m}**', color=embed_color)
	        await ctx.send(embed=embed)



	@commands.command()
	async def add_reaction(self, ctx, m_id, *, r):

	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:

	        r = r.split(' ')

	        msg = await ctx.fetch_message(m_id)
	        for _ in r:
	            _ = await get_emo(ctx,_)
	            await msg.add_reaction(_)
	        
	        await em(ctx, 'Done')


	@commands.command()
	async def create_role(self, ctx, *, rname):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        await ctx.guild.create_role(name=rname)


	@commands.command()
	async def chperms(self, ctx):
	    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 825765301236924456:
	        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)




	@commands.command()
	async def emo(self, ctx, *, m):

	    m = await get_emo(ctx, m)
	    
	    hooks = await ctx.channel.webhooks()
	    if hooks:
	        for hook in hooks:
	            if hook.name == ctx.channel.name:
	                await hook.send(content=m, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)

	    else:
	        hook = await ctx.channel.create_webhook(name=ctx.channel.name)
	        await hook.send(content=m, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)

	    await ctx.message.delete()


	@commands.command()
	async def list_roles(self, ctx):
	    global embed_color
	    l = []
	    for _ in ctx.guild.members:
	        names = [a.name for a in _.roles]
	        if 'Super Admin' in names:
	            l.append(f'**Super Admin: <@!{_.id}>**')
	        elif 'Admin' in names:
	            l.append(f'**Admin: <@!{_.id}>**')
	        elif 'Moderator' in names:
	            l.append(f'**Moderator: <@!{_.id}>**')

	    l = '\n'.join(l)
	    embed = discord.Embed(title='Staff', description=l, color=embed_color)
	    await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Administration(client))