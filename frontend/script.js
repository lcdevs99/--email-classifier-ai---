const emailText = document.getElementById("emailText");
const emailFile = document.getElementById("emailFile");
const resultado = document.getElementById("resultado");
const clearBtn = document.getElementById("clearBtn");

// Limpa resultado quando o campo de texto fica vazio
emailText.addEventListener("input", () => {
  if (emailText.value.trim() === "") {
    resultado.innerText = "";
  } else {
    // Se o usuário começar a digitar, limpamos o arquivo
    emailFile.value = "";
    clearBtn.style.display = "none";
  }
});

// Mostra ou esconde o X conforme arquivo selecionado
emailFile.addEventListener("change", () => {
  if (emailFile.files.length > 0) {
    clearBtn.style.display = "inline-block";
    // Se o usuário selecionar arquivo, limpamos o texto
    emailText.value = "";
  } else {
    clearBtn.style.display = "none";
    resultado.innerText = "";
  }
});

function clearFile() {
  emailFile.value = "";
  clearBtn.style.display = "none";
  resultado.innerText = "";
}

async function processEmail() {
  const text = emailText.value;
  if (!text.trim()) {
    resultado.innerText = "";
    return;
  }
  resultado.innerText = "Processando texto...";
  try {
    const response = await fetch("http://127.0.0.1:5000/process", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text})
    });
    const result = await response.json();

    if (result.error) {
      resultado.innerText = `Erro: ${result.error}`;
    } else {
      resultado.innerText =
        `Categoria: ${result.categoria}\nResposta: ${result.resposta}\nConfiança: ${result.confiança}`;
    }
  } catch (err) {
    resultado.innerText = "Erro de conexão com o servidor.";
  }
}

async function processFile() {
  if (emailFile.files.length === 0) {
    resultado.innerText = "";
    alert("Selecione um arquivo primeiro!");
    return;
  }
  const formData = new FormData();
  formData.append("file", emailFile.files[0]);

  resultado.innerText = "Processando arquivo...";
  try {
    const response = await fetch("/process", {
      method: "POST",
      body: formData
    });
    const result = await response.json();

    if (result.error) {
      resultado.innerText = `Erro: ${result.error}`;
    } else {
      resultado.innerText =
        `Categoria: ${result.categoria}\nResposta: ${result.resposta}\nConfiança: ${result.confiança}`;
    }
  } catch (err) {
    resultado.innerText = "Erro de conexão com o servidor.";
  }
}