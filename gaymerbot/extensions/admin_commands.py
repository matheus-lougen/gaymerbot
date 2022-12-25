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
    async def purge(self, interaction: discord.Interaction, limit: int = 99) -> None:
        await interaction.response.send_message(f'Tem certeza que deseja limpar **{limit}** mensagens neste canal ?', view=Purge(self.client, limit, interaction.user), ephemeral=True)

    @app_commands.command(name='menudeverificacao', description='Envia o menu de verificação no canal atual')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def verifymenu(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title='Verificação', description='Clique no botão abaixo para obter acesso ao servidor!', color=discord.Colour.random())
        await interaction.channel.send(embed=embed, view=Verify(self.client))
        return await interaction.response.send_message('Menu enviado!', ephemeral=True)

    @app_commands.command(name='regras', description='Envia as regras do servidor')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def rules(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title='Regras', description='Uma lista de regras do servidor', color=discord.Colour.random())
        embed.add_field(name='Regras gerais', value='**Regras que se aplicam a todo o servidor**', inline=False)
        embed.add_field(name='``Regra 01``', value='*Proibido conteúdo NSFW ( Not Safe For Work ).*', inline=False)
        embed.add_field(name='``Regra 02``', value='*Seja legal, não provoque baderna e discussões, principalmente políticas.*', inline=False)
        embed.add_field(name='``Regra 03``', value='*Extremamente proibido qualquer tipo de ideais racistas, preconceituosos, homofóbicos e etc...*', inline=False)
        embed.add_field(name='``Regra 04``', value='*Proibido apologia a drogas, crimes e etc...*', inline=False)
        embed.add_field(name='``Regra 05``', value='*Divulgação de qualquer servidor do discord, minecraft e etc... não parceiro é extremamente proibida*', inline=False)
        embed.add_field(name='Regras de chats', value='**Regras que se aplicam aos canais de texto**', inline=False)
        embed.add_field(name='``Regra 01``', value='*Proibido Flood em qualquer chat, evite mensagens repetitivas.*', inline=False)
        embed.add_field(name='``Regra 02``', value='*Evite marcar a staff ou qualquer membro desnecessáriamente*', inline=False)
        embed.add_field(name='Regras de calls', value='**Regras que se aplicam aos canais de voz**', inline=False)
        embed.add_field(name='``Regra 01``', value='*Evite barulhos altos no seu microfone como gritos, rage, barulho de ventilador e etc..., principalmente em calls públicas pois isso atrapalha muito a conversa.*', inline=False)
        embed.add_field(name='``Regra 02``', value='*Use o bot de musica apenas nas calls de musica*', inline=False)
        await interaction.channel.send(embed=embed)
        return await interaction.response.send_message('Menu enviado!', ephemeral=True)


async def setup(client):
    await client.add_cog(admin_commands(client))
