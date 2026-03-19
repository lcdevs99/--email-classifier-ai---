from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import io  

app = Flask(__name__, static_folder="../frontend")
CORS(app)

model_path = "lcdevs99/email-classifier-model"

classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        print("Carregando modelo...")

        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

        print("Modelo carregado!")

    return classifier


def classificar_email(texto):
    clf = get_classifier()

    resultado = clf(texto)[0]
    label = resultado['label']
    score = resultado['score']

    label_map = {"LABEL_0": "Improdutivo", "LABEL_1": "Produtivo"}
    categoria = label_map.get(label, "Desconhecido")

    if categoria == "Produtivo":
        resposta = "Obrigado pelo contato. Sua solicitação será analisada pela equipe."
    else:
        resposta = "Mensagem recebida. Não é necessária ação adicional."

    return categoria, resposta, score


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route("/process", methods=["POST"])
def process_email():
    email_text = ""

    if request.is_json:
        data = request.json
        email_text = data.get("text", "")

    elif "file" in request.files:
        file = request.files["file"]

        print("Arquivo recebido:", file.filename)

        if file.filename.endswith(".txt"):
            email_text = file.read().decode("utf-8")

        elif file.filename.endswith(".pdf"):
            import pdfplumber

            email_text = ""

            file_stream = io.BytesIO(file.read())

            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        email_text += text
        else:
            return jsonify({"error": "Formato não suportado"}), 400

    if not email_text.strip():
        return jsonify({"error": "Nenhum texto encontrado"}), 400

    categoria, resposta, score = classificar_email(email_text)

    return jsonify({
        "categoria": categoria,
        "resposta": resposta,
        "confiança": f"{score:.2f}"
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)