# -*- coding: utf-8 -*-
"""
JOURNAL_EXPORT - export du journal d'une histoire en PDF
==========================================================
Module autonome (comme image_utils.py ou mistral_client.py) : transforme
le journal d'une histoire (session.story_log -- un resume de chapitre par
entree, voir dice_engine.py) en un PDF lisible, pour pouvoir le relire ou
le garder de cote meme si l'histoire est ensuite supprimee de l'appli.

Necessite fpdf2 (pip install fpdf2). Si la bibliotheque n'est pas
installee, generate_journal_pdf() renvoie None sans lever d'exception --
dice_web.py propose alors automatiquement un export .txt a la place (voir
/export_journal), pour ne jamais casser la page.

  >>> IMPORTANT : ajoutez "fpdf2" a cote de "flask"/"pillow" dans les
  >>> dependances pip d'app/build.gradle, sinon l'export PDF ne
  >>> fonctionnera pas sur le telephone (export .txt utilise en secours,
  >>> toujours disponible).
"""

try:
    from fpdf import FPDF
    _FPDF_AVAILABLE = True
    _FPDF_IMPORT_ERROR = None
except Exception as e:  # capture large, comme dans image_utils.py : une
    # bibliotheque manquante/incompatible peut remonter sous d'autres
    # formes qu'un simple ImportError selon la plateforme.
    _FPDF_AVAILABLE = False
    _FPDF_IMPORT_ERROR = f"{type(e).__name__}: {e}"


def fpdf_available():
    return _FPDF_AVAILABLE


def fpdf_import_error():
    """Message d'erreur d'import, pour diagnostic (voir /debug_images
    dans dice_web.py pour l'equivalent Pillow) -- None si tout va bien."""
    return _FPDF_IMPORT_ERROR


# La police standard "Helvetica" de fpdf2 ne couvre que le Latin-1 : le
# journal contient regulierement des emojis (le ton du recit en met
# partout, voir build_mechanics_context dans dice_web.py) qui ne peuvent
# donc pas s'afficher tels quels dans le PDF. Plutot que de planter ou
# d'embarquer une police externe (poids supplementaire, pas forcement
# disponible sur Android/Pydroid), on les retire proprement : le texte
# reste lisible, seule la decoration disparait. Le contenu complet (avec
# emojis) reste par ailleurs toujours consultable via la page /story et
# le bouton "Copier" existant.
_PUNCT_REPLACEMENTS = {
    "\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2026": "...",
}


def _clean(text):
    if not text:
        return ""
    for src, dst in _PUNCT_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "ignore").decode("latin-1")


def generate_journal_pdf(title, subtitle, chapters):
    """chapters : liste de chaines (un resume par chapitre, dans l'ordre
    chronologique -- typiquement session.story_log). Renvoie les bytes du
    PDF genere, ou None si fpdf2 n'est pas disponible."""
    if not _FPDF_AVAILABLE:
        return None

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, _clean(title or "Journal de l'histoire"))
    if subtitle:
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(90, 90, 90)
        pdf.multi_cell(0, 8, _clean(subtitle))
        pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    pdf.set_draw_color(180, 170, 150)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(8)

    if not chapters:
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(0, 7, "(aucun chapitre enregistre pour l'instant)")
    else:
        for i, chapter_text in enumerate(chapters, start=1):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(20, 22, 26)
            pdf.multi_cell(0, 9, f"Chapitre {i}")
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 6, _clean(chapter_text))
            pdf.ln(6)

    out = pdf.output()
    return bytes(out)
