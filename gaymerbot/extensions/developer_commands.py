# import discord
from discord.ext import commands

from gaymerbot.modules import Logger


class DeveloperCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('commands')
        self.view_log = Logger.get_logger('views')
        self.extension_log = Logger.get_logger('extensions')

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def extension(self, ctx):
        pass

    # !extension load {extension} - load a extension
    @extension.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            await ctx.message.delete()
            await self.client.load_extension(f'gaymerbot.extensions.{extension}')
            self.extension_log.info(f'The extension {extension} was sucessfully loaded')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'The extension {extension} is alreadly loaded')
            self.extension_log.exception(f'The extension {extension} is alreadly loaded')
        except Exception:
            await ctx.send(f'An error ocurred while loading the extension ``{extension}``')
            self.extension_log.exception(f'An error ocurred while loading the extension {extension}')

    # !extension unload {extension} - unload a extension
    @extension.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            await ctx.message.delete()
            await self.client.unload_extension(f'gaymerbot.extensions.{extension}')
            self.extension_log.info(f'The extension {extension} was sucessfully unloaded')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'The extension {extension} is not loaded')
            self.extension_log.exception(f'The extension {extension} is not loaded')
        except Exception:
            await ctx.send(f'An error ocurred while unloading the extension ``{extension}``')
            self.extension_log.exception(f'An error ocurred while unloading the extension {extension}')

    # !extension reload {extension} - reload a extension
    @extension.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            await ctx.message.delete()
            await self.client.reload_extension(f'gaymerbot.extensions.{extension}')
            self.extension_log.info(f'The extension {extension} was sucessfully reloaded')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'The extension {extension} is not loaded')
            self.extension_log.exception(f'The extension {extension} is not loaded')
        except Exception:
            await ctx.send(f'An error ocurred while reloading the extension ``{extension}``')
            self.extension_log.exception(f'An error ocurred while reloading the extension {extension}')

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def view(self, ctx):
        pass

    # !extension load {extension} - load a extension
    @view.command(name='load')
    @commands.is_owner()
    async def load_view(self, ctx, view):
        try:
            await ctx.message.delete()
            await self.client.load_extension(f'gaymerbot.views.{view}')
            self.view_log.info(f'The view {view} was sucessfully loaded')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'The view {view} is alreadly loaded')
            self.view_log.exception(f'The view {view} is alreadly loaded')
        except Exception:
            await ctx.send(f'An error ocurred while loading the view ``{view}``')
            self.view_log.exception(f'An error ocurred while loading the view {view}')

    # !extension unload {extension} - unload a extension
    @view.command(name='unload')
    @commands.is_owner()
    async def unload_view(self, ctx, view):
        try:
            await ctx.message.delete()
            await self.client.unload_extension(f'gaymerbot.views.{view}')
            self.view_log.info(f'The view {view} was sucessfully unloaded')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'The view ``{view}`` is not loaded')
            self.view_log.exception(f'The view {view} is not loaded')
        except Exception:
            await ctx.send(f'An error ocurred while unloading the view ``{view}``')
            self.view_log.exception(f'An error ocurred while unloading the view {view}')

    # !extension reload {extension} - reload a extension
    @view.command(name='reload')
    @commands.is_owner()
    async def reload_view(self, ctx, view):
        try:
            await ctx.message.delete()
            await self.client.reload_extension(f'gaymerbot.views.{view}')
            self.view_log.info(f'The view {view} was sucessfully reloaded')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'The view ``{view}`` is alreadly loaded')
            self.view_log.exception(f'The view {view} is alreadly loaded')
        except Exception:
            await ctx.send(f'An error ocurred while reloading the view ``{view}``')
            self.view_log.exception(f'An error ocurred while reloading the view {view}')

    # !sync {~} - sync slash commands globally or on this ctx guild only
    @view.command()
    @commands.is_owner()
    async def sync(self, ctx, arg=None):
        await ctx.message.delete()
        if arg == 'guild':
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            self.view_log.warning(f'Synced {len(synced)} commands on this guild')
        else:
            synced = await ctx.bot.tree.sync()
            self.view_log.warning(f'Synced {len(synced)} commands globally')


async def setup(client: commands.Bot) -> None:
    await client.add_cog(DeveloperCommands(client))
