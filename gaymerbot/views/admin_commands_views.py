import discord


class Purge(discord.ui.View):
    def __init__(self, client, limit, user):
        self.user = user
        self.limit = limit
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label='Sim', style=discord.ButtonStyle.green, custom_id='button:purge_yes')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: remove if/else block, make interaction ephemeral
        if interaction.user.id == self.user.id:
            await interaction.response.defer()
            await interaction.channel.purge(limit=self.limit)
            await interaction.channel.send(f'**{self.limit}** mensagens foram excluídas desse canal por {interaction.user.mention}!', delete_after=10.0)
        else:
            await interaction.response.send_message('Essa interação não é sua!', ephemeral=True)

    @discord.ui.button(label='Não', style=discord.ButtonStyle.red, custom_id='button:purge_no')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: remove if/else block, make interaction ephemeral
        if interaction.user.id == self.user.id:
            await interaction.response.send_message(f'Purge cancelado!', ephemeral=True)
            await interaction.message.delete()
        else:
            await interaction.response.send_message('Essa interação não é sua!', ephemeral=True)


class Verify(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label='Verificar', style=discord.ButtonStyle.grey, custom_id='button:verify')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name='Membro'))
        await interaction.response.send_message('Verificado com sucesso!', ephemeral=True)
