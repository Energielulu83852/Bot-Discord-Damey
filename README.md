# Bot Discord DownTown Cab Co
![DowntownCabCo-GTAV-Logo](https://github.com/Energielulu83852/Bot-Discord-DownTown-CabCo/assets/87243558/d7220ec5-043b-4cb1-b29f-a8f30c064251)

Ce bot a été entièrement codé par Papy Lulu, avec python et sous license MIT.
## Dépendances utilisées :
Discord.py, pytz, datetime et asyncio
## Installation
Lorsque vous souhaitez utiliser ce code, veuillez créer un fichier "config.py" et y insérer la ligne suivante : 
```
BOT_TOKEN = "votre-token-du-bot"
main_color = couleur_principale_de_votre_bot
ban_color = couleur_des_embeds_de_bannissement
unban_color = couleurs_des_embeds_de_débannissement
role_client = "role_client_du_serveur"
channel_pds_fds = "salons_des_status_des_pds_fds"
channel_airport_arrival = "salon_d'annonce_arrivee_membre"
channel_airport_departure = "salon_d'annonce_depart_membre"
channel_facture = "salon_des_factures"
espacesperso_cat = "salon_de_la_categorie_espace_perso"
name_staff = "nom_role_staff"
candid_cat = "nom_categorie_candidature"
help_cat = "nom_categorie_candidature"
role_service = "nom_role_service" 
```
Ainsi que d'installer les dépendances avec :
```
pip install discord.py pytz datetime asyncio
```
## Ses fonctionnalitées : 
Le préfix est ? et modifiable dès le début du code. Il est représenté par la suite avec [prefix].

### Différentes commandes slash : 
    - Commande BAN (restrinte au administrateurs) -> /ban
    - Commande Kick (restrinte au administrateurs) -> /Kick
    - Commande d'ajout de rôle pour un membre -> /add_role
    - Commande qui fait dire bonjour au bot -> /bonjour
    - Commande de suppression de rôle pour un membre -> /delete_role
    - Commande DM (restrinte au administrateurs) -> /dm
    - Commande Facture -> /facture
    - Commande ping -> /ping
    - Commande say -> /say
    - Commande service -> /service
    - Commande de suppression des anciens service / nettoyage du salon PDS / FDS -> /service_clear

### Commandes classiques (utilisé pour les embed avec boutons) : 
    - Commande de création de ticket aide -> [prefix]Help
    - Commande de création de ticket de candidature -> [prefix]recrutement
    - Commande de création d'un embed avec les boutons PDS / FDS -> [prefix]pds_fds

