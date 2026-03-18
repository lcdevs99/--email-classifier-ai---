# Email Classifier AI

Projeto para classificar emails em **Produtivo** ou **Improdutivo** e sugerir respostas automáticas.

## Estrutura

- `backend/app.py` → Flask backend
- `frontend/index.html` → Interface web
- `data/sample_email.txt` → Exemplo de email
- `requirements.txt` → Dependências

## Como rodar localmente

1. Clone o repositório.
   git clone https://github.com/lcdevs99/--email-classifier-ai---.git
   cd --email-classifier-ai---

2. Crie um ambiente virtual e instale dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
    pip install -r requirements.txt


3. 	Inicie o backend Flask:
    python backend/app.py

4. 	Abra o - Abra o frontend/index.html no navegador para usar a interface.

Funcionalidades
- Classificação automática de emails em Produtivo ou Improdutivo.
- Sugestão de respostas automáticas.
- Interface web simples para interação.
- API backend que pode ser integrada a outros sistemas.

Formatos aceitos
- 	Arquivos .txt com frases simples.
-	Arquivos .pdf contendo mensagens de texto.
- 	Texto colado diretamente na interface web.

Observações
- Arquivos de modelo e checkpoints não são versionados (estão no .gitignore).
- Para treinar novamente, salve os modelos na pasta backend/email-classifier-model/.

Contribuição
- Faça um fork do projeto.
- Crie uma branch para sua feature:
    git checkout -b minha-feature

- Commit suas alterações e faça push.
- Abra um Pull Request.

