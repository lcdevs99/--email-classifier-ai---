from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pdfplumber   # substitui o PyPDF2

app = Flask(__name__)
CORS(app)

# Carregar modelo treinado
model_path = "./email-classifier-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Criar pipeline de classificação
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def classificar_email(texto):
    resultado = classifier(texto)[0]
    label = resultado['label']
    score = resultado['score']

    # Ajuste do mapeamento
    label_map = {"LABEL_0": "Improdutivo", "LABEL_1": "Produtivo"}
    categoria = label_map.get(label, "Desconhecido")

    if categoria == "Produtivo":
        resposta = "Obrigado pelo contato. Sua solicitação será analisada pela equipe."
    else:
        resposta = "Mensagem recebida. Não é necessária ação adicional."

    return categoria, resposta, score

@app.route("/process", methods=["POST"])
def process_email():
    email_text = ""

    # Caso seja texto direto (JSON)
    if request.is_json:
        data = request.json
        email_text = data.get("text", "")

    # Caso seja upload de arquivo
    elif "file" in request.files:
        file = request.files["file"]
        if file.filename.endswith(".txt"):
            email_text = file.read().decode("utf-8")
        elif file.filename.endswith(".pdf"):
            email_text = ""
            with pdfplumber.open(file) as pdf:
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
    app.run(debug=True)