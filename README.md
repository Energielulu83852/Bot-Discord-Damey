# Bot Discord DownTown Cab Co
![DowntownCabCo-GTAV-Logo](https://github.com/Energielulu83852/Bot-Discord-DownTown-CabCo/assets/87243558/d7220ec5-043b-4cb1-b29f-a8f30c064251)

Ce bot a été entièrement codé par Papy Lulu, avec python et sous license MIT.
## Dépendances utilisées :
Discord.py, pytz, datetime et asyncio
## Installation
Lorsque vous souhaitez utiliser ce code, veuillez créer un fichier "config.py" et y insérer la ligne suivante : 
```
BOT_TOKEN = "votre-token-du-bot"
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

