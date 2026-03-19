# Arquitetura do Projeto

Este documento descreve as principais decisões de arquitetura tomadas durante o desenvolvimento do desafio.

## Estrutura do Repositório

Optamos por manter **frontend** e **backend** no mesmo repositório para simplificar a gestão e facilitar a comunicação entre as partes.  
A estrutura de pastas foi definida logo no início para garantir organização e escalabilidade.

## Backend

- Linguagem: **Python**
- Framework: **Flask**
- Motivação: escolha leve e simples para prototipagem rápida, ideal para o desafio.
- Primeiros passos: criamos um arquivo de teste em texto para validar a comunicação entre backend e frontend antes de evoluir para a integração com IA.

- Mantido dentro do mesmo repositório para facilitar deploy e integração.
- Separado em **HTML**, **JavaScript** e **style.ts** para garantir modularidade e clareza na organização do código.
- Comunicação inicial validada com o backend via requisições simples.


## Inteligência Artificial

- Modelo de classificação de e-mails treinado e versionado no Hugging Face Hub.
- Estrutura de arquivos do modelo: `config.json`, `tokenizer.json`, `model.safetensors`, etc.
- Decisão: manter apenas arquivos simples em **.txt** e **.pdf** como exemplos de entrada, pois isso já demonstra o funcionamento essencial do sistema.

## Decisões de Projeto

1. **Repositório único**: facilita integração e deploy.
2. **Flask**: framework minimalista, rápido para levantar APIs.
3. **Testes iniciais com arquivos simples**: garantiu que a comunicação estava funcionando antes de investir tempo no treinamento da IA.
4. **IA integrada ao backend**: o modelo é carregado diretamente pelo Flask, permitindo classificação de e-mails em tempo real.

---

## Próximos Passos

- Expandir suporte para outros formatos de arquivo, se necessário.
- Adicionar testes à medida que o projeto for escalando.
- Incrementar a documentação conforme o crescimento do projeto.
 