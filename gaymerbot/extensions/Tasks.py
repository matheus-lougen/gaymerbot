import random

from discord.ext import tasks
from discord.ext import commands

import gaymerbot
from gaymerbot.modules import Logger


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('tasks')
        self.presence_switcher.start()

    def cog_unload(self):
        self.presence_switcher.cancel()
        self.log.info('Stopped task [presence_switcher]')

    @tasks.loop(seconds=5.0)
    async def presence_switcher(self):
        activity = random.choice(self.client.activities)
        await self.client.change_presence(activity=activity)
        self.log.debug(f'Presence switched to [{activity}]')

    @presence_switcher.before_loop
    async def before_presence_switcher(self):
        await self.client.wait_until_ready()
        self.log.info('Started task [presence_switcher]')


async def setup(client: gaymerbot.Client) -> None:
    await client.add_cog(Tasks(client))
