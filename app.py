import streamlit as st
import pandas as pd
import os

# --- ARQUIVO DE BANCO DE DADOS (CSV) ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    """Carrega dados do arquivo CSV de forma robusta para persistência de dados."""
    try:
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])
    except Exception as e:
        st.error(f"Erro ao acessar o banco de dados: {e}")
        return pd.DataFrame()

def salvar_recomendacao(nome, interesses, escolaridade, recomendacao):
    """Salva uma nova recomendação no banco de dados CSV."""
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

# --- INJEÇÃO DE CSS PERSONALIZADO (UI/UX) ---
st.markdown("""
<style>
    /* FUNDO E APP GLOBAL */
    .stApp {
        background-color: #F4F9FD; 
    }
    
    /* LOGOTIPO */
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

    /* TÍTULOS E HERO */
    .hero-title {
        text-align: center;
        color: #3A7CA5;
        font-size: 22px;
        margin-bottom: 20px;
    }
    .test-header-title { 
        color: #1A5276; 
        font-size: 28px; /* Aumentado conforme pedido */
        font-style: italic; 
        font-weight: bold; 
        text-align: center; 
        margin-top: -15px; /* Reposicionado para cima */
        margin-bottom: 15px; 
    }
    .test-banner { 
        background: linear-gradient(180deg, #D6EAF8, #EBF5FB); 
        color: #1A5276; 
        text-align: center; 
        padding: 15px; 
        border-radius: 12px;
        font-size: 16px; 
        margin-bottom: 25px; 
    }

    /* BOTÃO ESTILO PÍLULA LARANJA (CENTRALIZADO) */
    div.stButton > button {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important;
        border: none !important;
        border-radius: 35px !important;
        padding: 12px 50px !important; 
        font-size: 20px !important; 
        font-weight: bold !important;
        display: block !important;
        margin: 25px auto !important; /* Força centralização */
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4) !important;
        transition: transform 0.2s !important;
        min-width: 280px !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) !important;
    }

    /* FORMULÁRIO */
    .question-title { 
        color: #1A5276; 
        font-size: 16px; 
        font-weight: bold; 
        border-bottom: 1px solid #D4E6F1; 
        padding-bottom: 5px; 
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* FEATURE ICONS (LANDING) */
    .flex-features-container {
        display: flex;
        justify-content: space-around; 
        margin-top: 30px;
        padding-bottom: 30px;
    }
    .flex-feature-item {
        display: flex;
        flex-direction: column;
        align-items: center;
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

    /* CARDS DE RESULTADOS (TELA 3) */
    .results-header { text-align: center; margin-bottom: 25px; }
    .results-title { color: #1A5276; font-size: 24px; font-weight: 800; }
    .rec-card { 
        background: white; 
        border-radius: 15px; 
        padding: 15px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06); 
        margin-bottom: 20px; 
        display: flex;
        align-items: center;
    }
    .rec-card-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; margin-right: 15px; }
    .rec-card-title { color: #1A5276; font-size: 17px; font-weight: 800; margin-bottom: 3px; }
    .rec-card-desc { color: #555; font-size: 13px; line-height: 1.3; }
    .rec-card-reason { color: #2980B9; font-size: 12px; font-style: italic; margin-top: 5px; }

    /* FOOTER NAV (TELA 3) */
    .footer-nav-container { 
        display: flex; 
        justify-content: space-between; 
        margin-top: 30px; 
        border-top: 2px solid #EBF5FB; 
        padding: 20px 0; 
    }
    .footer-nav-item { text-align: center; width: 32%; }
    .footer-nav-icon { 
        width: 45px; height: 45px; border-radius: 50%; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 20px; color: white; margin: 0 auto 8px auto; 
    }
    .icon-green { background: linear-gradient(180deg, #48C9B0, #17A589); }
    .icon-orange { background: linear-gradient(180deg, #F39C12, #D35400); }
    .icon-blue { background: linear-gradient(180deg, #2980B9, #1A5276); }
    .footer-nav-text { font-size: 11px; color: #1A5276; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATA DE CARREIRAS (MODULARIZADA) ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Desenvolvedor de Software', 'description': 'Trilha de Programação FullStack', 'reason': 'Seu perfil analítico combina com engenharia.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Suporte Técnico TI', 'description': 'Infraestrutura e Redes', 'reason': 'Ótimo início para quem gosta de hardware.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Gestor de Projetos', 'description': 'Metodologias Ágeis e Liderança', 'reason': 'Ideal para quem busca cargos executivos.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Médio', 'Ensino Superior'], 'career': {'title': 'Designer UX/UI', 'description': 'Criação de Interfaces Digitais', 'reason': 'Sua criatividade focada no usuário.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400'}},
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Analista Clínico', 'description': 'Gestão de Dados Laboratoriais', 'reason': 'Une saúde com precisão técnica.', 'image': 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?q=80&w=400'}}
]

def get_career_recommendation(selected_interests, selected_education):
    matches = [c['career'] for c in career_database if any(i in c['interests'] for i in selected_interests) and selected_education in c['education']]
    return matches if matches else [{'title': 'Empreendedor Digital', 'description': 'Gestão de Novos Negócios', 'reason': 'Perfil versátil e inovador.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400'}]

# --- TELA 1: LANDING PAGE ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso Profissional</h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800" width="380" style="border-radius:20px;"></div>', unsafe_allow_html=True)
    
    if st.button("Comece Agora"):
        st.session_state.page = 'test'
        st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-blue-small">👤</div><div class="feature-text-small">Teste</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-yellow-small">📋</div><div class="feature-text-small">Trilhas</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-red-small">🎓</div><div class="feature-text-small">Dicas</div></div>
        </div>
    """, unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO DE TESTE ---
def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    st.markdown("<div class='test-banner'>Nos ajude a conhecer você melhor para sugerir a melhor trilha.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='question-title'>Qual o seu nome?</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Digite seu nome...", label_visibility="collapsed")
    
    st.markdown("<div class='question-title'>Quais são seus principais interesses?</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        t = st.checkbox("Tecnologia")
        s = st.checkbox("Saúde")
    with c2:
        n = st.checkbox("Negócios")
        a = st.checkbox("Artes & Design")
    
    st.markdown("<div class='question-title'>Qual seu nível de escolaridade?</div>", unsafe_allow_html=True)
    edu = st.radio("", ["Ensino Médio", "Ensino Superior", "Pós-Graduação"], label_visibility="collapsed")
    
    selected_interests = [i for i, v in zip(["Tecnologia", "Negócios", "Saúde", "Artes & Design"], [t, n, s, a]) if v]

    if st.button("Continuar"):
        if not name.strip() or not selected_interests:
            st.warning("⚠️ Preencha seu nome e escolha ao menos um interesse.")
        else:
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_interests, edu)
            salvar_recomendacao(name, selected_interests, edu, st.session_state.recommended_careers[0]['title'])
            st.session_state.page = 'results'
            st.rerun()

# --- TELA 3: RESULTADOS ---
def show_results_page():
    st.markdown(f"<div class='test-header-title'>Resultados para {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.markdown("<div class='results-header'>Baseado no seu perfil, aqui estão as melhores opções:</div>", unsafe_allow_html=True)

    for career in st.session_state.recommended_careers:
        st.markdown(f"""
        <div class="rec-card">
            <img src="{career['image']}" class="rec-card-img">
            <div>
                <div class="rec-card-title">{career['title']}</div>
                <div class="rec-card-desc">{career['description']}</div>
                <div class="rec-card-reason">{career['reason']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer-nav-container">
            <div class="footer-nav-item"><div class="footer-nav-icon icon-green">🏆</div><div class="footer-nav-text">Cursos</div></div>
            <div class="footer-nav-item"><div class="footer-nav-icon icon-orange">⚙️</div><div class="footer-nav-text">Habilidades</div></div>
            <div class="footer-nav-item"><div class="footer-nav-icon icon-blue">👤</div><div class="footer-nav-text">Dicas</div></div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Refazer Teste"):
        st.session_state.page = 'test'
        st.rerun()

# --- CONTROLE DE NAVEGAÇÃO ---
if st.session_state.page == 'landing': show_landing_page()
elif st.session_state.page == 'test': show_profile_test_page()
elif st.session_state.page == 'results': show_results_page()

st.divider()
if st.checkbox("⚙️ Modo Administrador (Ver CSV)"):
    st.dataframe(carregar_dados())