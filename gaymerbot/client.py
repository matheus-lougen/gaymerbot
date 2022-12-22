#!/usr/bin/env python


import discord
from discord.ext import commands

from .modules import Logger


class Client(commands.Bot):
    def __init__(self, start_time, config, initial_extensions, initial_views):
        self.config = config
        self.start_time = start_time
        intents = discord.Intents.all()
        intents.message_content = True
        self.initial_views = initial_views
        self.view_log = Logger.get_logger('views')
        self.initial_extensions = initial_extensions
        self.extension_log = Logger.get_logger('extensions')

        # Calling the constructor method from the base class
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        if not self.initial_extensions:
            self.extension_log.info('No initial extensions especified to load')
        else:
            failed_extensions = []

            for extension in self.initial_extensions:
                try:
                    await self.load_extension(extension)
                    self.extension_log.debug(f'Loaded extension [{extension}]')
                except Exception:
                    failed_extensions.append(extension)
                    self.extension_log.exception(f'Failed to load extension [{extension}]')

            if failed_extensions:
                for failed in failed_extensions:
                    self.extension_log.warning(f'Failed to load the extension [{failed}]')
            else:
                self.extension_log.debug('No errors while loading extensions')

        if not self.initial_views:
            self.view_log.info('No initial views especified to load')
        else:
            failed_views = []

            for view in self.initial_views:
                try:
                    await self.load_extension(view)
                    self.view_log.debug(f'Loaded view [{view}]')
                except Exception:
                    failed_views.append(view)
                    self.view_log.exception(f'Failed to load view [{view}]')

            if failed_extensions:
                for failed in failed_extensions:
                    self.view_log.warning(f'Failed to load the view [{failed}]')
            else:
                self.view_log.debug('No errors while loading views')
