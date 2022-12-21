#!/usr/bin/env python


import sys
import discord
from discord.ext import commands

from .modules import Logger

log = Logger.get_logger('main')


class SupremeBot(commands.Bot):
    def __init__(self, start_time, config, initial_extensions):
        self.start_time = start_time
        self.config = config
        self.initial_extensions = initial_extensions
        intents = discord.Intents.all()
        intents.message_content = True

        # Calling the constructor method from the base class
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        # Check if there are any extensions to load
        if not self.initial_extensions:
            log.info('No initial extensions especified to load')
        else:
            failed_extensions = []

            for extension in self.initial_extensions:
                try:
                    await self.load_extension(extension)
                    log.debug(f'Loaded extension [{extension}]')
                except Exception:
                    # If the extension failed to load add it to a list and log the error
                    failed_extensions.append(extension)
                    log.exception(f'Failed to load extension [{extension}]')

            if failed_extensions:
                for failed in failed_extensions:
                    log.warning(f'Failed to load the extension [{failed}]')
            else:
                log.debug('No errors while loading extensions')


if __name__ == '__main__':
    log.critical('Use the launcher.py to run the bot!')
    sys.exit()
