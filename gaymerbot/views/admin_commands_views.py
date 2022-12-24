"""View classes from discord.py module"""

import discord


class Purge(discord.ui.View):
    def __init__(self, client, limit, user):
        # User object that sent the command
        self.user = user
        # Limit of messages to purge
        self.limit = limit
        self.client = client
        # Calling the constructor method from the base class
        super().__init__(timeout=None)

    @discord.ui.button(label='Sim', style=discord.ButtonStyle.green, custom_id='button:purge_yes')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the user pressing the button is the same that sent the command
        if interaction.user.id == self.user.id:
            await interaction.response.defer()
            await interaction.channel.purge(limit=self.limit)
            await interaction.channel.send(f'**{self.limit}** mensagens foram excluídas desse canal por {interaction.user.mention}!', delete_after=10.0)
        else:
            await interaction.response.send_message('Essa interação não é sua!', ephemeral=True)

    @discord.ui.button(label='Não', style=discord.ButtonStyle.red, custom_id='button:purge_no')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the user pressing the button is the same that sent the command
        if interaction.user.id == self.user.id:
            await interaction.response.send_message(f'Purge cancelado!', ephemeral=True)
            await interaction.message.delete()
        else:
            await interaction.response.send_message('Essa interação não é sua!', ephemeral=True)


class Verify():
    def __init__(self, client):
        self.client = client

    @discord.ui.button(label='Verificar', style=discord.ButtonStyle.green, custom_id='button:verify')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name='Membro'))
        await interaction.response.send_message('Verificado com sucesso!', ephemeral=True)
