import streamlit as st
import pd as pd
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
    /* RESET BÁSICO E CORES DO TEMA GLOBAL */
    .stApp {
        background-color: #F4F9FD; 
    }
    
    /* CABEÇALHO E LOGO */
    .logo-container {
        text-align: center;
        padding-top: 10px;
        margin-bottom: 20px;
    }
    .logo-text {
        font-size: 32px;
        font-weight: 800;
        color: #3A7CA5; 
        font-family: 'Arial', sans-serif;
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

    /* TELA INICIAL (HERO SECTION) */
    .hero-title {
        text-align: center;
        color: #3A7CA5;
        font-size: 22px;
        margin-top: 10px;
        margin-bottom: 20px;
        font-weight: normal;
    }
    .hero-title b {
        font-weight: 800;
    }
    .hero-image-container {
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-image-container img {
        width: 100%;
        max-width: 400px;
        border-radius: 20px;
    }

    /* ESTILO DOS BOTÕES (CENTRALIZADOS E COM DESIGN DA FOTO) */
    /* Selecionamos tanto o primário quanto o secundário para unificar o estilo */
    div.stButton > button {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 40px !important; /* Mais padding lateral para manter o formato */
        font-size: 20px !important; 
        font-weight: bold !important;
        display: block !important;
        margin: 0 auto !important; /* Força a centralização horizontal */
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4) !important;
        transition: transform 0.2s !important;
        width: auto !important; /* Deixa o botão respirar conforme o texto */
        min-width: 250px !important; /* Garante que ele não fique pequeno demais */
    }
    
    div.stButton > button:hover {
        transform: scale(1.05) !important;
        border: none !important;
    }

    /* REFINAMENTOS FEATURE ICONS */
    .flex-features-container {
        display: flex;
        justify-content: space-around; 
        align-items: flex-start;
        margin-top: 25px;
        margin-bottom: 20px;
        padding: 0 10px;
    }
    .flex-feature-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 30%;
    }
    .feature-icon-circle-small {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 55px; 
        height: 55px; 
        border-radius: 50%;
        font-size: 24px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 8px;
    }
    .bg-blue-small { background-color: #5DADE2; color: white; }
    .bg-yellow-small { background-color: #F4D03F; color: white; }
    .bg-red-small { background-color: #E74C3C; color: white; }
    
    .feature-text-small {
        font-size: 13px; 
        color: #555;
        font-weight: 600;
        text-align: center;
    }

    /* ESTILOS DA TELA DE TESTE */
    .test-header-title { 
        color: #1A5276; 
        font-size: 26px; 
        font-style: italic; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 10px; 
    }
    .test-banner { 
        background: linear-gradient(180deg, #D6EAF8, #EBF5FB); 
        color: #1A5276; 
        text-align: center; 
        padding: 15px; 
        font-size: 16px; 
        font-weight: 500; 
        margin-top: 5px;
        margin-bottom: 20px; 
    }
    .question-title { 
        color: #1A5276; 
        font-size: 15px; 
        font-weight: bold; 
        border-bottom: 1px solid #D4E6F1; 
        padding-bottom: 5px; 
        margin-bottom: 15px; 
        margin-top: 20px; 
    }

    /* TELAS DE RESULTADOS */
    .rec-card { background: white; border-radius: 15px; padding: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; }
    .rec-card-title { color: #1A5276; font-size: 17px; font-weight: 800; margin-bottom: 3px; }
    .rec-card-btn { background: linear-gradient(180deg, #2980B9, #1A5276); color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DE CARREIRAS ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Desenvolvedor de Software', 'description': 'Trilha de Programação Completa', 'reason': 'Ideal para seu perfil analítico.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400'}},
    {'interests': ['Negócios'], 'education': ['Ensino Médio', 'Ensino Superior'], 'career': {'title': 'Marketing Digital', 'description': 'Estratégia & Mídias Sociais', 'reason': 'Combina com sua visão de negócios.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400'}}
]

def get_career_recommendation(selected_interests, selected_education):
    possible_careers = []
    for option in career_database:
        if any(interest in option['interests'] for interest in selected_interests) and selected_education in option['education']:
            possible_careers.append(option['career'])
    return possible_careers if possible_careers else [{'title': 'Empreendedor Inovador', 'description': 'Gestão de Startups', 'reason': 'Perfil adaptável.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400'}]

# --- TELA 1: LANDING PAGE ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso Profissional</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-image-container"><img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800"></div>', unsafe_allow_html=True)
    
    # Botão Centralizado
    if st.button("Comece Agora"):
        st.session_state.page = 'test'
        st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-blue-small">👤</div>
                <div class="feature-text-small">Teste</div>
            </div>
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-yellow-small">📋</div>
                <div class="feature-text-small">Trilhas</div>
            </div>
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-red-small">🎓</div>
                <div class="feature-text-small">Dicas</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO DE TESTE ---
def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    st.markdown("<div class='test-banner'>Nos ajude a conhecer você melhor.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='question-title'>Qual o seu nome?</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Digite seu nome...", label_visibility="collapsed")
    
    st.markdown("<div class='question-title'>Quais são seus principais interesses?</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        tech_check = st.checkbox("Tecnologia")
        health_check = st.checkbox("Saúde")
    with col2:
        biz_check = st.checkbox("Negócios")
        design_check = st.checkbox("Artes & Design")
    
    selected_interests = [i for i, v in zip(["Tecnologia", "Negócios", "Saúde", "Artes & Design"], [tech_check, biz_check, health_check, design_check]) if v]
        
    st.markdown("<div class='question-title'>Qual seu nível de escolaridade?</div>", unsafe_allow_html=True)
    selected_education = st.radio("", ["Ensino Médio", "Ensino Superior", "Pós-Graduação"], label_visibility="collapsed")
    
    st.write("") 
    
    # Botão "Continuar" Centralizado
    if st.button("Continuar"):
        if not name.strip():
            st.warning("⚠️ Por favor, digite seu nome.")
        elif not selected_interests:
            st.warning("⚠️ Selecione pelo menos um interesse.")
        else:
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
            salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
            st.session_state.page = 'results'
            st.rerun()

# --- TELA 3: RESULTADOS ---
def show_results_page():
    st.markdown('<div class="results-header"><div class="results-title">Suas Recomendações</div></div>', unsafe_allow_html=True)
    for career in st.session_state.recommended_careers:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-card-title">{career['title']}</div>
            <div>{career['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Voltar"): 
        st.session_state.page = 'test'
        st.rerun()

# --- GERENCIADOR DE ROTAS ---
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()