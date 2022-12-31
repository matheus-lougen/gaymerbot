import discord
from discord.ext import commands
from discord import app_commands
from twitchAPI.twitch import Twitch

import gaymerbot
from gaymerbot.modules import Logger
from gaymerbot.modules import TwitchUser, UserNotFoundError, StreamNotFoundError


class TwitchIntegrations(commands.GroupCog, name='twitch'):
    def __init__(self, client: gaymerbot.Client) -> None:
        self.client = client
        self.log = Logger.get_logger('commands')
        self.twitch_log = Logger.get_logger('twitch')
        super().__init__()  # this is now required in this context.

    @app_commands.command(name='stream', description='Informações sobre uma live')
    @app_commands.describe(user_login='Nome de usuário do streamer')
    @app_commands.rename(user_login='streamer')
    async def stream(self, interaction: discord.Interaction, user_login: str) -> None:
        twitch_api = await Twitch(self.client.config.twitch_app_id, self.client.config.twitch_app_secret)
        try:
            twitch_user = await TwitchUser.get(twitch_api, user_login)
            twitch_stream = await twitch_user.get_stream()
            embed = await twitch_stream.to_embed()
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except UserNotFoundError:
            await interaction.response.send_message(f'Desculpe, não pude encontrar o usuário ``{user_login}``', ephemeral=True)
        except StreamNotFoundError:
            await interaction.response.send_message(f'Desculpe, o usuário ``{user_login}`` não está ao vivo no momento!', ephemeral=True)

    @app_commands.command(name='user', description='Informações sobre um streamer')
    @app_commands.describe(user_login='Nome de usuário do streamer')
    @app_commands.rename(user_login='streamer')
    async def user(self, interaction: discord.Interaction, user_login: str) -> None:
        twitch_api = await Twitch(self.client.config.twitch_app_id, self.client.config.twitch_app_secret)
        try:
            twitch_user = await TwitchUser.get(twitch_api, user_login)
            embed = await twitch_user.to_embed()
            await interaction.response.send_message(embed=embed)
        except UserNotFoundError:
            await interaction.response.send_message(f'Desculpe, não pude encontrar o usuário ``{user_login}``', ephemeral=True)


async def setup(client: gaymerbot.Client) -> None:
    await client.add_cog(TwitchIntegrations(client))
