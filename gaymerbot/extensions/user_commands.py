
import time
import aiohttp
import discord
import datetime
from discord.ext import commands
from discord import app_commands

from gaymerbot.modules import Logger


class user_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('commands')

    @app_commands.command(name='uptime', description='Mostra o tempo que o cliente está online')
    @app_commands.guild_only()
    async def uptime(self, interaction: discord.Interaction) -> None:
        # /uptime
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - self.client.start_time))))
        await interaction.response.send_message(f'Tempo online: ``{uptime}``')

    @app_commands.command(name='ping', description='Mostra a latência do cliente')
    @app_commands.guild_only()
    async def ping(self, interaction: discord.Interaction) -> None:
        # /ping
        latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f'🏓 Pong! ``{latency}ms``')

    @app_commands.command(name='avatar', description='Envia o avatar do usuário')
    @app_commands.describe(user='O membro para enviar o avatar')
    @app_commands.rename(user='membro')
    @app_commands.guild_only()
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None) -> None:
        # avatar [user: discord.User]
        if user:
            await interaction.response.send_message(user.display_avatar)
        else:
            await interaction.response.send_message(interaction.user.display_avatar)

    @app_commands.command(name='naosei', description='sei la kkk')
    @app_commands.guild_only()
    async def naosei(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Irineu você não sabe nem eu!')

    @app_commands.command(name='rastrearip', description='Rastreia geolocalização de um endereço IP usando a Weather API')
    @app_commands.describe(ip='Endereço IP do alvo')
    @app_commands.guild_only()
    async def trackip(self, interaction: discord.Interaction, ip: str) -> None:
        # /rastrearip {ip: str}
        query = f'http://api.weatherapi.com/v1/current.json?key={self.client.config.weather_api_key}&q={ip}&aqi=no'
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(query) as r:
                    response = await r.json()
        except Exception as e:
            self.log.exception(e)
        else:
            self.log.info(response)
            if response['error']:
                error_message = response['error']['message']
                await interaction.response.send_message(f'Um erro com a API aconteceu: {error_message}')
            else:
                location = response['location']
                embed = discord.Embed(title='Rastreamento de endereço IP', description=f'Aqui estão os resultados de sua busca para o ip ``{ip}``', color=0x087500)
                embed.add_field(name='Cidade', value=location['name'], inline=True)
                embed.add_field(name='Estado', value=location['region'], inline=True)
                embed.add_field(name='País', value=location['country'], inline=True)
                embed.add_field(name='Latitude', value=location['lat'], inline=True)
                embed.add_field(name='Longitude', value=location['lon'], inline=True)
                embed.add_field(name='Hora local', value=location['localtime'], inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(client):
    await client.add_cog(user_commands(client))
