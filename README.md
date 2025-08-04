# Online Chess Game

Un petit jeu d'échecs en ligne développé en Python, utilisant `pygame` pour l'interface et des sockets pour la communication réseau.

## Fonctionnalités

- Plateau d'échecs interactif
- Détection des mouvements légaux, (échecs, échec et mat, pat codé juste a corriger et rajouter)
- Partie jouable entre deux joueurs via réseau local ou à distance en ouvrant les ports
- Communication client-serveur simple via TCP sockets

## Démarrage rapide

### Lancer une partie locale

1. Ouvre un terminal et exécute le serveur :
    python server.py

2. Ouvre un deuxième terminal ou une autre machine, puis exécute le client :
    python client.py

### Jouer à distance

1. Modifier dans client.py la ligne `game = Game(is_server=False, host='127.0.0.1', port=5000)` pour que le ports et l'adresse de l'hôte correspondent.