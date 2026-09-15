# -*- coding: utf-8 -*-
"""
STORIES - registre des histoires disponibles dans l'application
=================================================================
Chaque histoire partage EXACTEMENT le meme moteur de jeu (dice_engine.py)
et la meme interface (dice_web.py) -- seuls changent, par histoire :
  - l'image de fond,
  - le fichier de sauvegarde (chaque histoire garde sa propre partie),
  - le roster de totems de depart (Animorph part avec les siens deja
    acquis ; Poudlard part de zero, tout se construit en jouant),
  - le texte de contexte specifique a l'univers, envoye a l'IA narratrice.

La cle API Mistral, elle, N'EST PAS ici : elle est partagee entre toutes
les histoires (voir app_config.json / load_app_config() dans dice_web.py),
puisqu'un seul compte gratuit suffit largement pour les deux.

Ajouter une troisieme histoire plus tard = ajouter une entree ici, sans
toucher au reste du code.
"""

from bg_animorph_data import BG_IMAGE_B64 as _ANIMORPH_BG
from bg_poudlard_data import BG_IMAGE_B64 as _POUDLARD_BG


# ---------------------------------------------------------------------
# ANIMORPH (histoire d'origine)
# ---------------------------------------------------------------------

ANIMORPH_PIP_SYMBOLS = {
    "araignee":    {"emoji": "\U0001f577\ufe0f", "label": "Araignee (Spider-Man)"},
    "aigle":       {"emoji": "\U0001f985", "label": "Aigle"},
    "loup":        {"emoji": "\U0001f43a", "label": "Loup"},
    "renard":      {"emoji": "\U0001f98a", "label": "Renard"},
    "jaguar":      {"emoji": "\U0001f406", "label": "Jaguar"},
    "bond":        {"emoji": "\U0001f998", "label": "Grand Bond"},
    "profondeurs": {"emoji": "\U0001f42c", "label": "Profondeurs"},
    "patte":       {"emoji": "\U0001f43e", "label": "Emblazon d'Animorph"},
    "bouclier":    {"emoji": "\U0001f6e1\ufe0f", "label": "Bouclier (Captain America)"},
    "etoile":      {"emoji": "\U0001f31f", "label": "Etoile (Shuri / Wakanda)"},
}

ANIMORPH_TOTEMS = [
    {
        "key": "aigle", "icon": "\U0001f985", "label": "Aigle \u2014 Maitre des Courants",
        "powers": ["Vol", "Vision exceptionnelle", "Grande vitesse aerienne",
                   "Controle des courants d'air", "Creation de rafales",
                   "Vol plus precis et rapide"],
        "special": "\U0001f32c\ufe0f Ascension Absolue \u2014 Permet de monter tres haut "
                   "et d'observer toute une zone depuis le ciel.",
    },
    {
        "key": "loup", "icon": "\U0001f43a", "label": "Loup",
        "powers": ["Grande force", "Endurance", "Odorat tres developpe",
                   "Instinct de protection", "Detection et suivi de pistes"],
        "special": "",
    },
    {
        "key": "renard", "icon": "\U0001f98a", "label": "Renard",
        "powers": ["Agilite", "Discretion", "Ruse", "Precision",
                   "Intelligence tactique"],
        "special": "",
    },
    {
        "key": "jaguar", "icon": "\U0001f406", "label": "Jaguar / Jaguar Astral",
        "powers": ["Vision nocturne parfaite", "Intuition du danger",
                   "Perception spirituelle", "Communication mentale avec Gabin",
                   "Conseils et guidance"],
        "special": "\U0001f30c Fureur Astrale \u2014 Une fois par aventure, augmente "
                   "fortement les reflexes, la vitesse et la lucidite de Gabin.",
    },
    {
        "key": "bond", "icon": "\U0001f998", "label": "Totem du Grand Bond",
        "powers": ["Sauts extremement hauts", "Sauts extremement longs",
                   "Atterrissages maitrises", "Grande mobilite",
                   "Possibilite de transporter un allie pendant un bond"],
        "special": "",
    },
    {
        "key": "profondeurs", "icon": "\U0001f42c", "label": "Totem des Profondeurs",
        "powers": ["Respiration sous l'eau", "Grande vitesse aquatique",
                   "Resistance a la pression", "Perception des vibrations sous-marines",
                   "Echo-sens"],
        "special": "\U0001f30a Vague Primordiale \u2014 Creation d'une puissante onde "
                   "aquatique pouvant repousser des ennemis et modifier les courants.",
    },
]

ANIMORPH_FIXED_ALLIES_LINE = (
    "\U0001f577\ufe0fAraignee=allie Spider-Man | \U0001f6e1\ufe0fBouclier=allie "
    "Captain America | \U0001f31fEtoile=allie Shuri (Wakanda) | "
    "\U0001f43ePatte (Emblazon d'Animorph)=pas d'allie exterieur, declenche "
    "'Second Souffle' (relance immediatement le dernier lancer de reussite)."
)

ANIMORPH_ALLY_HELP_TEXT = {
    "araignee": "\U0001f577\ufe0f Spider-Man intervient a vos cotes !",
    "bouclier": "\U0001f6e1\ufe0f Captain America vient preter main-forte !",
    "etoile": "\U0001f31f Shuri envoie une aide high-tech depuis le Wakanda !",
}

ANIMORPH_LORE_PARAGRAPHS = [
    "UNIVERS : l'aventure se deroule dans l'univers Marvel. Tu peux y faire "
    "intervenir d'autres personnages Marvel au fil de l'histoire (nouvelles "
    "rencontres, alliances ponctuelles), en plus des trois allies deja lies "
    "a un symbole fixe (Araignee=Spider-Man, Bouclier=Captain America, "
    "Etoile=Shuri). Tous les totems listes ci-dessus sont deja acquis par "
    "Gabin des le debut de l'aventure (ce ne sont pas des decouvertes a "
    "venir).",

    "NOUVEAUX TOTEMS : quand une quete secondaire de type 'objet' est menee "
    "a terme, c'est l'occasion ideale d'inventer la rencontre d'un nouveau "
    "totem animal pour Gabin (nom, apparence, pouvoirs de ton invention) -- "
    "raconte cette decouverte dans l'histoire. Le joueur l'ajoutera ensuite "
    "lui-meme dans l'application une fois le chapitre termine (nouvelle "
    "jauge, image...) : tu n'as donc rien a gerer mecaniquement pour lui, "
    "juste a le raconter. S'il apparait plus tard dans la liste des "
    "TOTEMS/ALLIES ci-dessus (le joueur l'aura alors ajoute), integre-le "
    "naturellement a partir de ce moment-la, sans revenir sur les chapitres "
    "precedents ou il n'existait pas encore.",
]


# ---------------------------------------------------------------------
# POUDLARD (nouvelle histoire)
# ---------------------------------------------------------------------

# Un seul totem de depart : la baguette magique, recuperee des l'arrivee
# a Poudlard. Tous les autres se construisent en jouant, via le meme
# systeme de totems personnalises que sur Animorph (voir add_custom_totem
# dans dice_engine.py) -- utilise ici pour les amis, les creatures
# fantastiques ET les sorts appris en cours.
POUDLARD_PIP_SYMBOLS = {
    "baguette": {"emoji": "\U0001fa84", "label": "Baguette Magique"},
}
POUDLARD_TOTEMS = [
    {
        "key": "baguette", "icon": "\U0001fa84", "label": "Baguette Magique",
        "powers": ["premiers sorts", "concentration magique"],
        "special": "Second Sort \u2014 relance immediatement le dernier lancer de reussite.",
    },
]
POUDLARD_FIXED_ALLIES_LINE = ""

POUDLARD_LORE_PARAGRAPHS = [
    "UNIVERS : l'aventure se deroule dans l'univers de Harry Potter. Elle "
    "commence par l'arrivee du personnage a Poudlard, jusqu'a sa "
    "repartition par le Choixpeau magique dans l'une des 4 maisons "
    "(Gryffondor, Serdaigle, Poufsouffle, Serpentard). Si le prenom du "
    "personnage n'est pas encore connu au moment ou tu ecris cette scene, "
    "demande-le au joueur avant la repartition (par exemple via une "
    "question posee par un professeur ou par le Choixpeau lui-meme), "
    "plutot que d'en inventer un toi-meme.",

    "BAGUETTE MAGIQUE : des son arrivee (par exemple chez un marchand de "
    "baguettes), le personnage recoit sa baguette -- c'est son premier "
    "totem, deja acquis, ne l'invente pas comme une decouverte plus tard. "
    "Sa jauge (Second Sort) permet, une fois pleine, de relancer "
    "immediatement le dernier lancer de reussite. IMPORTANT : quand cette "
    "jauge est pleine et qu'un lancer de reussite ne satisfait pas le "
    "joueur, DEMANDE-LUI explicitement s'il souhaite utiliser sa baguette "
    "pour relancer AVANT de continuer le recit -- ne poursuis jamais "
    "l'histoire sur ce resultat sans lui avoir pose la question.",

    "TOTEMS = AMIS ET CREATURES : en dehors de la baguette, il n'y a AUCUN "
    "totem ni sort au debut de cette aventure -- tout le reste se "
    "construit en jouant. Quand le personnage se lie d'amitie avec "
    "quelqu'un ou rencontre une creature fantastique marquante, c'est "
    "l'occasion d'inventer ce nouveau compagnon (nom, apparence, ce qu'il "
    "apporte) et de raconter cette rencontre. Le joueur l'ajoutera ensuite "
    "lui-meme dans l'application (nouvelle jauge, image...) : tu n'as rien "
    "a gerer mecaniquement, juste a le raconter. S'il apparait plus tard "
    "dans la liste des TOTEMS/ALLIES ci-dessus, integre-le naturellement a "
    "partir de ce moment-la.",

    "NOUVEAUX SORTS (mecanique de cours) : regulierement, fais vivre au "
    "personnage un cours de magie qui enseigne d'abord un vrai fait "
    "scientifique ou logique, en une ou deux phrases simples et exactes "
    "(physique, biologie, nature...), puis pose une question a ce sujet. "
    "Si le joueur repond correctement, le personnage apprend un nouveau "
    "sort dont l'effet decoule logiquement de ce fait -- exemple : l'air "
    "chaud monte et l'air froid descend, donc le sort Wingardium Leviosa "
    "fait leviter les objets. Si la reponse est fausse, ne fais jamais "
    "echouer definitivement : donne un indice, un nouvel essai, ou l'aide "
    "d'un professeur. Comme pour les totems, tu n'as rien a gerer "
    "mecaniquement pour un sort appris : raconte la decouverte, le joueur "
    "l'ajoutera ensuite lui-meme dans l'application.",
]


# ---------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------

STORIES = {
    "animorph": {
        "slug": "animorph",
        "title": "Animorph",
        "header_title": "Les D\u00e9s de l'Aventure d'Animorph",
        "subtitle": "Gabin explore la jungle, guide par ses totems.",
        "save_file": "dice_state_animorph.json",
        "bg_image_b64": _ANIMORPH_BG,
        "pip_symbols": ANIMORPH_PIP_SYMBOLS,
        "totems": ANIMORPH_TOTEMS,
        "default_pip_symbol": "araignee",
        "protagonist_ref": "Gabin/Animorph",
        "fixed_allies_line": ANIMORPH_FIXED_ALLIES_LINE,
        "ally_help_text": ANIMORPH_ALLY_HELP_TEXT,
        "lore_paragraphs": ANIMORPH_LORE_PARAGRAPHS,
        "seed_state_file": "dice_state_seed.json",  # partie de depart fournie (Android)
    },
    "poudlard": {
        "slug": "poudlard",
        "title": "Poudlard",
        "header_title": "Les D\u00e9s de l'Aventure \u00e0 Poudlard",
        "subtitle": "Un nouvel eleve arrive a Poudlard, sans savoir encore ce qui l'attend.",
        "save_file": "dice_state_poudlard.json",
        "bg_image_b64": _POUDLARD_BG,
        "pip_symbols": POUDLARD_PIP_SYMBOLS,
        "totems": POUDLARD_TOTEMS,
        "default_pip_symbol": "baguette",
        "protagonist_ref": "un nouvel eleve de Poudlard (prenom a demander en debut d'aventure)",
        "fixed_allies_line": POUDLARD_FIXED_ALLIES_LINE,
        "ally_help_text": {},
        "lore_paragraphs": POUDLARD_LORE_PARAGRAPHS,
        "seed_state_file": None,  # part de zero, aucune partie pre-remplie
    },
}

STORY_ORDER = ["animorph", "poudlard"]
