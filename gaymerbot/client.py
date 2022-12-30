import discord
from discord.ext import commands

from .modules import Logger
from .views import Furry, Age, Sexuality, Games, Notifications, Verify


class Client(commands.Bot):
    def __init__(self, config, initial_extensions, activities, start_time):
        self.config = config
        self.activities = activities
        self.start_time = start_time
        intents = discord.Intents.all()
        intents.message_content = True
        self.initial_extensions = initial_extensions
        self.log = Logger.get_logger('main')
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

        await self.add_persistant_views()

    async def add_persistant_views(self):
        try:
            self.add_view(Furry(self))
            self.add_view(Age(self))
            self.add_view(Sexuality(self))
            self.add_view(Games(self))
            self.add_view(Notifications(self))
            self.add_view(Verify(self))
        except Exception:
            self.log.exception('An error ocurred while loading persistant views!')
        else:
            self.log.info('Sucessfully loaded all persistant views')
            self.log.debug(self.persistent_views)
