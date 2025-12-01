import streamlit as st
from transformers import pipeline
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime
import os
import tempfile
import torch

# ==========================================
# 1. CONFIGURAÇÃO VISUAL (ACESSIBILIDADE)
# ==========================================
st.set_page_config(page_title="Assistente Visual", page_icon="👁️", layout="wide")

# CSS para Alto Contraste (Amarelo e Preto para o seu pai)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    p, label, .stMarkdown, h1, h2, h3 { color: #FFFFFF !important; font-size: 24px !important; }
    .stButton>button {
        width: 100%; height: 80px; font-size: 30px !important; font-weight: bold;
        background-color: #FFFF00 !important; color: #000000 !important;
        border: 2px solid #FFFFFF; border-radius: 15px; margin-top: 10px;
    }
    .resposta-box {
        background-color: #222222; padding: 20px; border-radius: 10px;
        border: 2px solid #FFFF00; text-align: center; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("👁️ Assistente Visual")

# ==========================================
# 2. CARREGAMENTO DOS MODELOS (CACHE)
# ==========================================
@st.cache_resource
def load_models():
    print("⏳ Carregando modelos...")
    # Verifica GPU
    device = 0 if torch.cuda.is_available() else -1
    
    # Visão
    vision_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device=device)
    
    # Tradução
    translator = GoogleTranslator(source='auto', target='pt')
    
    # Memória
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("✅ Modelos prontos!")
    return vision_pipe, translator, embeddings

vision_pipe, translator, embeddings = load_models()
persist_directory = "./memoria_db"

# ==========================================
# 3. FUNÇÕES LÓGICAS
# ==========================================

def gerar_audio_gtts(texto):
    """Gera áudio usando Google (Grátis e Ilimitado)"""
    if not texto: return None
    try:
        tts = gTTS(text=texto, lang='pt', slow=False)
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Erro no áudio: {e}")
        return None

def salvar_memoria(texto):
    try:
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        agora = datetime.now().strftime("%H:%M")
        db.add_texts(texts=[f"Eu vi: {texto}"], metadatas=[{"hora": agora}])
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def buscar_memoria(pergunta):
    try:
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        docs = db.similarity_search(pergunta, k=1)
        if docs:
            return f"Às {docs[0].metadata['hora']}, {docs[0].page_content}"
        return "Não encontrei nada na memória recente."
    except:
        return "Ainda não tenho memórias guardadas."

# ==========================================
# 4. INTERFACE STREAMLIT
# ==========================================

aba_ver, aba_memoria = st.tabs(["📸 VER AGORA", "🧠 MEMÓRIA"])

with aba_ver:
    st.write("Aponte a câmera para o objeto:")
    camera = st.camera_input("Tirar Foto", label_visibility="collapsed")
    
    if camera:
        img = Image.open(camera).convert('RGB')
        
        with st.spinner('👀 Analisando...'):
            # 1. Visão
            res = vision_pipe(img)
            texto_en = res[0]['generated_text']
            
            # 2. Tradução
            texto_pt = translator.translate(texto_en)
            
            # 3. Salvar
            salvar_memoria(texto_pt)
            
            msg_final = f"Eu vejo: {texto_pt}"
            
            # 4. Mostrar e Falar
            st.markdown(f'<div class="resposta-box"><h1>{msg_final}</h1></div>', unsafe_allow_html=True)
            
            audio_path = gerar_audio_gtts(msg_final)
            if audio_path:
                st.audio(audio_path, format="audio/mp3", autoplay=True)

with aba_memoria:
    st.write("Pergunte algo (Ex: Onde está a chave?):")
    
    with st.form("form_mem"):
        pergunta = st.text_input("Sua pergunta:", placeholder="Digite aqui...")
        btn_buscar = st.form_submit_button("🔎 LEMBRAR")
        
        if btn_buscar and pergunta:
            with st.spinner('🧠 Pensando...'):
                resposta = buscar_memoria(pergunta)
                
                st.markdown(f'<div class="resposta-box"><h1>{resposta}</h1></div>', unsafe_allow_html=True)
                
                audio_path = gerar_audio_gtts(resposta)
                if audio_path:
                    st.audio(audio_path, format="audio/mp3", autoplay=True)
