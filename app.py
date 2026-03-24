import streamlit as st
import pandas as pd
import os

# --- ARQUIVO DE BANCO DE DADOS (CSV) ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    # Tenta carregar os dados. Se o arquivo estiver corrompido ou vazio, o try/except garante que um novo banco de dados seja criado.
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
    st.session_state.page = 'landing' # Agora começamos na Landing Page!
if 'recommended_careers' not in st.session_state:
    st.session_state.recommended_careers = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.set_page_config(page_title="AprendaJá PRO", page_icon="🚀", layout="centered")

# --- INJEÇÃO DE CSS PERSONALIZADO (Design System Completo) ---
st.markdown("""
<style>
    /* RESET BÁSICO E CORES DO TEMA GLOBAL */
    .stApp {
        background-color: #F4F9FD; /* Fundo azul bem clarinho como na foto */
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
        color: #3A7CA5; /* Azul do logo */
        font-family: 'Arial', sans-serif;
    }
    .logo-badge {
        background: linear-gradient(90deg, #F39C12, #D35400); /* Gradiente Laranja */
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        vertical-align: super;
        margin-left: 5px;
    }

    /* --- TELA 1 (REFINAMENTOS FOTO 1) --- */
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

    /* BOTÃO PRIMÁRIO (COMECE AGORA - CENTRALIZADO E MENOR) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #F39C12, #D35400);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 15px; /* Reduzi padding */
        font-size: 20px; /* Reduzi font-size */
        font-weight: bold;
        width: 60%; /* Reduzi largura */
        margin: 0 auto; /* Centralizado */
        display: block; /* Essencial para margin-auto funcionar */
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4);
        transition: transform 0.2s;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        color: white;
    }

    /* REFINAMENTOS FEATURE ICONS (UM LINHA, MENOR) */
    .flex-features-container {
        display: flex;
        justify-content: space-around; /* Distribuição uniforme */
        align-items: center; /* Alinhamento vertical central */
        margin-top: 25px;
        margin-bottom: 20px;
    }
    .flex-feature-item {
        text-align: center;
        display: flex;
        align-items: center; /* Alinhamento ícone e texto na mesma linha */
    }
    .feature-icon-circle-small {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px; /* Reduzi tamanho */
        height: 45px; /* Reduzi tamanho */
        border-radius: 50%;
        font-size: 20px; /* Reduzi font-size */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-right: 8px; /* Espaço entre ícone e texto */
    }
    /* Cores individuais dos círculos pequenos */
    .bg-blue-small { background-color: #5DADE2; color: white; }
    .bg-yellow-small { background-color: #F4D03F; color: white; }
    .bg-red-small { background-color: #E74C3C; color: white; }
    
    .feature-text-small {
        font-size: 13px; /* Reduzi font-size */
        color: #555;
        font-weight: 600;
        white-space: nowrap; /* Impede quebra de linha do texto curto */
    }

    /* --- ESTILOS DAS OUTRAS TELAS (MANTER) --- */
    div.stButton > button[kind="secondary"] {
        background-color: #2C3E50;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #1A252F;
        color: white;
    }

    .result-card {
        background-color: white;
        border: 2px solid #E5E7E9;
        border-left: 6px solid #D35400; 
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .career-title { color: #2C3E50 !important; font-size: 22px !important; font-weight: 800 !important; margin-bottom: 5px !important; }
    .career-description { color: #555555 !important; font-size: 15px; margin-bottom: 10px; }
    .career-reason { background-color: #FDF2E9; padding: 10px; border-radius: 8px; color: #D35400 !important; font-size: 14px; font-style: italic; margin-top: 10px; }
    
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DE CARREIRAS ---
# ... (manter o mesmo banco de dados) ...
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Programador de Softwares', 'description': 'Crie aplicativos e sistemas de alta tecnologia.', 'reason': 'Com seu interesse em tecnologia e formação acadêmica avançada, você possui a base ideal para criar lógicas complexas e inovar no mercado digital.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Analista de Dados Júnior', 'description': 'Comece na área de dados transformando números em decisões.', 'reason': 'Você tem afinidade com tecnologia e está no momento perfeito para iniciar uma trilha técnica muito requisitada pelas empresas.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Gestor de Projetos', 'description': 'Lidere equipes e gerencie negócios de sucesso.', 'reason': 'Seu foco em negócios demonstra um perfil de liderança e visão estratégica, essencial para gerenciar processos e pessoas.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Designer Criativo', 'description': 'Projete interfaces e experiências visuais inovadoras.', 'reason': 'Sua escolha por artes indica alta criatividade e empatia visual, habilidades chave para se destacar no mercado criativo.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Especialista em Saúde', 'description': 'Atue no cuidado e bem-estar em áreas clínicas.', 'reason': 'O interesse em saúde e sua formação superior refletem sua dedicação técnica e vocação para o cuidado humano.', 'image': 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?q=80&w=400&auto=format&fit=crop'}},
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Pesquisador em Saúde', 'description': 'Desenvolva soluções avançadas para a área médica.', 'reason': 'Sua pós-graduação aliada à saúde te coloca em uma posição de destaque para pesquisas e inovações científicas.', 'image': 'https://images.unsplash.com/photo-1584447128309-b66b7a14890c?q=80&w=400&auto=format&fit=crop'}}
]

def get_career_recommendation(selected_interests, selected_education):
    possible_careers = []
    for option in career_database:
        if any(interest in option['interests'] for interest in selected_interests) and selected_education in option['education']:
            possible_careers.append(option['career'])
    if possible_careers:
        return possible_careers 
    else:
        return [{'title': 'Empreendedor Inovador', 'description': 'Crie seu próprio caminho unindo diferentes áreas do conhecimento.', 'reason': 'Seu perfil é versátil e não se prende a padrões! Essa combinação única te dá a base para empreender e inovar.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400&auto=format&fit=crop'}]

# --- TELA 1: LANDING PAGE (REFINADA) ---
def show_landing_page():
    # Logo
    st.markdown("""
        <div class="logo-container">
            <span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Título Principal
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso Profissional</h2>", unsafe_allow_html=True)
    
    # Imagem Hero (Ilustração vetorial)
    st.markdown("""
        <div class="hero-image-container">
            <img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800&t=st=1708450000~exp=1708450600~hmac=abcd123" alt="Estudantes trabalhando">
        </div>
    """, unsafe_allow_html=True)
    
    # Botão "Comece Agora" - NATIVO, CENTRALIZADO VIA CSS OVERSIDES
    # Chamo a função st.button em um container vazio para depois centralizar
    # st.button tem o tipo "primary" que eu estilizei acima
    with st.container():
        if st.button("Comece Agora", type="primary"):
            st.session_state.page = 'test'
            st.rerun()
        
    st.write("") # Espaço
    st.write("")
    
    # --- REVISÃO FEATURE ICONS (UMA LINHA, MENOR) ---
    # Removi st.columns(3). Usei HTML Flexbox puro.
    # O HTML abaixo cria uma linha com os três ícones menores lado a lado.
    
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-blue-small">👤</div>
                <div class="feature-text-small">✓ Teste de Perfil</div>
            </div>
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-yellow-small">📋</div>
                <div class="feature-text-small">✓ Trilhas Personalizadas</div>
            </div>
            <div class="flex-feature-item">
                <div class="feature-icon-circle-small bg-red-small">🎓</div>
                <div class="feature-text-small">✓ Dicas de Carreira</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO DE TESTE ---
# ... (manter o mesmo código das telas 2 e 3) ...
def show_profile_test_page():
    st.markdown("""
        <div class="logo-container" style="text-align: left; padding-top: 0;">
            <span class="logo-text" style="font-size: 24px;">AprendaJá</span><span class="logo-badge" style="font-size: 14px;">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h3 style='color: #2C3E50;'>Nos ajude a conhecer você melhor.</h3>", unsafe_allow_html=True)
    st.divider()
    
    name = st.text_input("Qual seu nome?")
    st.write("Quais são seus principais interesses?")
    
    col1, col2 = st.columns(2)
    with col1:
        tech_check = st.checkbox("💻 Tecnologia")
        health_check = st.checkbox("🩺 Saúde")
    with col2:
        biz_check = st.checkbox("🤝 Negócios")
        design_check = st.checkbox("🎨 Artes & Design")
    
    selected_interests = []
    if tech_check: selected_interests.append("Tecnologia")
    if biz_check: selected_interests.append("Negócios")
    if health_check: selected_interests.append("Saúde")
    if design_check: selected_interests.append("Artes & Design")
        
    st.write("Qual seu nível de escolaridade?")
    education_options = {
        "📖 Ensino Médio": "Ensino Médio",
        "🎓 Ensino Superior": "Ensino Superior",
        "🏅 Pós-Graduação": "Pós-Graduação"
    }
    selected_education_label = st.radio("Escolha uma opção:", list(education_options.keys()), label_visibility="collapsed")
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
# ... (manter o mesmo código das telas 2 e 3) ...
def show_results_page():
    st.markdown("""
        <div class="logo-container" style="text-align: left; padding-top: 0;">
            <span class="logo-text" style="font-size: 24px;">AprendaJá</span><span class="logo-badge" style="font-size: 14px;">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #2C3E50;'>Suas Recomendações</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #555; font-size: 16px;'>Escolhas alinhadas ao seu perfil, <b>{st.session_state.user_name}</b>!</p>", unsafe_allow_html=True)
    st.divider()

    for i in range(0, len(st.session_state.recommended_careers), 2):
        card_col1, card_col2 = st.columns(2)
        
        if i < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i]
            with card_col1:
                st.markdown(f"""
                <div class="result-card">
                    <img src="{career['image']}" style="width:100%; border-radius:10px; margin-bottom:15px;">
                    <div class="career-title">{career['title']}</div>
                    <div class="career-description">{career['description']}</div>
                    <div class="career-reason">💡 <b>Por que combina?</b><br>{career['reason']}</div>
                </div>
                """, unsafe_allow_html=True)

        if i+1 < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i+1]
            with card_col2:
                st.markdown(f"""
                <div class="result-card">
                    <img src="{career['image']}" style="width:100%; border-radius:10px; margin-bottom:15px;">
                    <div class="career-title">{career['title']}</div>
                    <div class="career-description">{career['description']}</div>
                    <div class="career-reason">💡 <b>Por que combina?</b><br>{career['reason']}</div>
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