import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import pytz
import discord_timestamps
from config import BOT_TOKEN, role_recrutement, prefix, url_logo_entreprise ,url_image_entreprise, entreprise_name, main_color, ban_color, unban_color, role_client, channel_pds_fds, channel_airport_arrival, channel_airport_departure, channel_facture, espacesperso_cat, name_staff, candid_cat, help_cat, role_service 


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = prefix,intents=intents)
service_start_times = {}
service_effectif=0
personnes_service = []


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
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name=channel_airport_arrival)
    if channel:
        name_srv = member.guild.name
        await channel.send(f'<@{member.id}>')
        embed = discord.Embed(title="Un nouveau membre est arrivé !", description=f"Bienvenu {member.name} sur le discord {name_srv}", color=0x14ca13)
        embed.set_image(url="https://ih1.redbubble.net/image.846319379.2002/st,small,507x507-pad,600x600,f8f8f8.u2.jpg")
        await channel.send(embed=embed)
    roles = discord.utils.get(member.guild.roles, name=role_client)
    if roles is not None:
        await member.add_roles(roles)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name=channel_airport_departure)
    if channel:
        name_srv = member.guild.name
        embed = discord.Embed(title="Un membre est parti...😢", description=f"A très vite {member.name} sur le discord {name_srv}", color=0x999999)
        embed.set_image(url="https://ih1.redbubble.net/image.846319379.2002/st,small,507x507-pad,600x600,f8f8f8.u2.jpg")
        await channel.send(embed=embed)

# Commande Help

@bot.tree.command(name='help', description='Donne des indication sur le fonctionnement du bot.')
async def test(interaction: discord.Interaction):
    embed = discord.Embed(description=f"Bienvenu sur la commande Aide, vous trouverez ici toutes les commandes ainsi que leur fonctionnement et utilité.\n\n • **/add_role** : (Réservé au Staff) Ajouter un rôle à un membre.\n • **/ban** : (Réservé au Staff) Banni un membre.\n • **/bonjour** : Dit bonjour dans le salon où la commande est exécutée.\n • **/delete_role** : (Réservé au Staff) Supprimer le rôle d'un membre.\n • **/dm** : (Réservé au Staff) Envoyer un message privé avec le bot à un membre du serveur.\n • **/facture** : Créer une nouvelle facture.\n • **/kick** : (Réservé au Staff) Permet d'exclure un membre du serveur.\n • **/ping** : Permet de connaître le ping entre vous et le bot.\n • **/say** : (Réservé au Staff) Permet d'envoyer un message à l'aide du bot.\n • **/service** : Permet de connaître le nombre de personnes en service.\n • **/service_clear** : (Réservé au Staf) Permet de nettoyer le salon des PDS et FDS.\n • **/unban** : (Réservé au Staff) Permet de débannir un joueur\n • **{prefix}Help** : (Réservé au Staff) Permet de créer l'embed Aide dans le salon où est executé la commande\n • **{prefix}recrutement** : (Réservé au Staff) Permet de créer l'embed pour les recrutements\n • **{prefix}pds_fds** : (Réservé au Staff) Permet de créer l'embed pour les prises et fin de service\n • **{prefix}recrutement_on** : (Réservé au Staff) Permet de rendre possible le dépot de CV sur l'embed recrutement\n • **{prefix}recrutement_off** : (Réservé au Staff) Permet de ne plus rendre accessible le dépot de CV sur l'embed recrutement", color=main_color)
    embed.set_author(name="Commande Aide", icon_url=url_logo_entreprise)
    embed.set_footer(text=bot.user.name)
    await interaction.response.send_message(embed=embed)


# Commandes Slash Administration

@bot.tree.command(name='add_role', description='Ajouter un rôle à un membre.')
@discord.app_commands.describe(member = "Pseudo du membre")
@discord.app_commands.describe(roles = "Rôle à ajouter")
async def test(interaction: discord.Interaction, member: discord.Member, roles: discord.Role):
    if interaction.user.guild_permissions.moderate_members:
        if roles is not None:
            await member.add_roles(roles)
        await interaction.response.send_message(f"Rôle {roles} ajouté à __{member.name}__", ephemeral=True)
    else : 
        await interaction.response.send_message(f"Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

@bot.tree.command(name='delete_role', description='Retirer un rôle à un membre.')
@discord.app_commands.describe(member = "Pseudo du membre")
@discord.app_commands.describe(roles = "Rôle à supprimer")
async def test(interaction: discord.Interaction, member: discord.Member, roles: discord.Role):
    if interaction.user.guild_permissions.moderate_members:
        if roles is not None:
            await member.remove_roles(roles)
        await interaction.response.send_message(f"Rôle {roles} retiré à __{member.name}__", ephemeral=True)
    else : 
        await interaction.response.send_message(f"Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

# Commandes Slash Utilitaires

@bot.tree.command(name='ping', description="Calculer le temps de réponse du bot.", guild=None, )
async def ping(interaction: discord.Interaction):
    bot_latency = bot.latency * 1000
    embed = discord.Embed(description=f"✅ Le ping est de **{bot_latency:.1f}**ms", color=main_color)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='bonjour', description="Dire bonjour.")
async def bonjour(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} dis bonjour ! 👋", ephemeral=False)

@bot.tree.command(name='service_clear', description="Effacer le salon des PDS / FDS.")
async def effacer(interaction: discord.Interaction):
    if interaction.user.guild_permissions.manage_channels:
            salon = discord.utils.get(interaction.guild.channels, name=channel_pds_fds)
            salon_name = channel_pds_fds
            salon_category = salon.category
            salon_permissions = salon.overwrites
            salon_position = salon.position
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

                await interaction.response.send_message(f"Le salon `{salon_name}` a été effacé puis recréé dans la catégorie `{salon_category.name}`.", ephemeral=True)
            else:
                await interaction.response.send_message("Le salon spécifié n'a pas été trouvé.", ephemeral=True)
    else:
        await interaction.response.send_message("Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

# Commandes Slash de modération

@bot.tree.command(name='ban', description="Bannir un membre.")
@discord.app_commands.describe(membre = "Pseudo du membre")
@discord.app_commands.describe(raison = "Raison du bannissement")
async def ping(interaction: discord.Interaction, membre: discord.Member, raison: str):
    if interaction.user.guild_permissions.ban_members:
        if membre == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous bannir vous-même.", ephemeral=True)
            return

        if membre == interaction.guild.owner:
            await interaction.response.send_message("Vous ne pouvez pas bannir le propriétaire du serveur.", ephemeral=True)
            return

        try:
            await membre.ban(delete_message_days=7, reason=raison)
            embed = discord.Embed(title="Bannisement", description=f"L'utilisateur `{membre}` à été **banni**\n > Raison: {raison}", color=ban_color)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour bannir cet utilisateur.", ephemeral=True)
    else:
        await interaction.response.send_message("Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

@bot.tree.command(name='kick', description="Kick un membre.")
@discord.app_commands.describe(member = "Pseudo du membre")
@discord.app_commands.describe(reason = "Raison du kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason:str):
    if interaction.user.guild_permissions.kick_members:
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous kick vous-même.", ephemeral=True)
            return

        if member == interaction.guild.owner:
            await interaction.response.send_message("Vous ne pouvez pas kick le propriétaire du serveur.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="Expulsion", description=f"L'utilisateur `{member}` à été **kick**\n > Raison: {reason}", color=ban_color)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour kick cet utilisateur.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

@bot.tree.command(name='unban', description='Débanir un membre.')
@discord.app_commands.describe(user_id = "ID de l'utilisateur")
async def unban(interaction: discord.Interaction, user_id: str):
    user = await bot.fetch_user(user_id)
    if interaction.user.guild_permissions.ban_members:
        try:
            await interaction.guild.unban(user)
            embed = discord.Embed(title="Débannissement", description=f"L'utilisateur `({user})` a été **débanni**.", color=unban_color)
            await interaction.response.send_message(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message(f"L'utilisateur {user.mention} n'est pas actuellement banni.")
        except discord.Forbidden:
            await interaction.response.send_message("Le bot n'a pas les permissions nécessaires pour débannir cet utilisateur.")
    else:
        await interaction.response.send_message("Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)


# Commande Slash statut service
        
@bot.tree.command(name="service", description="Effectif en service.")
async def service(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=role_service)
    if role:
        nombre_membres_en_service = len(role.members)
        await interaction.response.send_message(f"Il y a actuellement {nombre_membres_en_service} personne(s) en service.", ephemeral=True)
    else:
        await interaction.response.send_message("Le rôle 'En Service' n'a pas été trouvé sur ce serveur.", ephemeral=True)
    

# Commandes Slash Factures

@bot.tree.command(name="facture", description="Enregistrer une facture.")
@discord.app_commands.describe(facturation = "Prix de la facture.")
@discord.app_commands.describe(photo_url = "URL de la capture de la facture.") 
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
@discord.app_commands.describe(user = "Utilisateur à DM.")
@discord.app_commands.describe(message = "Message à envoyer.")
@discord.app_commands.describe(image = "Lien de l'image à envoyer.")
async def service(interaction: discord.Interaction, user: discord.Member, message: str, image: discord.Attachment = None):
    if interaction.user.guild_permissions.administrator:
        if image:
            image_send = await image.to_file()
            await user.send("**(Staff " + interaction.user.name + ") :** " + message, file = image_send)
        else :
            await user.send("**(Staff " + interaction.user.name + ") :** " + message)
        await interaction.response.send_message("Votre message a bien été envoyé !", ephemeral=True)
    else:
        await interaction.response.send_message(f"Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)
 
# Commande SAY

@bot.tree.command(name="say", description="Envoyer un message sur un salon spécifique.")
@discord.app_commands.describe(channel = "Salon où envoyer le message.")
@discord.app_commands.describe(content = "Contenu du message.")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, content: str):
    if interaction.user.guild_permissions.manage_messages:
        if discord.utils.get(interaction.user.roles, name=name_staff):
            if channel.permissions_for(interaction.guild.me).read_messages and channel.permissions_for(interaction.guild.me).send_messages:
                await channel.send(content)
                await interaction.response.send_message(f"Message envoyé dans {channel.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Le bot n'a pas les permissions nécessaires pour envoyer des messages dans ce salon.", ephemeral=True)
        else:
            await interaction.response.send_message("Vous devez être un membre du staff pour accéder à cette commande.")
    else:
        await interaction.response.send_message(f"Vous n'avez pas les permissions nécessaires pour éxecuter cette commande.", ephemeral=True)

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
    role = discord.utils.get(ctx.author.roles, name=role_recrutement)
    if ctx.author.guild_permissions.administrator or role :
        embed = discord.Embed(title=f"{entreprise_name} - Recrutements", description=f"Pour avoir une chance de rejoindre notre société, il faut respecter quelques critères importants :\n\n> • Être sérieux et responsable.\n> • Être disponible assez souvent dans la semaine. (Disponibilité à notifier dans la candidature)\n> • Être à l'écoute des ordres et ne pas manquez de respect à la hiérarchie.\n> • Être respectueux envers les civils.\n> • Être titulaire du code ainsi que du permis de voiture.\n> • Être calme attentif et à l'écoute\n> • Avoir un langage correct\n\nSi vous respectez tous ces critères et que vous souhaitez nous rejoindre, cliquez sur le bouton pour confirmer votre candidature. __*Vous devrez remplir un formulaire après avoir cliqué sur le bouton.*__", color=main_color)
        embed.set_footer(text=f"L'équipe du {entreprise_name}.")
        embed.set_image(url=url_image_entreprise)
        embed.add_field(name="État des recrutuments", value="🔴 Actuellements fermés.", inline=False)
        await ctx.send(embed=embed, view=Tickets_rec())

@bot.command()
async def recrutement_on(ctx, id: int):
    role = discord.utils.get(ctx.author.roles, name=role_recrutement)
    if ctx.author.guild_permissions.administrator or role :
        channel = ctx.channel
        message_to_edit = await channel.fetch_message(id)
        embed = discord.Embed(title=f"{entreprise_name} - Recrutements", description=f"Pour avoir une chance de rejoindre notre société, il faut respecter quelques critères importants :\n\n> • Être sérieux et responsable.\n> • Être disponible assez souvent dans la semaine. (Disponibilité à notifier dans la candidature)\n> • Être à l'écoute des ordres et ne pas manquez de respect à la hiérarchie.\n> • Être respectueux envers les civils.\n> • Être titulaire du code ainsi que du permis de voiture.\n> • Être calme attentif et à l'écoute\n> • Avoir un langage correct\n\nSi vous respectez tous ces critères et que vous souhaitez nous rejoindre, cliquez sur le bouton pour confirmer votre candidature. __*Vous devrez remplir un formulaire après avoir cliqué sur le bouton.*__", color=main_color)
        embed.set_footer(text=f"L'équipe du {entreprise_name}.")
        embed.set_image(url=url_image_entreprise)
        embed.add_field(name="État des recrutuments", value="🟢 Actuellements ouverts.", inline=False)
        await message_to_edit.edit(embed=embed, view=Tickets_rec())

@bot.command()
async def recrutement_off(ctx, id: int):
    role = discord.utils.get(ctx.author.roles, name=role_recrutement)
    if ctx.author.guild_permissions.administrator or role :
        channel = ctx.channel
        message_to_edit = await channel.fetch_message(id)
        embed = discord.Embed(title=f"{entreprise_name} - Recrutements", description=f"Pour avoir une chance de rejoindre notre société, il faut respecter quelques critères importants :\n\n> • Être sérieux et responsable.\n> • Être disponible assez souvent dans la semaine. (Disponibilité à notifier dans la candidature)\n> • Être à l'écoute des ordres et ne pas manquez de respect à la hiérarchie.\n> • Être respectueux envers les civils.\n> • Être titulaire du code ainsi que du permis de voiture.\n> • Être calme attentif et à l'écoute\n> • Avoir un langage correct\n\nSi vous respectez tous ces critères et que vous souhaitez nous rejoindre, cliquez sur le bouton pour confirmer votre candidature. __*Vous devrez remplir un formulaire après avoir cliqué sur le bouton.*__", color=main_color)
        embed.set_footer(text=f"L'équipe du {entreprise_name}.")
        embed.set_image(url=url_image_entreprise)
        embed.add_field(name="État des recrutuments", value="🔴 Actuellements fermés.", inline=False)
        await message_to_edit.edit(embed=embed, view=None)

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
    if ctx.author.guild_permissions.administrator :
        embed = discord.Embed(title="Besoin d'aide", description=f"Clique sur le bouton pour créer un ticket d'aide. __**Tout abus sera puni**__", color=0xe60000)
        embed.set_footer(text='La Direction')
        embed.set_image(url=url_image_entreprise)
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
                '''tz = pytz.timezone('Europe/Paris')
                service_start_times[interaction.user.id] = datetime.now(tz)
                current_time = datetime.now(tz).strftime("%H:%M")
                embed = discord.Embed(title="Prise de service", description=f"Prise de service par {interaction.user.mention}", color=0x4bf542)
                embed.add_field(name="Heure", value=f"{current_time}")
                await channel.send(embed=embed)'''
                tz = pytz.timezone('Europe/Paris')
                current_time = datetime.now(tz)
                current_timestamp = int(datetime.now(tz).timestamp())
                personnes_service.append([interaction.user.id,current_timestamp])
                if personnes_service:
                    utilisateurs = "\n".join([f"<@{user_id[0]}> | Depuis : <t:{user_id[1]}:R>" for user_id in personnes_service])
                    description = f"Voici les utilisateurs actuellement en service :\n{utilisateurs}"
                else:
                    description = "_Personne n'est en service ... :(_"
                embed = discord.Embed(
                    title='🔎 Utilisateurs en service (0) :', 
                    description=description, 
                    color=main_color, 
                    timestamp=current_time)
                embed.set_footer(text=f'La Direction')
                embed.set_author(name=entreprise_name, icon_url=url_logo_entreprise)
                await bot.saved_message_pds_fds.edit(embed=embed)
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

            '''if interaction.user.id in service_start_times:
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
                tz = pytz.timezone('Europe/Paris')
                current_time = datetime.now(tz).strftime("%H:%M")
                embed = discord.Embed(title="Fin de service", description=f"Fin de service pris par {interaction.user.mention}", color=0xf54242)
                embed.add_field(name="Heure", value=f"{current_time}")
                await channel.send(embed=embed)'''
            for i in range(len(personnes_service)):
                if interaction.user.id == personnes_service[i][0]:
                    personnes_service.pop(i)
            tz = pytz.timezone('Europe/Paris')
            current_time = datetime.now(tz)
            current_timestamp = int(datetime.now(tz).timestamp())
            if personnes_service:
                utilisateurs = "\n".join([f"<@{user_id[0]}> | Depuis : <t:{user_id[1]}:R>" for user_id in personnes_service[0]])
                description = f"Voici les utilisateurs actuellement en service :\n{utilisateurs}"
            else:
                description = "_Personne n'est en service ... :(_"
            embed = discord.Embed(
                title='🔎 Utilisateurs en service (0) :', 
                description=description, 
                color=main_color, 
                timestamp=current_time)
            embed.set_footer(text=f'La Direction')
            embed.set_author(name=entreprise_name, icon_url=url_logo_entreprise)
            await bot.saved_message_pds_fds.edit(embed=embed)

        else:
            await interaction.response.send_message(f"Vous n'êtes pas en service.", ephemeral=True)


@bot.command()
async def pds_fds(ctx):
    if ctx.author.guild_permissions.administrator :
        tz = pytz.timezone('Europe/Paris')
        current_time = datetime.now(tz)
        embed = discord.Embed(title='🔎 Utilisateurs en service (0) :', description=f"_Personne n'est en service ... :(_", color=main_color, timestamp=current_time)
        embed.set_footer(text=f'La Direction')
        embed.set_author(name=entreprise_name, icon_url=url_logo_entreprise)
        message = await ctx.send(embed = embed, view=PDS_FDS())
        bot.saved_message_pds_fds = message

bot.run(BOT_TOKEN)