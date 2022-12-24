
import time
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
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - self.client.start_time))))
        await interaction.response.send_message(f'Tempo online: ``{uptime}``')

    @app_commands.command(name='ping', description='Mostra a latência do cliente')
    @app_commands.guild_only()
    async def ping(self, interaction: discord.Interaction) -> None:
        latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f'🏓 Pong! ``{latency}ms``')

    @app_commands.command(name='codigofonte', description='Link para o código fonte do projeto')
    @app_commands.guild_only()
    async def sourcecode(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'Sinta-se a vontade para fazer um Pull Request ou abrir um Issue!\nhttps://github.com/SystemFalll/gaymerbot')

    @app_commands.command(name='avatar', description='Envia o avatar do usuário')
    @app_commands.describe(user='O membro para enviar o avatar')
    @app_commands.rename(user='membro')
    @app_commands.guild_only()
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None) -> None:
        if user:
            await interaction.response.send_message(user.display_avatar)
        else:
            await interaction.response.send_message(interaction.user.display_avatar)


async def setup(client):
    await client.add_cog(user_commands(client))
