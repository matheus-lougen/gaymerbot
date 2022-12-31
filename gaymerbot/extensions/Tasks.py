import random
import asyncio

from discord.ext import tasks
from discord.ext import commands
from twitchAPI.twitch import Twitch

import gaymerbot
from gaymerbot.modules import Logger
from gaymerbot.modules import TwitchUser, UserNotFoundError, StreamNotFoundError


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('tasks')
        self.presence_switcher.start()
        self.twitch_notifier.start()

    def cog_unload(self):
        self.presence_switcher.cancel()
        self.log.info('Stopped task [presence_switcher]')
        self.twitch_notifier.cancel()
        self.log.info('Stopped task [twitch_notifier]')

    @tasks.loop(seconds=20.0)
    async def presence_switcher(self):
        activity = random.choice(self.client.activities)
        await self.client.change_presence(activity=activity)
        self.log.debug(f'Presence switched to [{activity}]')

    @presence_switcher.before_loop
    async def before_presence_switcher(self):
        await self.client.wait_until_ready()
        self.log.info('Started task [presence_switcher]')

    @tasks.loop(seconds=60.0)
    async def twitch_notifier(self):
        try:
            twitch_user = await TwitchUser.get(self.twitch_api, self.user_name)
        except UserNotFoundError:
            self.log.critical(f'Failed to find twitch user [{self.user_name}]')
        else:
            try:
                if self.notification_sent is False:
                    self.notification_sent = True
                    stream = await twitch_user.get_stream()
                    embed = await stream.to_embed()
                    channel = await self.client.fetch_channel(self.channel_id)
                    await channel.send(embed=embed)

            except StreamNotFoundError:
                self.notification_sent = False
                self.log.debug(f'Twitch user [{self.user_name}] is not live retrying in 60 seconds')

            else:
                self.notification_sent = True

    @twitch_notifier.before_loop
    async def before_twitch_notifier(self):
        await self.client.wait_until_ready()
        self.user_name = 'gaules'
        self.channel_id = 728612092315435098
        self.notification_sent = False
        self.twitch_api = await Twitch(self.client.config.twitch_app_id, self.client.config.twitch_app_secret)
        self.log.info('Started task [twitch_notifier]')


async def setup(client: gaymerbot.Client) -> None:
    await client.add_cog(Tasks(client))
