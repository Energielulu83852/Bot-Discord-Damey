# Sous licence, crée par Lucas DE ARAUJO.

import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from discord import app_commands
import pytz
from config import BOT_TOKEN


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = "?",intents=intents)
service_start_times = {}
service_effectif=0

#ID des channels de diffusion

channel_pds_fds = "📍・pds-fds-statut" #Définir le channel de prise de service
channel_airport_arrival = "🛬・𝖡ienvenu" #Définir le salon d'annonce d'arrivé
channel_airport_departure = "👋・𝖣éparts" #Définir le salon d'annonce des départs
#channel_logs_roles = 926610730080411720 #Définir le salon des logs (Modifiaction Rôles Membres)
channel_facture = "💵・facture" #Définir le salon des factures
server_taxi = 1187497813895032902 # Définir l'ID du serveur Taxi
espacesperso_cat = "Espace perso" # Définir le nom de la catégorie où seront les espaces personnels
name_staff = "➖Direction➖" # Définir le nom du rôle Staff
candid_cat = "Equipe du taxi" # Définir le nom de la catégorie où seront les candidatures
help_cat = "Equipe du taxi" # Définir le nom de la catégorie où seront les tickets d'aide
role_service = "✅・En Service"



# Limiter commande à un serveur en particulier

def guild_only(ctx):
    return ctx.guild and ctx.guild.id == server_taxi

# Définition statut Bot

@bot.event
async def on_ready():
    print("Bot prêt à l'utilisation !")
    bot.add_view(Tickets_close())
    bot.add_view(Aide())
    bot.add_view(Tickets_rec())
    bot.add_view(PDS_FDS())
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='A votre service ! 🚕'))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Annonces arrivées / départs membres

@bot.event
@commands.check(guild_only)
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name=channel_airport_arrival)
    if channel:
        await channel.send(f'<@{member.id}>')
        embed = discord.Embed(title="Un nouveau membre est arrivé !", description=f"Bienvenu {member.name} sur le discord du Taxi | VitaLife 🚕", color=0x999999)
        embed.set_image(url="https://ih1.redbubble.net/image.846319379.2002/st,small,507x507-pad,600x600,f8f8f8.u2.jpg")
        await channel.send(embed=embed)
    roles = discord.utils.get(member.guild.roles, name="Client")
    if roles is not None:
        await member.add_roles(roles)

@bot.event
@commands.check(guild_only)
async def on_member_remove(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name=channel_airport_departure)
    if channel:
        embed = discord.Embed(title="Un membre est parti...😢", description=f"A très vite {member.name} sur le discord du Taxi | VitaLife 🚕", color=0x999999)
        embed.set_image(url="https://ih1.redbubble.net/image.846319379.2002/st,small,507x507-pad,600x600,f8f8f8.u2.jpg")
        await channel.send(embed=embed)

# Logs
"""
@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        channel = bot.get_channel(channel_logs_roles)
        if before.nick != None:
            if channel:
                embed = discord.Embed(title="Changement de Pseudo", description=f"{after.mention} à changé de pseudo : {before.nick} -> {after.mention}", color=0x808080)
                embed.set_author(name="Logs", icon_url="https://cdn.discordapp.com/avatars/847534646047932437/e192ce9e720500030d988d3f9ee1a951.png")
                await channel.send(embed=embed)
        else:
            if channel:
                embed = discord.Embed(title="Changement de Pseudo", description=f"{after.mention} à changé de pseudo : {before.mention} -> {after.nick}", color=0x808080)
                embed.set_author(name="Logs", icon_url="https://cdn.discordapp.com/avatars/847534646047932437/e192ce9e720500030d988d3f9ee1a951.png")
                await channel.send(embed=embed)
"""
# Commandes Slash Administration

@bot.tree.command(name='add_role', description='Ajouter un rôle à un membre.')
async def test(interaction: discord.Interaction, member: discord.Member, roles: discord.Role):
    if roles is not None:
        await member.add_roles(roles)
    await interaction.response.send_message(f"Rôle {roles} ajouté à __{member.name}__", ephemeral=True)

@bot.tree.command(name='delete_role', description='Retirer un rôle à un membre.')
async def test(interaction: discord.Interaction, member: discord.Member, roles: discord.Role):
    if roles is not None:
        await member.remove_roles(roles)
    await interaction.response.send_message(f"Rôle {roles} retiré à __{member.name}__", ephemeral=True)

# Commandes Slash Utilitaires

@bot.tree.command(name='ping', description="Calculer le temps de réponse du bot.", guild=None, )
async def ping(interaction: discord.Interaction):
    bot_latency = bot.latency * 1000
    await interaction.response.send_message(f"✅ Le ping est de {bot_latency:.2f} ms", ephemeral=False)

@bot.tree.command(name='bonjour', description="Dire bonjour.")
async def bonjour(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} dis bonjour ! 👋", ephemeral=False)

@bot.tree.command(name='service_clear', description="Effacer le salon des PDS / FDS.")
@commands.check(guild_only)
async def effacer(interaction: discord.Interaction, salon_id: discord.TextChannel):
    if interaction.user.guild_permissions.manage_channels:
            salon = bot.get_channel(salon_id.id)
            salon_name = salon_id.name
            salon_category = salon_id.category
            salon_permissions = salon_id.overwrites
            salon_position = salon_id.position
            if salon:
                await salon.delete()
                if isinstance(salon, discord.TextChannel):
                    new_salon = await salon_category.create_text_channel(
                        name=salon_name,
                        overwrites=salon_permissions,
                        position=salon_position
                    )
                elif isinstance(salon, discord.VoiceChannel):
                    new_salon = await salon_category.create_voice_channel(
                        name=salon_name,
                        overwrites=salon_permissions,
                        position=salon_position
                    )

                await interaction.response.send_message(f"Le salon {salon_name} a été effacé puis recréé dans la catégorie {salon_category.name}.", ephemeral=True)
            else:
                await interaction.response.send_message("Le salon spécifié n'a pas été trouvé.", ephemeral=True)
    else:
        await interaction.response.send_message("Vous n'avez pas la permission de gérer les salons.", ephemeral=True)

# Commandes Slash de modération

@bot.tree.command(name='ban', description="Bannir un membre.", guild=None)
async def ping(interaction: discord.Interaction, member: discord.Member, reason: str):
    if member == interaction.user:
        await interaction.response.send_message("Vous ne pouvez pas vous bannir vous-même.", ephemeral=True)
        return

    if member == interaction.guild.owner:
        await interaction.response.send_message("Vous ne pouvez pas bannir le propriétaire du serveur.", ephemeral=True)
        return

    try:
        await member.ban(delete_message_days=7)
        await interaction.response.send_message(f"{member.mention} a été banni avec succès. ```Raison : {reason}```", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour bannir cet utilisateur.", ephemeral=True)

@bot.tree.command(name='kick', description="Kick un membre.", guild=None)
async def unban(interaction: discord.Interaction, member: discord.Member, reason:str):
    if member == interaction.user:
        await interaction.response.send_message("Vous ne pouvez pas vous kick vous-même.", ephemeral=True)
        return

    if member == interaction.guild.owner:
        await interaction.response.send_message("Vous ne pouvez pas kick le propriétaire du serveur.", ephemeral=True)
        return

    try:
        await member.kick()
        await interaction.response.send_message(f"{member.mention} a été kick avec succès. ```Raison : {reason}```", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour bannir cet utilisateur.", ephemeral=True)

# Commande Slash statut service
        
@bot.tree.command(name="service", description="Effectif en service.")
@commands.check(guild_only)
async def service(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=role_service)

    if role:
        nombre_membres_en_service = len(role.members)
        await interaction.response.send_message(f"Il y a actuellement {nombre_membres_en_service} personne(s) en service.", ephemeral=True)
    else:
        await interaction.response.send_message("Le rôle 'En Service' n'a pas été trouvé sur ce serveur.", ephemeral=True)
    

# Commandes Slash Factures

@bot.tree.command(name="facture", description="Enregistrer une facture.")
@commands.check(guild_only)
async def service(interaction: discord.Interaction, facturation: str, photo_url: str = None):
    guild = interaction.guild
    channel = discord.utils.get(guild.channels, name=channel_facture)
    embed = discord.Embed(title="Factures", description=f"Une nouvelle facture a été déposée !", color=0x4bf542)
    embed.add_field(name="Auteur", value=f"{interaction.user.mention}")
    embed.add_field(name="Montant", value=f"{facturation}$")
    embed.set_image(url=photo_url)
    await channel.send(embed=embed)
    await interaction.response.send_message("Votre facture a bien été prise en compte !", ephemeral=True)

# Commande discussion DM

@bot.tree.command(name="dm", description="DM une personne.")
async def service(interaction: discord.Interaction, user: discord.Member, message: str):
    await user.send("**(Staff " + interaction.user.name + ") :** " + message)
    await interaction.response.send_message("Votre message a bien été envoyé !", ephemeral=True)

# Commande Boutton Espace Personnel    

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Ouvrir un dossier personnel 📁", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button:discord.ui.Button):
        position = discord.utils.get(interaction.guild.categories, name=espacesperso_cat) 
        channel = await interaction.guild.create_text_channel(f"📁・{interaction.user.name}-Espace Personnel", category=position)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
        await interaction.response.send_message(f"Dossier personnel crée <#{channel.id}>", ephemeral=True)
        await asyncio.sleep(2)
        await channel.send(f"Bienvenue sur ton espace personnel {interaction.user.mention}, un membre du staff va te donner ton matricule d'ici peu. Bienvenu parmis nous!")

@bot.command()
async def menu(ctx):
    view = Menu()
    await ctx.send(f"Clique sur le bouton __Ouvrir un dossier personnel 📁__ pour créer ton espace personnel.", view=view)
    
# Commande SAY

@bot.tree.command(name="say", description="Envoyer un message sur un salon spécifique.")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, content: str):
    if discord.utils.get(interaction.user.roles, name=name_staff):
        if channel.permissions_for(interaction.guild.me).read_messages and channel.permissions_for(interaction.guild.me).send_messages:
            await channel.send(content)
            await interaction.response.send_message(f"Message envoyé dans {channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("Le bot n'a pas les permissions nécessaires pour envoyer des messages dans ce salon.", ephemeral=True)
    else:
        await interaction.response.send_message("Vous devez être un membre du staff pour accéder à cette commande.")

# Système de Tickets - Recrutement

class Tickets_rec(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🗃️ - Déposer une candidature", style=discord.ButtonStyle.green, custom_id="recrutement")
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RecrutementForm())

class RecrutementForm(discord.ui.Modal, title="Recrutement - Informations"):
    rm_name = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label = "Nom - Prénom RP",
        required= True,
        placeholder="Nom et Prénom dans le jeu"
    )
    rm_age = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label = "Age",
        required= True,
        placeholder="Votre âge IRL"
    )
    rm_motivations = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label = "Motivations",
        required= True,
        max_length=500,
        placeholder="Donnez vos motivations"
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Votre ticket de candidature a été ouvert.", ephemeral=True)
        position = discord.utils.get(interaction.guild.categories, name=candid_cat) 
        channel = await interaction.guild.create_text_channel(f"🪪・{interaction.user.name}-Candidature", category=position)
        role = discord.utils.get(interaction.guild.roles, name=name_staff)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"Informations de : {interaction.user.name}", color=0x3366ff)
        embed.add_field(name="・Nom - Prénom RP", value=f"`{self.rm_name.value}`", inline=False)
        embed.add_field(name="・Age IRL", value=f"`{self.rm_age.value}`", inline=False)
        embed.add_field(name="・Motivations", value=f"`{self.rm_motivations.value}`", inline=False)
        await channel.send(f"Merci {interaction.user.mention} pour ton intérêt à notre société, un membre du {role.mention} va te répondre dans quelque instants.", embed=embed, view=Tickets_close())


@bot.command()
async def recrutement(ctx):
    embed = discord.Embed(title="DownTown Cab Co - Recrutements", description=f"Pour avoir une chance de rejoindre notre société, il faut respecter quelques critères importants :\n\n> • Être sérieux et responsable.\n> • Être disponible assez souvent dans la semaine. (Disponibilité à notifier dans la candidature)\n> • Être à l'écoute des ordres et ne pas manquez de respect à la hiérarchie.\n> • Être respectueux envers les civils.\n> • Être titulaire du code ainsi que du permis de voiture.\n> • Être calme attentif et à l'écoute\n> • Avoir un langage correct\n\nSi vous respectez tous ces critères et que vous souhaitez nous rejoindre, cliquez sur le bouton pour confirmer votre candidature. __*Oubliez pas de remplir le formulaire avant.*__", color=0xffff00)
    embed.set_footer(text="L'équipe du DownTown Cab Co.")
    embed.set_image(url='https://i.imgur.com/FOeB1Rl.jpg')
    embed.add_field(name="État des recrutuments", value="🟢 Actuellements ouverts.", inline=False)
    embed.add_field(name="Lien du formulaire", value="https://docs.google.com/forms/d/e/1FAIpQLSckEXklFZcd2Ctj5ZgCcJFFY8nWSgYjP8Fz0DTv9EgA-dv9hg/viewform?usp=sharing", inline=False)
    await ctx.send(embed=embed, view=Tickets_rec())

# Système de Tickets - Aide

class Aide(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❔ - Besoin d'aide", style=discord.ButtonStyle.grey, custom_id="aide")
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = await interaction.guild.create_text_channel(f"❔・{interaction.user.name}-Aide")
        role = discord.utils.get(interaction.guild.roles, name=name_staff)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
        await interaction.response.send_message(f"Votre ticket de demande d'aide a été ouvert <#{channel.id}>.", ephemeral=True)
        await asyncio.sleep(2)
        await channel.send(f"Bonjour {interaction.user.mention}, un membre du {role.mention} va te répondre dans quelque instants.", view=Tickets_close())

@bot.command()
async def Help(ctx):
    embed = discord.Embed(title="Besoin d'aide", description=f"Clique sur le bouton pour créer un ticket d'aide. __**Tout abus sera puni**__", color=0xe60000)
    embed.set_footer(text='La Direction')
    embed.set_image(url='https://i.imgur.com/FOeB1Rl.jpg')
    await ctx.send(embed=embed, view=Aide())

# Système de Tickets - Fermeture des tickets

class Tickets_close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 - Fermer le ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        await interaction.response.send_message(f"Votre ticket va être supprimé dans de brefs instants.")
        await asyncio.sleep(5)
        await channel.delete()

# Système de boutons - PDS / FDS

class PDS_FDS(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = None)
  @discord.ui.button(label="✅ - Prendre son service", style=discord.ButtonStyle.green, custom_id="on_service")
  async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
            global channel_pds_fds
            role = discord.utils.get(interaction.user.guild.roles, name=role_service)
            guild = interaction.guild
            channel = discord.utils.get(guild.channels, name=channel_pds_fds)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Bon service !", ephemeral=True)
                tz = pytz.timezone('Europe/Paris')
                service_start_times[interaction.user.id] = datetime.now(tz)
                current_time = datetime.now(tz).strftime("%H:%M")
                embed = discord.Embed(title="Prise de service", description=f"Prise de service par {interaction.user.mention}", color=0x4bf542)
                embed.add_field(name="Heure", value=f"{current_time}")
                await channel.send(embed=embed)
            else:
                await interaction.response.send_message(f"Vous êtes déjà en service.", ephemeral=True)
  @discord.ui.button(label="❌ - Prendre sa fin de service", style=discord.ButtonStyle.red, custom_id="out_service")
  async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        global channel_pds_fds
        role = discord.utils.get(interaction.user.guild.roles, name=role_service)
        guild = interaction.guild
        channel = discord.utils.get(guild.channels, name=channel_pds_fds)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Fin de service confirmé !", ephemeral=True)

            if interaction.user.id in service_start_times:
                service_start_time = service_start_times[interaction.user.id]
                tz = pytz.timezone('Europe/Paris')
                service_duration = datetime.now(tz) - service_start_time
                current_time = datetime.now(tz).strftime("%H:%M")
                embed = discord.Embed(title="Fin de service", description=f"Fin de service pris par {interaction.user.mention}", color=0xf54242)
                embed.add_field(name="Heure", value=f"{current_time}")
                embed.add_field(name="Temps de service", value=f"{service_duration.total_seconds() // 60} minutes")
                await channel.send(embed=embed)
                del service_start_times[interaction.user.id]
            else:
                await channel.send(f'{interaction.user.mention} prend sa fin de service à {datetime.now().strftime("%H:%M")}.')

        else:
            await interaction.response.send_message(f"Vous n'êtes pas en service.", ephemeral=True)


@bot.command()
async def pds_fds(ctx):
    embed = discord.Embed(title="Prises de services", description=f"Annoncer votre début de service ou fin de service à l'aide des boutons. Cela permet d'aider le staff a connaître le nombre d'effectif en service", color=0xffff00)
    embed.set_footer(text='La Direction')
    embed.set_image(url='https://i.imgur.com/FOeB1Rl.jpg')
    await ctx.send(embed = embed, view=PDS_FDS())

bot.run(BOT_TOKEN)