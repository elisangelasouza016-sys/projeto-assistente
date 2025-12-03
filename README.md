# 👁️ Assistente Visual com Memória (RAG)

> Tecnologia Assistiva potencializada por IA Generativa para auxiliar pessoas com baixa visão.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Prototype-warning)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Sobre o Projeto

Este projeto nasceu de uma necessidade pessoal. Meu pai convive com a **Retinose Pigmentar** há mais de 15 anos, uma condição degenerativa que causa perda de visão periférica (visão em túnel) e cegueira noturna.

O objetivo foi criar uma aplicação de **Tecnologia Assistiva** que atue como um "segundo par de olhos", devolvendo autonomia em tarefas diárias, como identificar remédios, encontrar objetos perdidos ou descrever o ambiente.

## ✨ Funcionalidades Principais

* **📸 Visão Computacional (Image-to-Text):** Identifica objetos e descreve cenas em tempo real usando modelos de IA (BLIP).
* **🧠 Memória de Longo Prazo (RAG):** Utiliza *Retrieval-Augmented Generation* para armazenar descrições. O usuário pode perguntar: *"Onde deixei minhas chaves?"* e o sistema busca no histórico.
* **🗣️ Interface Auditiva:** Toda a interação é respondida por voz (Text-to-Speech), eliminando a necessidade de leitura.
* **🎨 Acessibilidade Visual:** Interface desenvolvida com alto contraste (Amarelo/Preto) e fontes grandes.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface:** Streamlit (foco em acessibilidade)
* **Visão:** Hugging Face Transformers (`Salesforce/blip-image-captioning-large`)
* **RAG & Vetores:** LangChain, ChromaDB
* **Tradução:** Deep Translator
* **Áudio:** gTTS (Google Text-to-Speech) / ElevenLabs API

## 🚀 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU-USUARIO/NOME-DO-REPO.git](https://github.com/SEU-USUARIO/NOME-DO-REPO.git)
