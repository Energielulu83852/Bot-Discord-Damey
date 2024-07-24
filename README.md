# Bot Discord Damey
![Logo_bot_Lucas](https://github.com/user-attachments/assets/82cd4a32-ec53-4d72-b785-97a568c045a3)

Ce bot a été entièrement codé par Papy Lulu, avec python et sous licence MIT.
## Dépendances utilisées :
Discord.py, pytz, datetime et asyncio
## Installation
Lorsque vous souhaitez utiliser ce code, veuillez créer un fichier "config.py" et y insérer les lignes suivantes : 
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
entreprise_name = "nom de l'entreprise"
url_image_entreprise = "une image représentant l'entreprise"
url_logo_entreprise = "le logo de l'entreprises" 
prefix = "le prefix que vous souhaitez"
role_recrutement = "nom du rôle du responsable recrutement"
```
Ainsi que d'installer les dépendances avec :
```
pip install discord.py pytz datetime asyncio
```
## Ses fonctionnalitées : 
Le préfix est ? et il est modifiable dès le début du code. Il est représenté par la suite avec [prefix].

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
    - Commande de modification de l'embed des recrutements (recrutements ouverts) -> [prefix]recrutement_on
    - Commande de modification de l'embed des recrutements (recrutements fermés) -> [prefix]recrutement_off

## Si vous souhaitez soutenir le projet : 
Si vous souhaitez soutenir le projet, voici le lien de mon compte PayPal : https://paypal.me/ldaraujo?country.x=FR&locale.x=fr_FR
