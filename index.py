# -*- coding: utf-8 -*-
import os
from threading import Thread
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import Client, filters
import asyncio
import json
from time import sleep
from datetime import datetime, timezone, timedelta
import re
import traceback
import traceback

def get_list(name):
	with open(name+'.txt','r') as file:
		return file.read().splitlines()

async def start():
	all_messages = []
	await app.start()
	while True:
		include = get_list('include')
		exclude = get_list('exclude')
		try:
			channels = [exclude,include]
			
			exclude_members = []

			for i in range(2):
				for channel in channels[i]:
					users_messages = {} 
					print(channel)
					if i == 1:
						async for message in app.get_chat_history(channel.split('/')[-1],limit=100):
							if message.from_user and not message.from_user.id in users_messages:
								if message.text:
									text = str(message.link)+'\n\n'+message.text
								else:
									text = str(message.link)
								
								if text not in all_messages:
									users_messages[message.from_user.id] = text
									all_messages.append(text)
					try:
						async for member in app.get_chat_members(channel.split('/')[-1]):
							if i == 0:
								exclude_members.append(member.user.id)
							else:
								while True:
									try:
										if not member.user.id in exclude_members and member.user.id in users_messages:
											await app.send_message(chat_id=params['username'],text=users_messages[member.user.id])
										break
									except FloodWait:
										traceback.print_exc()
										sleep(10)
									except:
										traceback.print_exc()
										break
					except:			
						traceback.print_exc()

					sleep(1)
		
			sleep(params['auto'])
		except:
			traceback.print_exc()

with open('params.json','r') as file:
	params = json.loads(file.read())

app = Client('my_account',api_id=params['api_id'], api_hash=params['api_hash'])

asyncio.run(start())