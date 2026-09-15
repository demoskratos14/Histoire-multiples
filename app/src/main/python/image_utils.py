# -*- coding: utf-8 -*-
"""
IMAGE_UTILS - redimensionnement/compression des images de fond et de
totems (module autonome, comme mistral_client.py).
=====================================================================
CORRIGE LE BUG "image trop grosse pour etre visible" (Poudlard, nouvelles
histoires) : une photo prise directement au telephone (plusieurs milliers
de pixels de large, plusieurs Mo) embarquee telle quelle dans la page peut
tout simplement ne pas s'afficher sur Android -- la WebView (comme la
plupart des moteurs mobiles) a une limite de taille de texture pour tout
ce qui est achemine au GPU (fond d'ecran CSS compris), generalement autour
de 2048 ou 4096 pixels sur le plus grand cote. Au-dela, l'image reste
invisible (ou s'affiche de facon cassee/enorme), meme si le CSS demande un
cadrage "cover" qui devrait pourtant toujours "rentrer" a l'ecran.

L'image de fond d'Animorph (bg_animorph_data.py) a ete redimensionnee
"a la main" a l'origine, ce qui explique qu'elle fonctionne bien. Ce
module applique desormais AUTOMATIQUEMENT le meme traitement a toute image
de fond (Poudlard comprise, deja integree, sans avoir besoin de toucher au
fichier bg_poudlard_data.py existant : voir resize_bg_b64() utilise
directement dans stories.py) et a toute nouvelle histoire creee depuis
l'application.

Necessite Pillow (pip install pillow) -- voir la note en bas de ce
fichier pour app/build.gradle. Si Pillow n'est pas installe, toutes les
fonctions ci-dessous renvoient l'image d'origine sans y toucher (aucun
crash de l'appli), mais le probleme de taille peut alors persister.

  >>> IMPORTANT : ajoutez "pillow" a cote de "flask" dans les
  >>> dependances pip d'app/build.gradle (bloc `pip { install "flask" }`
  >>> devient `pip { install "flask"; install "pillow" }`), sinon ce
  >>> module ne pourra rien redimensionner du tout sur le telephone.
"""

import base64
import io

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


# Cote le plus long, en pixels, au-dela duquel une image de FOND est
# redimensionnee. 1600px est largement suffisant pour remplir n'importe
# quel ecran de telephone en "cover", tout en restant tres en dessous des
# limites de texture GPU qui rendent une image invisible sur certains
# telephones/WebView quand elle est trop grande.
MAX_BG_DIMENSION = 1600
BG_JPEG_QUALITY = 82

# Les icones de totem sont affichees minuscules (1em / 1.15rem) : nul
# besoin d'une grande resolution. Les garder petites accelere aussi le
# chargement de chaque page de jeu (elles sont reaffichees a chaque lancer).
MAX_TOTEM_DIMENSION = 400
TOTEM_JPEG_QUALITY = 85


def _has_alpha(img):
    return img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)


def _resize_if_needed(img, max_dimension):
    w, h = img.size
    if max(w, h) > max_dimension:
        ratio = max_dimension / float(max(w, h))
        new_size = (max(1, round(w * ratio)), max(1, round(h * ratio)))
        img = img.resize(new_size, Image.LANCZOS)
    return img


def resize_bg_bytes(raw_bytes, max_dimension=MAX_BG_DIMENSION, quality=BG_JPEG_QUALITY):
    """Pour une image de FOND (toujours affichee en JPEG opaque -- voir
    'data:image/jpeg;base64,' cote dice_web.py) : redimensionne et
    reencode systematiquement en JPEG, sans transparence. En cas d'echec
    (format illisible, Pillow absent...), renvoie les bytes d'origine tels
    quels plutot que de planter."""
    if not _PIL_AVAILABLE or not raw_bytes:
        return raw_bytes
    try:
        img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        img = _resize_if_needed(img, max_dimension)
        out = io.BytesIO()
        img.save(out, format="JPEG", quality=quality, optimize=True)
        return out.getvalue()
    except Exception:
        return raw_bytes


def resize_bg_b64(b64_str, max_dimension=MAX_BG_DIMENSION, quality=BG_JPEG_QUALITY):
    """Meme chose que resize_bg_bytes, mais prend et renvoie une chaine
    base64 -- pratique pour les images de fond deja integrees dans le
    code (bg_animorph_data.py / bg_poudlard_data.py)."""
    if not b64_str:
        return b64_str
    try:
        raw = base64.b64decode(b64_str)
    except Exception:
        return b64_str
    return base64.b64encode(resize_bg_bytes(raw, max_dimension, quality)).decode("ascii")


def resize_totem_bytes(raw_bytes, max_dimension=MAX_TOTEM_DIMENSION, quality=TOTEM_JPEG_QUALITY):
    """Pour une image de TOTEM : redimensionne, et conserve la
    transparence si la source en a une (reencodee en PNG dans ce cas),
    sinon reencode en JPEG. Renvoie un tuple (bytes, extension). En cas
    d'echec, renvoie (raw_bytes, None) -- l'appelant garde alors
    l'extension d'origine du fichier uploade."""
    if not _PIL_AVAILABLE or not raw_bytes:
        return raw_bytes, None
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        has_alpha = _has_alpha(img)
        img = _resize_if_needed(img, max_dimension)
        out = io.BytesIO()
        if has_alpha:
            img.convert("RGBA").save(out, format="PNG", optimize=True)
            return out.getvalue(), "png"
        img.convert("RGB").save(out, format="JPEG", quality=quality, optimize=True)
        return out.getvalue(), "jpg"
    except Exception:
        return raw_bytes, None
