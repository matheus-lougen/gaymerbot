
import discord
from discord.ext import commands
from discord import app_commands

from gaymerbot.modules import Logger
from gaymerbot.views import Purge, Verify


class admin_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('commands')

    @app_commands.command(name='limpar', description='Limpa tudo no canal')
    @app_commands.describe(limit='A quantidade de mensagens que deseja limpar')
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.rename(limit='limite')
    @app_commands.guild_only()
    # /purge [limit]
    async def purge(self, interaction: discord.Interaction, limit: int = 99) -> None:
        await interaction.response.send_message(f'Tem certeza que deseja limpar **{limit}** mensagens neste canal ?')
        await interaction.edit_original_response(view=Purge(self.client, limit, interaction.user))

    @app_commands.command(name='menudeverificacao', description='Envia o menu de verificação no canal atual')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def verifymenu(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title='Verificação', description='Clique no botão abaixo para obter acesso ao servidor!', color=0x087500)
        await interaction.channel.send(embed=embed, view=Verify(self.client))


async def setup(client):
    await client.add_cog(admin_commands(client))
