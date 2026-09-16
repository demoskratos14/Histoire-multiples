# -*- coding: utf-8 -*-
"""
Pont entre l'application Android (Kotlin) et le serveur Flask existant.

Ce module est appele une seule fois au demarrage de l'appli (depuis
MainActivity.kt). Il :
  1. Place le repertoire de travail sur le stockage interne de l'appli
     (os.environ["HOME"], fourni automatiquement par Chaquopy), qui est
     le seul endroit inscriptible sur Android.
  2. Copie la sauvegarde de depart d'Animorph (fournie avec l'appli) dans
     le repertoire de travail -- UNIQUEMENT si l'histoire Animorph n'a pas
     encore sa propre sauvegarde -- pour que switch_story() (dans
     dice_web.py) puisse s'en servir comme point de depart la toute
     premiere fois que cette histoire est choisie, sans jamais ecraser une
     aventure deja en cours. Poudlard, elle, part toujours de zero.
  3. Importe dice_web (qui cree l'objet Flask "app", sans choisir
     d'histoire : ce sera fait par le joueur via l'ecran de selection) et
     le lance dans un thread en arriere-plan, sur 127.0.0.1:PORT (voir
     PORT ci-dessous).

Le WebView de MainActivity charge ensuite directement cette adresse : tout
se passe a l'interieur de l'application, sans jamais ouvrir de navigateur
externe.

IMPORTANT -- a propos du choix du PORT :
127.0.0.1 (la boucle locale) est partage par TOUT l'appareil Android, pas
cloisonne par application comme le reste (stockage, memoire...). Si deux
applications differentes essaient chacune de se brancher sur le meme port
pendant qu'elles tournent toutes les deux en arriere-plan, la premiere a
avoir demarre garde le port et la seconde ne peut plus se connecter --
elle reste bloquee, comme si elle ne s'ouvrait plus. Cette appli utilise
le port 5001 (libere par un ancien prototype, depuis supprime) ; l'autre
application installee en parallele utilise le port 5011 -- les deux
peuvent ainsi tourner en meme temps sans jamais se gener, meme laissees
ouvertes toutes les deux en fond.
"""

import os
import shutil
import threading
from os.path import dirname, join, exists

# Port du serveur interne de CETTE version. Doit rester different de
# celui de toute autre variante de l'appli installee en parallele sur le
# meme telephone -- voir l'explication ci-dessus. Doit correspondre
# exactement a la valeur de "serverUrl" dans MainActivity.kt.
PORT = 5001

_started = False
_lock = threading.Lock()


def start_server():
    global _started
    with _lock:
        if _started:
            return "already_running"
        _started = True

        home = os.environ["HOME"]
        os.chdir(home)

        # Seed Animorph uniquement -- Poudlard part toujours de zero, pas
        # de seed pour elle. Copie du seed dans le repertoire de travail
        # (sous son propre nom, distinct du fichier de sauvegarde final
        # "dice_state_animorph.json") -- c'est switch_story() qui decidera
        # de s'en servir ou non au moment ou Animorph est choisie.
        if not exists(join(home, "dice_state_animorph.json")):
            seed_src = join(dirname(__file__), "dice_state_seed.json")
            seed_dest = join(home, "dice_state_seed.json")
            if exists(seed_src) and not exists(seed_dest):
                shutil.copyfile(seed_src, seed_dest)

        import dice_web  # cree l'app Flask (aucune histoire choisie au demarrage)

        def _run():
            dice_web.app.run(
                host="127.0.0.1",
                port=PORT,
                debug=False,
                use_reloader=False,
                threaded=True,
            )

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return "started"
