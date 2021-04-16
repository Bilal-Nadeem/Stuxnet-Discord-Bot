import discord
from discord.ext import commands
from discord.utils import get
import typing
from global_functions import prefix, em, embed_color
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://legend9:%40Bilal987654321@first-cluster-for-disco.xkovb.mongodb.net/discord?retryWrites=true&w=majority")

#https://stackoverflow.com/questions/64741471/discord-py-get-user-minutes-in-vc


class Levels(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = cluster['discord']['leveling']
		self.exp_amount = 1
		self.level_up_message_channel_id = cluster['discord']['etc'].find_one({"_id": 'level_up_message_channel_id'})['level_up_message_channel_id']
		self.user_level = {}


	@commands.Cog.listener()
	async def on_message(self, message):
		uid = message.author.id
		if message.guild.id in [830809734126501908, 829709301630369862] and not message.author.bot:
			user = await self.get_user(uid)
			if user == None:
				user = await self.create_user(uid)

			if uid in self.user_level:
				last_level = self.user_level[uid]
				current_level = await self.calc_level(user['exp'])
				if current_level > last_level:
					ch = self.client.get_channel(self.level_up_message_channel_id)
					embed = discord.Embed(title=None, description=f'<@!{uid}> Leveled up from `{last_level}` to `{current_level}`', color=embed_color)
					await ch.send(f'Congratulations! <@!{uid}>')
					await ch.send(embed=embed)
				if current_level < last_level:
					ch = self.client.get_channel(self.level_up_message_channel_id)
					await ch.send(f'Sorry! <@!{uid}>')
					embed = discord.Embed(title=None, description=f'<@!{uid}> Leveled down from `{last_level}` to `{current_level}`', color=embed_color)
					await ch.send(embed=embed)
				self.user_level[uid] = current_level
			else:
				self.user_level[uid] = await self.calc_level(user['exp'])


			await self.update_user(uid, self.exp_amount)

			#we will store level last time user messaged, and if level greater then last time then say in a channel u leveled up


			#create a document for that user is mongo database if not there, else retrieve the user
			#then $inc some exp according to what i set
			#maybe do something like a timer where exp is only posted to database if user hasent done a message in last 8 seconds
			#will keep a time assinged to id using time.time() and check if time.time() difference > 8 seconds if so update the dict and add exp
			#make every level require 1.2x exp then last like 100 exp level 1 220 exp level 2 484 at level 3 and so on which i can calculate on the go through exp and no need to use the db for levels

	@commands.command()
	async def profile(self, ctx, user: typing.Union[int, discord.Member, None]):
			try:
				uid = int(user)
			except:
				user = user or ctx.author
				uid = user.id

			data = await self.get_user(uid)
			if data != None:
				exp = data['exp']
				level = await self.calc_level(exp)
				embed = discord.Embed(title=f'{user.name} Profile!', color=embed_color)
				embed.set_thumbnail(url=user.avatar_url)
				embed.add_field(name='Level!', value=f'`{level}`', inline=False)
				embed.add_field(name='Experiece Points!', value=f'`{exp}`', inline=False)
				embed.add_field(name='Next Level!', value=f'At `{level + 1}00` Points', inline=False)
				# embed.set_footer(text=f"You get 1 level every 100 experience points")
				await ctx.send(embed=embed)
			else:
				await em(ctx, f'User Doesnt Exists')

	@commands.command(aliases=['leaderboards',])
	async def leaderboard(self, ctx):
		all_users = self.db.find({})
		d = {}
		m = {}
		for _ in all_users:
			d[_['_id']] = _['exp']

		print(d)
		for _ in range(len(d)):
			ma = max(d, key=lambda key: d[key])
			m[_+1] = {ma: d[ma]}
			d.pop(ma)
		user_list = []
		exp_list = []
		for _ in range(0+1, 8+1): #change to 8 later
			k = [_ for _ in m[_].keys()][0]
			user_list.append(k)
			exp_list.append(m[_][k])

		data = ''
		for _ in range(len(user_list)):
			data += f'<@!{user_list[_]}>: `{exp_list[_]}`\n\n'

		embed = discord.Embed(title='Top 8!', description=data, color=embed_color)
		await ctx.send(embed=embed)


	@commands.command()
	async def level_up_channel(self, ctx, channel_id: int):
		if ctx.message.author.id == 825765301236924456:
			ch = self.client.get_channel(channel_id)
			if ch:
				cluster['discord']['etc'].update_one({"_id": 'level_up_message_channel_id'}, {"$set": {'level_up_message_channel_id': channel_id}})
				self.level_up_message_channel_id = cluster['discord']['etc'].find_one({"_id": 'level_up_message_channel_id'})['level_up_message_channel_id']
				embed = discord.Embed(title=None, description=f'***Successfully Changed Level Up Message Channel To <#{channel_id}>***', color=embed_color)
				await ctx.send(embed=embed)
			else:
				await em(ctx, 'Channel Not Found')


	@commands.command(aliases=['delete_user',])
	async def delete(self, ctx, user: typing.Union[int, discord.Member]):
		if ctx.message.author.id == 825765301236924456:
			if user != None:
				try:
					_id = int(user)
				except:
					_id = user.id

				if await self.get_user(_id) != None:
					a = await self.delete_user(_id)
					print(a.deleted_count)
					if a.deleted_count != 0:
						embed = discord.Embed(title=None, description=f'***Successfully Deleted <@!{_id}>***', color=embed_color)
						await ctx.send(embed=embed)
					else:
						await em(ctx, 'I wasnt able to Delete that user')
				else:
					await em(ctx, 'User Doesnt Exists!')

			else:
				await em(ctx, 'Please pass a user id!')
		else:
			await em(ctx, 'You dont have permissions!')


	@commands.command()
	async def add_exp(self, ctx, user: typing.Union[int, discord.Member], exp: int):
		if ctx.message.author.id == 825765301236924456:
			if user != None:
				if exp != None:
					try:
						_id = int(user)
					except:
						_id = user.id

					if await self.get_user(_id) != None:
						a = await self.update_user(_id, exp)
						if a.matched_count != 0:
							embed = discord.Embed(title=None, description=f'***Successfully Added `{exp}` Experiece Points To <@!{_id}>***', color=embed_color)
							await ctx.send(embed=embed)
						else:
							await em(ctx, 'I wasnt able to add experience points to that user')
					else:
						await em(ctx, 'User Doesnt Exsist!')

				else:
					await em(ctx, 'Please give a number for experience')

			else:
				await em(ctx, 'Please pass a user id!')
		else:
			await em(ctx, 'You dont have permissions!')


	@commands.command()
	async def change_exp(self, ctx, user: typing.Union[int, discord.Member], exp: int):
		if ctx.message.author.id == 825765301236924456:
			if user != None:
				if exp != None:
					try:
						_id = int(user)
					except:
						_id = user.id

					if await self.get_user(_id) != None:
						a = await self.change_user_exp(_id, exp)
						if a.matched_count != 0:
							embed = discord.Embed(title=None, description=f'***Successfully Changed <@!{_id}> Experiece Points To `{exp}`***', color=embed_color)
							await ctx.send(embed=embed)
						else:
							await em(ctx, 'I wasnt able to add experience points to that user')
					else:
						await em(ctx, 'User Doesnt Exsist!')

				else:
					await em(ctx, 'Please give a number for experience')

			else:
				await em(ctx, 'Please pass a user id!')
		else:
			await em(ctx, 'You dont have permissions!')


	@commands.command()
	async def add_user(self, ctx, user: typing.Union[int, discord.Member]):
		if ctx.message.author.id == 825765301236924456:
			if user != None:
					try:
						_id = int(user)
					except:
						_id = user.id
					if await self.get_user(_id) == None:
						a = await self.create_user(_id)
						embed = discord.Embed(title=None, description=f'***Successfully Added The User***', color=embed_color)
						await ctx.send(embed=embed)
					else:
						await em(ctx, 'User Is Already Added!')

			else:
				await em(ctx, 'Please pass a user id!')
		else:
			await em(ctx, 'You dont have permissions!')



	@commands.command()
	async def change_exp_amount(self, ctx, amount: int):
		last_amount = self.exp_amount
		self.exp_amount = amount
		await em(ctx, f'Successfully Changed Exp Points Given Every Message From `{last_amount}` To `{amount}`')




	# async def calc_level(exp, multi):
	# 	if exp >= 100:
	# 		a = 100
	# 		b = 100
	# 		l = 1
	# 		for _ in range(1000):
	# 			a = (a * multi)
	# 			b = a + b
	# 			if exp >= b:
	# 				l += 1
	# 		return l
	# 	else:
	# 		return 0

	async def calc_level(self, exp):
		# level = 0
		# for _ in range(100,exp + 200,100):
		# 	print(_)
		# 	if exp >= _:
		# 		level += 1
		# 	else:
		# 		break
		# return level

		a = str(exp)[:-2] or 0
		a = int(a)
		return a




	async def create_user(self, _id):
		return self.db.insert_one({"_id":_id, 'exp':0})

	async def delete_user(self, _id):
		return self.db.delete_one({"_id":_id})

	async def get_user(self, _id):
		return self.db.find_one({"_id":_id})

	async def update_user(self, _id, exp):
		return self.db.update_one({"_id": _id}, {"$inc": {'exp': exp}})

	async def change_user_exp(self, _id, exp):
		return self.db.update_one({"_id": _id}, {"$set": {'exp': exp}})








def setup(client):
	client.add_cog(Levels(client))