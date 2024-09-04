from flask import Flask, request, render_template
from langdetect import detect, DetectorFactory
from googletrans import Translator, LANGUAGES

app = Flask(__name__)


def detect_and_translate(text, target_lang):
    result_lang_code = detect(text)
    result_lang_name = LANGUAGES.get(result_lang_code, "Unknown Language")

    # Translate
    translator = Translator()
    translated_text = translator.translate(text, src=result_lang_code, dest=target_lang)

    return result_lang_name, translated_text


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/trans", methods=['GET', 'POST'])
def translate():
    translation = ""
    detected_lang = ""
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['target_lang']
        detected_lang, translation = detect_and_translate(text, target_lang)
    return render_template("index.html", detected_lang=detected_lang, translation=translation, languages=LANGUAGES)


if __name__ == "__main__":
    app.run(debug=True)
