import discord
from discord.ext import commands
from discord import app_commands

from gaymerbot.modules import Logger
from gaymerbot.views import Furry, Age, Sexuality, Notifications, Games


class RoleSelector(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Logger.get_logger('commands')

    @app_commands.command(name='menudetags', description='Envia o menu de tags')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def rolemenu(self, interaction: discord.Interaction) -> None:
        furry_embed = discord.Embed(title='🦊 » Furry', description='Você faz parte da comunidade furry ?', colour=discord.Colour.random())
        age_embed = discord.Embed(title='🔞 » Idade', description='Qual sua idade ?', colour=discord.Colour.random())
        sexuality_embed = discord.Embed(title='❤ » Orientação sexual', description='Qual sua orientação sexual ?', colour=discord.Colour.random())
        games_embed = discord.Embed(title='🎮 » Jogos', description='Quais jogos você joga ou se interessa ?', colour=discord.Colour.random())
        notification_embed = discord.Embed(title='🔔 » Notificações', description='Você deseja receber notificações ?', colour=discord.Colour.random())
        await interaction.channel.send(embed=furry_embed, view=Furry(self.client))
        await interaction.channel.send(embed=age_embed, view=Age(self.client))
        await interaction.channel.send(embed=sexuality_embed, view=Sexuality(self.client))
        await interaction.channel.send(embed=games_embed, view=Games(self.client))
        await interaction.channel.send(embed=notification_embed, view=Notifications(self.client))
        await interaction.response.send_message('Menu enviado!', ephemeral=True)


async def setup(client):
    await client.add_cog(RoleSelector(client))
