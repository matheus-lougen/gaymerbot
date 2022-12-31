import twitchAPI
import discord
from twitchAPI.helper import first


class UserNotFoundError(Exception):
    pass


class StreamNotFoundError(Exception):
    pass


class TwitchStream:
    @classmethod
    async def get(cls, raw_stream_data, twitch_user) -> object:
        self = TwitchStream()
        self.twitch_user = twitch_user
        self.raw_stream_data = raw_stream_data
        if raw_stream_data is None:
            raise StreamNotFoundError
        else:
            return self

    async def get_url(self) -> str:
        url = f'https://twitch.tv/{self.raw_stream_data.user_name}'
        return url

    async def to_embed(self) -> discord.Embed or None:
        try:
            stream_url = await self.get_url()
            embed = discord.Embed(
                title=f'**{self.raw_stream_data.title}**',
                description='',
                url=stream_url,
                colour=discord.Colour.purple(),
            )
            embed.add_field(
                name='Streamer:',
                value=f'``{self.raw_stream_data.user_name}``',
                inline=True,
            )
            embed.add_field(
                name='Jogo:',
                value=f'``{self.raw_stream_data.game_name}``',
                inline=True,
            )
            embed.add_field(
                name='Número de viewers:',
                value=f'``{self.raw_stream_data.viewer_count}``',
                inline=True,
            )
            embed.set_image(url=self.raw_stream_data.thumbnail_url.format(width=800, height=600))
            return embed
        except StreamNotFoundError:
            return None


class TwitchUser:
    @classmethod
    async def get(cls, twitch_api, user_login) -> object:
        self = TwitchUser()
        self.twitch_api = twitch_api
        self.user_login = user_login
        self.raw_user_data = await first(self.twitch_api.get_users(logins=user_login))
        if self.raw_user_data is None:
            raise UserNotFoundError
        else:
            return self

    async def get_raw_stream_data(self) -> twitchAPI.object.Stream:
        raw_stream_data = await first(self.twitch_api.get_streams(user_id=self.raw_user_data.id))
        return raw_stream_data

    async def get_stream(self) -> TwitchStream:
        raw_stream_data = await self.get_raw_stream_data()
        stream = await TwitchStream.get(raw_stream_data, self)
        return stream

    async def get_url(self) -> str:
        url = f'https://twitch.tv/{self.raw_user_data.login}'
        return url

    async def to_embed(self) -> discord.Embed:
        try:
            user_url = await self.get_url()
            embed = discord.Embed(
                title=f'**{self.raw_user_data.display_name}**',
                description=f'{self.raw_user_data.description}',
                url=user_url,
                colour=discord.Colour.purple(),
            )
            embed.add_field(
                name='Total de viewers:',
                value=f'``{self.raw_user_data.view_count}``',
                inline=True,
            )
            embed.set_image(url=self.raw_user_data.profile_image_url)
            return embed
        except UserNotFoundError:
            return None
