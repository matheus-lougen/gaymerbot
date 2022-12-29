import asyncio

import discord
from discord.ext import commands

from gaymerbot.modules import Logger


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('events')

    @commands.Cog.listener()
    async def on_ready(self):
        self.log.debug(f'Logged in as {self.client.user} ID: {self.client.user.id}')
        self.log.debug(f'Client latency is: {round(self.client.latency * 1000)}ms')

        while True:
            await self.client.change_presence(activity=discord.Game(name='V1.3'))
            await asyncio.sleep(5)
            await self.client.change_presence(activity=discord.Game(name='/help'))
            await asyncio.sleep(5)
            await self.client.change_presence(activity=discord.Game(name='Minecraft'))
            await asyncio.sleep(5)


async def setup(client):
    await client.add_cog(Events(client))
