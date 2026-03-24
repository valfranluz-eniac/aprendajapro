import streamlit as st
import pandas as pd
import os

# --- ARQUIVO DE BANCO DE DADOS (CSV) ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        except:
            return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])
    else:
        return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])

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

    /* BOTÃO PRIMÁRIO (CORRIGIDO PARA NÃO QUEBRAR O TEXTO) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #F39C12, #D35400);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 15px; 
        font-size: 20px; 
        font-weight: bold;
        width: 100%; /* Largura total dentro da coluna do Streamlit */
        white-space: nowrap; /* Impede o texto de quebrar de linha */
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4);
        transition: transform 0.2s;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        color: white;
    }

    /* REFINAMENTOS FEATURE ICONS (ICONE EM CIMA, TEXTO EMBAIXO, SEM ESTOURAR) */
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
        flex-direction: column; /* Coloca o icone em cima e o texto embaixo */
        align-items: center;
        width: 30%; /* Distribui por igual */
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
        margin-bottom: 8px; /* Espaço entre o ícone e a palavra */
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

    /* ESTILOS DAS OUTRAS TELAS */
    .test-header-title { color: #1A5276; font-size: 18px; font-style: italic; font-weight: bold; text-align: center; margin-top: 10px; }
    .test-banner { background: linear-gradient(180deg, #D6EAF8, #EBF5FB); color: #1A5276; text-align: center; padding: 15px; font-size: 16px; font-weight: 500; margin-top: 10px; margin-bottom: 20px; }
    .question-title { color: #1A5276; font-size: 15px; font-weight: bold; border-bottom: 1px solid #D4E6F1; padding-bottom: 5px; margin-bottom: 15px; margin-top: 20px; }

    div.stButton > button[kind="secondary"] {
        background: linear-gradient(180deg, #2980B9, #1A5276);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button[kind="secondary"]:hover { background: linear-gradient(180deg, #1A5276, #154360); }

    /* TELAS DE RESULTADOS (3) */
    .top-menu-icon { text-align: right; font-size: 28px; color: #2980B9; margin-bottom: -10px; }
    .results-header { text-align: center; margin-bottom: 25px; }
    .results-title { color: #1A5276; font-size: 24px; font-weight: 800; margin-bottom: 5px; }
    .results-subtitle { color: #3A7CA5; font-size: 14px; font-style: italic; }
    .results-subtitle span { color: #D4E6F1; margin: 0 5px; }
    .rec-card { background: white; border-radius: 15px; padding: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; }
    .rec-card-top { display: flex; align-items: center; margin-bottom: 15px; }
    .rec-card-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; margin-right: 15px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
    .rec-card-text { flex: 1; }
    .rec-card-title { color: #1A5276; font-size: 17px; font-weight: 800; margin-bottom: 3px; line-height: 1.2; }
    .rec-card-desc { color: #555; font-size: 13px; line-height: 1.3; }
    .rec-card-reason { color: #2980B9; font-size: 12px; font-style: italic; margin-top: 5px; }
    .rec-card-btn { background: linear-gradient(180deg, #2980B9, #1A5276); color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 15px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    .footer-nav-container { display: flex; justify-content: space-between; margin-top: 30px; border-top: 2px solid #EBF5FB; padding-top: 20px; padding-bottom: 20px; }
    .footer-nav-item { text-align: center; width: 32%; }
    .footer-nav-icon { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: white; margin: 0 auto 8px auto; box-shadow: 0 4px 6px rgba(0,0,0,0.15); }
    .footer-nav-text { font-size: 11px; color: #1A5276; font-weight: bold; line-height: 1.1; }
    .icon-green { background: linear-gradient(180deg, #48C9B0, #17A589); }
    .icon-orange { background: linear-gradient(180deg, #F39C12, #D35400); }
    .icon-blue { background: linear-gradient(180deg, #2980B9, #1A5276); }
    
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DE CARREIRAS ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Desenvolvedor de Software', 'description': 'Trilha de Programação Completa', 'reason': 'Ideal para seu perfil analítico e foco em tecnologia avançada.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Suporte em TI', 'description': 'Iniciação à Infraestrutura e Redes', 'reason': 'Ótimo ponto de partida técnico para sua afinidade com tecnologia.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Marketing Digital', 'description': 'Curso de Estratégia & Mídias Sociais', 'reason': 'Combina perfeitamente com sua visão de negócios e comunicação.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Design Gráfico UX/UI', 'description': 'Criação de Interfaces e Experiências', 'reason': 'Sua criatividade será fundamental para inovar nesta área.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Gestão em Saúde', 'description': 'Administração de Clínicas e Hospitais', 'reason': 'Une o cuidado da saúde com a visão gerencial moderna.', 'image': 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Pesquisa Científica', 'description': 'Inovação em Tratamentos Médicos', 'reason': 'Sua formação avançada permite atuar na linha de frente da ciência.', 'image': 'https://images.unsplash.com/photo-1584447128309-b66b7a14890c?q=80&w=400&auto=format&fit=crop'}}
]

def get_career_recommendation(selected_interests, selected_education):
    possible_careers = []
    for option in career_database:
        if any(interest in option['interests'] for interest in selected_interests) and selected_education in option['education']:
            possible_careers.append(option['career'])
    if possible_careers:
        return possible_careers 
    else:
        return [{'title': 'Empreendedor Inovador', 'description': 'Gestão de Negócios e Startups', 'reason': 'Perfil versátil que se adapta a múltiplas frentes de mercado.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400&auto=format&fit=crop'}]

# --- TELA 1: LANDING PAGE ---
def show_landing_page():
    st.markdown("""
        <div class="logo-container">
            <span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso Profissional</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-image-container">
            <img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800&t=st=1708450000~exp=1708450600~hmac=abcd123" alt="Estudantes">
        </div>
    """, unsafe_allow_html=True)
    
    # CENTRALIZANDO O BOTÃO COM COLUNAS DO STREAMLIT (Resolve o esmagamento)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Comece Agora", type="primary", use_container_width=True):
            st.session_state.page = 'test'
            st.rerun()
        
    st.write("") 
    st.write("")
    
    # ÍCONES ALINHADOS (Ícone em cima, texto curto embaixo para não estourar a tela)
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
    col_back, col_title, col_empty = st.columns([1, 6, 1])
    with col_back:
        if st.button("‹", type="secondary"):
            st.session_state.page = 'landing'
            st.rerun()
    with col_title:
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
    
    selected_interests = []
    if tech_check: selected_interests.append("Tecnologia")
    if biz_check: selected_interests.append("Negócios")
    if health_check: selected_interests.append("Saúde")
    if design_check: selected_interests.append("Artes & Design")
        
    st.markdown("<div class='question-title'>Qual seu nível de escolaridade?</div>", unsafe_allow_html=True)
    education_options = {
        "Ensino Médio": "Ensino Médio",
        "Ensino Superior": "Ensino Superior",
        "Pós-Graduação": "Pós-Graduação"
    }
    selected_education_label = st.radio("", list(education_options.keys()), label_visibility="collapsed")
    selected_education = education_options[selected_education_label]
    
    st.write("") 
    if st.button("Continuar", type="secondary"):
        if not name.strip():
            st.warning("⚠️ Por favor, digite seu nome antes de continuar.")
        elif len(selected_interests) == 0:
            st.warning("⚠️ Por favor, escolha pelo menos um interesse.")
        else:
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
            if st.session_state.recommended_careers:
                 salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
            st.session_state.page = 'results'
            st.rerun()

# --- TELA 3: RESULTADOS ---
def show_results_page():
    st.markdown("<div class='top-menu-icon'>≡</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="results-header">
            <div class="results-title">Suas Recomendações de Carreira</div>
            <div class="results-subtitle"><span>—</span> Escolhas alinhadas ao seu perfil! <span>—</span></div>
        </div>
    """, unsafe_allow_html=True)

    for career in st.session_state.recommended_careers:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-card-top">
                <img src="{career['image']}" class="rec-card-img">
                <div class="rec-card-text">
                    <div class="rec-card-title">{career['title']}</div>
                    <div class="rec-card-desc">{career['description']}</div>
                    <div class="rec-card-reason">{career['reason']}</div>
                </div>
            </div>
            <div class="rec-card-btn">Saiba Mais</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer-nav-container">
            <div class="footer-nav-item">
                <div class="footer-nav-icon icon-green">🏆</div>
                <div class="footer-nav-text">Cursos<br>Recomendados</div>
            </div>
            <div class="footer-nav-item">
                <div class="footer-nav-icon icon-orange">⚙️</div>
                <div class="footer-nav-text">Habilidades<br>em Alta</div>
            </div>
            <div class="footer-nav-item">
                <div class="footer-nav-icon icon-blue">👤</div>
                <div class="footer-nav-text">Dicas de<br>Empregabilidade</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("Voltar para o Teste", type="secondary"): 
        st.session_state.page = 'test'
        st.rerun()

# --- GERENCIADOR DE ROTAS ---
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()

st.divider()
if st.checkbox("⚙️ Modo Administrador: Ver Banco de Dados (CSV)"):
    df = carregar_dados()
    st.dataframe(df)