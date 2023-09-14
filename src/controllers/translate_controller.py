from flask import Blueprint, render_template, request
from deep_translator import GoogleTranslator
from models.language_model import LanguageModel
from models.history_model import HistoryModel


translate_controller = Blueprint("translate_controller", __name__)

DEFAULT_TEXT_TO_TRANSLATE = "O que deseja traduzir"
DEFAULT_TRANSLATE_FROM = "pt"
DEFAULT_TRANSLATE_TO = "en"
DEFAULT_TRANSLATED = "Tradução"


def post_translate(languages, text_to_translate, translate_from, translate_to, reversed):
    try:
        translator = GoogleTranslator(source=translate_from, target=translate_to)
        translated = translator.translate(text_to_translate)
        if reversed:
            translate_from, translate_to = translate_to, translate_from

    except Exception as e:
        return render_template(
            "index.html",
            languages=languages,
            text_to_translate=text_to_translate,
            translate_from=translate_from,
            translate_to=translate_to,
            translated="Erro na tradução: " + str(e)
        )

    HistoryModel(
        {
            "text_to_translate":text_to_translate,
            "translate_from":translate_from,
            "translate_to":translate_to,
            "translated":translated
        }
    ).save()

    return render_template(
        "index.html",
        languages=languages,
        text_to_translate=text_to_translate,
        translate_from=translate_from,
        translate_to=translate_to,
        translated=translated
    )

# Reqs. 4 e 5
@translate_controller.route("/", methods=["GET", "POST"])
def index():
    languages = LanguageModel.list_dicts()
    reversed = False

    if request.method == "POST":
        text_to_translate = request.form.get("text-to-translate")
        translate_from = request.form.get("translate-from")
        translate_to = request.form.get("translate-to")

        return post_translate(languages, text_to_translate, translate_from, translate_to, reversed)

    return render_template(
            "index.html",
            languages=languages,
            text_to_translate=DEFAULT_TEXT_TO_TRANSLATE,
            translate_from=DEFAULT_TRANSLATE_FROM,
            translate_to=DEFAULT_TRANSLATE_TO,
            translated=DEFAULT_TRANSLATED
        )


# Req. 6
@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    languages = LanguageModel.list_dicts()
    reversed = True

    text_to_translate = request.form.get("text-to-translate")
    translate_from = request.form.get("translate-from")
    translate_to = request.form.get("translate-to")

    return post_translate(languages, text_to_translate, translate_from, translate_to, reversed)
