from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/process", methods=["POST"])
def process_email():
    data = request.json
    email_text = data.get("text", "")

    return jsonify({
        "categoria": "Em construção",
        "resposta": f"Recebi: {email_text}"
    })

if __name__ == "__main__":
    app.run(debug=True)