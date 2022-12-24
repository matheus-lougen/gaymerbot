import discord
from discord import utils
# from discord.ext import commands

from gaymerbot.modules import Logger

log = Logger.get_logger('commands')


class Interaction():
    """docstring for User"""

    def __init__(self, interaction):
        self.interaction = interaction

    async def fetch_option(self, name, values):
        if name == 'skip':
            return await self.defer()
        if name in values:
            return await self.add_role(name)
        else:
            return await self.remove_role(name)

    async def defer(self):
        if self.interaction.response.is_done():
            return
        elif not self.interaction.response.is_done():
            return await self.interaction.response.defer()

    async def add_role(self, name):
        role = utils.get(self.interaction.guild.roles, name=name)
        await self.interaction.user.add_roles(role)
        return await self.defer()

    async def remove_role(self, name):
        role = utils.get(self.interaction.guild.roles, name=name)
        await self.interaction.user.remove_roles(role)
        return await self.defer()


class Age(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='+18', value='+18', description='Eu tenho 18 anos ou mais', emoji='➡'),
        discord.SelectOption(label='-18', value='-18', description='Eu tenho menos de 18 anos', emoji='➡'),
        discord.SelectOption(label='Prefiro não dizer', value='skip', description='Prefiro não informar minha idade', emoji='➡')
    ]

    @discord.ui.select(cls=discord.ui.Select, placeholder='Escolha uma opção', min_values=1, max_values=1, options=options, custom_id='dropdown:age')
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        interaction = Interaction(interaction)
        await interaction.fetch_option('+18', select.values)
        await interaction.fetch_option('-18', select.values)
        await interaction.fetch_option('skip', select.values)


class Sexuality(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='Heterossexual', value='Heterossexual', description='Atração pelo sexo oposto', emoji='➡'),
        discord.SelectOption(label='Homosexual', value='Homossexual', description='Atração pelo mesmo sexo', emoji='➡'),
        discord.SelectOption(label='Bisexual', value='Bissexual', description='Atração por ambos os sexos', emoji='➡'),
        discord.SelectOption(label='Pansexual', value='Panssexual', description='Atração independente do sexo', emoji='➡'),
        discord.SelectOption(label='Prefiro não dizer', value='skip', description='Prefiro não informar minha orientação sexual', emoji='➡')
    ]

    @discord.ui.select(cls=discord.ui.Select, placeholder='Escolha uma opção', min_values=1, max_values=1, options=options, custom_id='dropdown:sexuality')
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        interaction = Interaction(interaction)
        await interaction.fetch_option('Heterossexual', select.values)
        await interaction.fetch_option('Homossexual', select.values)
        await interaction.fetch_option('Bissexual', select.values)
        await interaction.fetch_option('Panssexual', select.values)
        await interaction.fetch_option('skip', select.values)


class Furry(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='Sim', value='Furry', description='Eu faço parte da comunidade Furry', emoji='➡'),
        discord.SelectOption(label='Não', value='NãoFurry', description='Eu não faço parte da comunidade Furry', emoji='➡')
    ]

    @discord.ui.select(cls=discord.ui.Select, placeholder='Escolha uma opção', min_values=1, max_values=1, options=options, custom_id='dropdown:furry')
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        interaction = Interaction(interaction)
        await interaction.fetch_option('Furry', select.values)
        await interaction.fetch_option('NãoFurry', select.values)


class Notifications(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='Sim', value='Noticações', description='Eu quero receber notificações sobre coisas novas', emoji='➡'),
        discord.SelectOption(label='Não', value='skip', description='Eu não quero receber notificações sobre coisas novas', emoji='➡')
    ]

    @discord.ui.select(cls=discord.ui.Select, placeholder='Escolha uma ou mais opções', min_values=1, max_values=1, options=options, custom_id='dropdown:notifications')
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        interaction = Interaction(interaction)
        await interaction.fetch_option('Noticações', select.values)
        await interaction.fetch_option('skip', select.values)


class Games(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='Minecraft', value='Minecraft', description='', emoji='➡'),
        discord.SelectOption(label='Valorant', value='Valorant', description='', emoji='➡'),
        discord.SelectOption(label='Warzone', value='Warzone', description='', emoji='➡'),
        discord.SelectOption(label='Pubg', value='Pubg', description='', emoji='➡'),
        discord.SelectOption(label='Roblox', value='Roblox', description='', emoji='➡'),
        discord.SelectOption(label='Factorio', value='Factorio', description='', emoji='➡'),
        discord.SelectOption(label='Outros', value='skip', description='', emoji='➡')
    ]

    @discord.ui.select(cls=discord.ui.Select, placeholder='Escolha uma ou mais opções', min_values=1, max_values=7, options=options, custom_id='dropdown:games')
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        interaction = Interaction(interaction)
        await interaction.fetch_option('Minecraft', select.values)
        await interaction.fetch_option('Valorant', select.values)
        await interaction.fetch_option('Warzone', select.values)
        await interaction.fetch_option('Pubg', select.values)
        await interaction.fetch_option('Roblox', select.values)
        await interaction.fetch_option('Factorio', select.values)
        await interaction.fetch_option('skip', select.values)
