import streamlit as st
import pandas as pd
import os

# --- ARQUIVO DE BANCO DE DADOS (CSV) ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    try:
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])
    except Exception as e:
        st.error(f"Erro ao acessar o banco de dados: {e}")
        return pd.DataFrame()

def salvar_recomendacao(nome, interesses, escolaridade, recomendacao):
    df = carregar_dados()
    new_entry = pd.DataFrame([{
        "Nome": nome, 
        "Interesses": ", ".join(interesses),
        "Escolaridade": escolaridade, 
        "Carreira Recomendada": recomendacao
    }])
    df_final = pd.concat([df, new_entry], ignore_index=True)
    df_final.to_csv(CSV_FILE, index=False, encoding='utf-8')

# --- CONFIGURAÇÃO DA PÁGINA ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing' 
if 'recommended_careers' not in st.session_state:
    st.session_state.recommended_careers = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.set_page_config(page_title="AprendaJá PRO", page_icon="🚀", layout="centered")

# --- INJEÇÃO DE CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* RESET E FUNDO */
    .stApp {
        background-color: #F4F9FD; 
    }
    
    /* LOGO */
    .logo-container {
        text-align: center;
        padding-top: 10px;
        margin-bottom: 20px;
    }
    .logo-text {
        font-size: 32px;
        font-weight: 800;
        color: #3A7CA5; 
    }
    .logo-badge {
        background: linear-gradient(90deg, #F39C12, #D35400); 
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        vertical-align: super;
        margin-left: 5px;
    }

    /* TÍTULOS */
    .hero-title {
        text-align: center;
        color: #3A7CA5;
        font-size: 22px;
        margin-bottom: 20px;
    }
    .test-header-title { 
        color: #1A5276; 
        font-size: 28px; /* Aumentado */
        font-style: italic; 
        font-weight: bold; 
        text-align: center; 
        margin-top: -10px; /* Movido para cima */
        margin-bottom: 15px; 
    }

    /* BOTÃO - DESIGN IGUAL À FOTO E CENTRALIZADO */
    div.stButton > button {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important;
        border: none !important;
        border-radius: 35px !important; /* Formato Pílula */
        padding: 12px 50px !important; 
        font-size: 20px !important; 
        font-weight: bold !important;
        display: block !important;
        margin: 20px auto !important; /* CENTRALIZAÇÃO AUTOMÁTICA */
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4) !important;
        transition: transform 0.2s !important;
        min-width: 280px !important;
    }
    div.stButton > button:hover {
        transform: scale(1.03) !important;
    }

    /* BANNER E QUESTÕES */
    .test-banner { 
        background: linear-gradient(180deg, #D6EAF8, #EBF5FB); 
        color: #1A5276; 
        text-align: center; 
        padding: 15px; 
        border-radius: 10px;
        margin-bottom: 20px; 
    }
    .question-title { 
        color: #1A5276; 
        font-size: 16px; 
        font-weight: bold; 
        border-bottom: 1px solid #D4E6F1; 
        padding-bottom: 5px; 
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* GRID DE ÍCONES (LANDING) */
    .flex-features-container {
        display: flex;
        justify-content: space-around; 
        margin-top: 30px;
    }
    .flex-feature-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .feature-icon-circle-small {
        width: 55px; height: 55px; 
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 8px;
    }
    .bg-blue-small { background-color: #5DADE2; color: white; }
    .bg-yellow-small { background-color: #F4D03F; color: white; }
    .bg-red-small { background-color: #E74C3C; color: white; }

    /* CARDS DE RESULTADO */
    .rec-card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; }
    .rec-card-title { color: #1A5276; font-size: 18px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Desenvolvedor de Software', 'description': 'Trilha de Programação Completa', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400'}},
    {'interests': ['Negócios'], 'education': ['Ensino Médio', 'Ensino Superior'], 'career': {'title': 'Marketing Digital', 'description': 'Estratégia & Mídias Sociais', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400'}}
]

def get_career_recommendation(selected_interests, selected_education):
    possible_careers = [c['career'] for c in career_database if any(i in c['interests'] for i in selected_interests) and selected_education in c['education']]
    return possible_careers if possible_careers else [{'title': 'Empreendedor Inovador', 'description': 'Gestão de Startups', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400'}]

# --- TELAS ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso</h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-bottom:20px;"><img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800" width="350" style="border-radius:20px;"></div>', unsafe_allow_html=True)
    
    if st.button("Comece Agora"):
        st.session_state.page = 'test'
        st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-blue-small">👤</div><div style="font-size:12px; font-weight:bold;">Teste</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-yellow-small">📋</div><div style="font-size:12px; font-weight:bold;">Trilhas</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-red-small">🎓</div><div style="font-size:12px; font-weight:bold;">Dicas</div></div>
        </div>
    """, unsafe_allow_html=True)

def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    st.markdown("<div class='test-banner'>Nos ajude a conhecer você melhor.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='question-title'>Qual o seu nome?</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Digite seu nome...", label_visibility="collapsed")
    
    st.markdown("<div class='question-title'>Quais são seus principais interesses?</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        tech = st.checkbox("Tecnologia")
        health = st.checkbox("Saúde")
    with col2:
        biz = st.checkbox("Negócios")
        design = st.checkbox("Artes & Design")
    
    st.markdown("<div class='question-title'>Qual seu nível de escolaridade?</div>", unsafe_allow_html=True)
    edu = st.radio("", ["Ensino Médio", "Ensino Superior", "Pós-Graduação"], label_visibility="collapsed")
    
    selected_ints = [i for i, v in zip(["Tecnologia", "Negócios", "Saúde", "Artes & Design"], [tech, biz, health, design]) if v]

    if st.button("Continuar"):
        if not name.strip() or not selected_ints:
            st.warning("⚠️ Preencha seu nome e escolha um interesse.")
        else:
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_ints, edu)
            salvar_recomendacao(name, selected_ints, edu, st.session_state.recommended_careers[0]['title'])
            st.session_state.page = 'results'
            st.rerun()

def show_results_page():
    st.markdown("<div class='test-header-title'>Suas Recomendações</div>", unsafe_allow_html=True)
    for career in st.session_state.recommended_careers:
        st.markdown(f"""<div class="rec-card"><div class="rec-card-title">{career['title']}</div><p>{career['description']}</p></div>""", unsafe_allow_html=True)
    if st.button("Refazer Teste"):
        st.session_state.page = 'test'
        st.rerun()

# --- NAVEGAÇÃO ---
if st.session_state.page == 'landing': show_landing_page()
elif st.session_state.page == 'test': show_profile_test_page()
elif st.session_state.page == 'results': show_results_page()

st.divider()
if st.checkbox("⚙️ Modo Administrador"):
    st.dataframe(carregar_dados())