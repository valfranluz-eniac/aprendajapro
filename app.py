import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AprendaJá PRO", page_icon="🚀", layout="centered")

# --- ARQUIVO DE BANCO DE DADOS ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    try:
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])
    except:
        return pd.DataFrame()

def salvar_recomendacao(nome, interesses, escolaridade, recomendacao):
    df = carregar_dados()
    new_entry = pd.DataFrame([{"Nome": nome, "Interesses": ", ".join(interesses), "Escolaridade": escolaridade, "Carreira Recomendada": recomendacao}])
    pd.concat([df, new_entry], ignore_index=True).to_csv(CSV_FILE, index=False, encoding='utf-8')

if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INJEÇÃO DE CSS DE PRECISÃO (RESOLVE O DESALINHAMENTO) ---
st.markdown("""
<style>
    .stApp { background-color: #F4F9FD; }
    
    /* CENTRALIZAÇÃO TOTAL DO BOTÃO */
    /* Alvo: O container de elemento do Streamlit */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important;
        border: none !important;
        border-radius: 35px !important;
        padding: 12px 60px !important; 
        font-size: 18px !important; 
        font-weight: bold !important;
        min-width: 280px !important;
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.3) !important;
    }

    /* ESTILOS DE TEXTO E CARDS */
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-text { font-size: 32px; font-weight: 800; color: #3A7CA5; }
    .hero-title { text-align: center; color: #3A7CA5; font-size: 22px; margin-bottom: 20px; }
    .test-header-title { color: #1A5276; font-size: 26px; font-style: italic; font-weight: bold; text-align: center; margin-bottom: 15px; }
    
    .flex-features-container { display: flex; justify-content: space-around; margin-top: 30px; }
    .flex-feature-item { display: flex; flex-direction: column; align-items: center; }
    .feature-icon-circle-small {
        width: 55px; height: 55px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 8px;
    }
    
    .rec-card { 
        background: white; border-radius: 15px; padding: 15px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; 
        display: flex; align-items: center;
    }
    .rec-card-img { width: 80px; height: 80px; border-radius: 10px; margin-right: 15px; }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE TELAS ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso</h2>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800", use_container_width=True)
    
    if st.button("Comece Agora"):
        st.session_state.page = 'test'
        st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item"><div class="feature-icon-circle-small" style="background:#5DADE2; color:white;">👤</div><span>Teste</span></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small" style="background:#F4D03F; color:white;">📋</div><span>Trilhas</span></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small" style="background:#E74C3C; color:white;">🎓</div><span>Dicas</span></div>
        </div>
    """, unsafe_allow_html=True)

def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    name = st.text_input("Qual seu nome?", placeholder="Digite aqui...")
    interests = st.multiselect("Interesses:", ["Tecnologia", "Artes & Design", "Saúde", "Negócios"])
    edu = st.radio("Escolaridade:", ["Ensino Médio", "Ensino Superior"])
    
    if st.button("Continuar"):
        if name and interests:
            st.session_state.user_name = name
            st.session_state.page = 'results'
            st.rerun()

def show_results_page():
    st.markdown(f"<div class='test-header-title'>Resultados para {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="rec-card">
            <img src="https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400" class="rec-card-img">
            <div>
                <div style="color:#1A5276; font-weight:bold;">Designer UX/UI</div>
                <div style="font-size:13px; color:#666;">Criação de Interfaces Digitais</div>
                <div style="font-size:12px; color:#2980B9; font-style:italic;">Sua criatividade focada no usuário.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Refazer Teste"):
        st.session_state.page = 'test'
        st.rerun()

# --- NAVEGAÇÃO ---
if st.session_state.page == 'landing': show_landing_page()
elif st.session_state.page == 'test': show_profile_test_page()
elif st.session_state.page == 'results': show_results_page()