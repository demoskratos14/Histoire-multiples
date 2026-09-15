#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLIENT MISTRAL - narration automatique
=======================================
Client minimal pour l'API Mistral (endpoint "chat completions"), ecrit
avec uniquement la bibliotheque standard (urllib) -- aucune dependance
externe a installer, pour rester coherent avec le reste du projet
(compatible Pydroid 3 / Chaquopy sans rien ajouter au pip install).

Utilise par dice_web.py pour la narration automatique : a chaque
lancer, l'appli envoie le contexte du jeu + l'evenement au modele et
recupere la suite de l'histoire, sans que l'utilisateur ait besoin de
copier-coller quoi que ce soit dans un site externe.

Documentation officielle : https://docs.mistral.ai/
"""

import json
import urllib.request
import urllib.error

API_URL = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_MODEL = "mistral-small-latest"   # couvert par le plan gratuit "La Plateforme"
DEFAULT_TIMEOUT = 40                     # secondes
DEFAULT_MAX_TOKENS = 700


def chat(api_key, messages, model=DEFAULT_MODEL,
         max_tokens=DEFAULT_MAX_TOKENS, timeout=DEFAULT_TIMEOUT):
    """Envoie une conversation (liste de {"role": "system"/"user"/"assistant",
    "content": str}) a l'API Mistral.

    Renvoie toujours un tuple (texte, erreur) et ne leve jamais
    d'exception : toute erreur reseau, HTTP ou de format est convertie
    en message clair, pour que l'appli reste utilisable (mode manuel de
    secours) meme si l'IA est temporairement injoignable.
      - succes  -> (texte_de_la_reponse, None)
      - echec   -> (None, "message d'erreur lisible")
    """
    if not api_key:
        return None, "Aucune cle API Mistral configuree."
    if not messages:
        return None, "Rien a envoyer a l'IA."

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": max_tokens,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode("utf-8"))
            detail_msg = detail.get("message") or detail.get("error") or str(detail)
        except Exception:
            detail_msg = getattr(e, "reason", str(e))
        if e.code == 401:
            return None, "Cle API Mistral refusee (401) : verifie qu'elle est correcte."
        if e.code == 429:
            return None, ("Limite du plan gratuit atteinte pour l'instant (429). "
                           "Reessaie dans un instant.")
        return None, f"Erreur Mistral ({e.code}) : {detail_msg}"
    except urllib.error.URLError as e:
        return None, f"Impossible de joindre l'API Mistral (reseau ?) : {e.reason}"
    except Exception as e:  # securite : ne jamais planter l'appli pour ca
        return None, f"Erreur inattendue en contactant Mistral : {e}"

    try:
        data = json.loads(raw)
        text = data["choices"][0]["message"]["content"]
        text = (text or "").strip()
        if not text:
            return None, "Reponse vide renvoyee par l'API Mistral."
        return text, None
    except (KeyError, IndexError, ValueError, TypeError):
        return None, "Reponse de l'API Mistral illisible (format inattendu)."
