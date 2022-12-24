from discord.ext import commands

from gaymerbot.modules import Logger


class events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('events')

    @commands.Cog.listener()
    async def on_ready(self):
        self.log.debug(f'Logged in as {self.client.user} ID: {self.client.user.id}')
        self.log.debug(f'Client latency is: {round(self.client.latency * 1000)}ms')


async def setup(client):
    await client.add_cog(events(client))
