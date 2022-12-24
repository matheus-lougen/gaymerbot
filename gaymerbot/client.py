import discord
from discord.ext import commands

from .modules import Logger


class Client(commands.Bot):
    def __init__(self, start_time, config, initial_extensions):
        self.config = config
        self.start_time = start_time
        intents = discord.Intents.all()
        intents.message_content = True
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
