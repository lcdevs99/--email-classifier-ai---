from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Carregar pipeline de classificação de texto
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def classificar_email(texto):
    # Hugging Face retorna labels como POSITIVE/NEGATIVE
    resultado = classifier(texto)[0]
    label = resultado['label']
    score = resultado['score']

    if label == "POSITIVE":
        categoria = "Produtivo"
        resposta = "Obrigado pelo contato. Sua solicitação será analisada pela equipe."
    else:
        categoria = "Improdutivo"
        resposta = "Mensagem recebida. Não é necessária ação adicional."

    return categoria, resposta, score

@app.route("/process", methods=["POST"])
def process_email():
    data = request.json
    email_text = data.get("text", "")

    categoria, resposta, score = classificar_email(email_text)

    return jsonify({
        "categoria": categoria,
        "resposta": resposta,
        "confiança": f"{score:.2f}"
    })

if __name__ == "__main__":
    app.run(debug=True)