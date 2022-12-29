import discord
import asyncio
import twitchAPI
from discord.ext import commands
from discord import app_commands
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first

import gaymerbot
from gaymerbot.modules import Logger


class TwitchStream():
    @classmethod
    async def get(cls, raw_stream_data, twitch_user) -> object:
        self = TwitchStream()
        self.raw_stream_data = raw_stream_data
        self.twitch_user = twitch_user
        return self

    async def get_url(self) -> str:
        url = f'https://twitch.tv/{self.raw_stream_data.user_name}'
        return url

    async def to_embed(self) -> discord.Embed or None:
        if await self.twitch_user.is_live():
            stream_url = await self.get_url()
            embed = discord.Embed(title=f'**{self.raw_stream_data.title}**', description='', url=stream_url, colour=discord.Colour.purple())
            embed.add_field(name='Streamer:', value=f'``{self.raw_stream_data.user_name}``', inline=True)
            embed.add_field(name='Jogo:', value=f'``{self.raw_stream_data.game_name}``', inline=True)
            embed.add_field(name='Número de viewers:', value=f'``{self.raw_stream_data.viewer_count}``', inline=True)
            embed.set_image(url=self.raw_stream_data.thumbnail_url.format(width=800, height=600))
            return embed
        else:
            return None


class TwitchUser():
    @classmethod
    async def get(cls, twitch_api, user_login) -> object:
        self = TwitchUser()
        self.twitch_api = twitch_api
        self.user_login = user_login
        self.raw_user_data = await first(self.twitch_api.get_users(logins=user_login))
        return self

    async def get_raw_stream_data(self) -> twitchAPI.object.Stream:
        raw_stream_data = await first(self.twitch_api.get_streams(user_id=self.raw_user_data.id))
        return raw_stream_data

    async def get_stream(self) -> TwitchStream:
        raw_stream_data = await self.get_raw_stream_data()
        stream = await TwitchStream.get(raw_stream_data, self)
        return stream

    async def is_live(self) -> bool:
        raw_stream_data = await self.get_raw_stream_data()
        if raw_stream_data is None:
            return False
        else:
            return True

    async def found(self) -> bool:
        if self.raw_user_data is None:
            return False
        else:
            return True

    async def get_url(self) -> str:
        url = f'https://twitch.tv/{self.raw_user_data.login}'
        return url

    async def to_embed(self) -> discord.Embed:
        if await self.found():
            user_url = await self.get_url()
            embed = discord.Embed(title=f'**{self.raw_user_data.display_name}**', description=f'{self.raw_user_data.description}', url=user_url, colour=discord.Colour.purple())
            embed.add_field(name='Total de viewers:', value=f'``{self.raw_user_data.view_count}``', inline=True)
            embed.set_image(url=self.raw_user_data.profile_image_url)
            return embed
        else:
            return None


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
        twitch_user = await TwitchUser.get(twitch_api, user_login)
        if await twitch_user.found():
            if await twitch_user.is_live():
                stream = await twitch_user.get_stream()
                embed = await stream.to_embed()
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message(f'Desculpe, o usuário ``{twitch_user.user_login}`` não está ao vivo no momento!', ephemeral=True)
        else:
            await interaction.response.send_message(f'Desculpe, não pude encontrar o usuário ``{twitch_user.user_login}``', ephemeral=True)

    @app_commands.command(name='user', description='Informações sobre um streamer')
    @app_commands.describe(user_login='Nome de usuário do streamer')
    @app_commands.rename(user_login='streamer')
    async def user(self, interaction: discord.Interaction, user_login: str) -> None:
        twitch_api = await Twitch(self.client.config.twitch_app_id, self.client.config.twitch_app_secret)
        twitch_user = await TwitchUser.get(twitch_api, user_login)
        if await twitch_user.found():
            embed = await twitch_user.to_embed()
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f'Desculpe, não pude encontrar o usuário ``{twitch_user.user_login}``', ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        notification_sent = False
        twitch_api = await Twitch(self.client.config.twitch_app_id, self.client.config.twitch_app_secret)
        twitch_user = await TwitchUser.get(twitch_api, 'thinaibr')
        if await twitch_user.found():
            while not self.client.is_closed():
                if await twitch_user.is_live() and notification_sent is False:
                    notification_sent = True
                    stream = await twitch_user.get_stream()
                    embed = await stream.to_embed()
                    channel = await self.client.fetch_channel(728612092315435098)
                    await channel.send(embed=embed)

                elif await twitch_user.is_live():
                    notification_sent = True
                    await asyncio.sleep(60)

                elif not await twitch_user.is_live():
                    notification_sent = False
                    self.twitch_log.debug('User is not live retrying in 60 seconds')
                    await asyncio.sleep(60)
                    continue
        else:
            self.log.critical('Could not find the user!')


async def setup(client: gaymerbot.Client) -> None:
    await client.add_cog(TwitchIntegrations(client))
