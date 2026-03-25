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

# --- INJEÇÃO DE CSS PERSONALIZADO (MANTIDO INTACTO) ---
st.markdown("""
<style>
    .stApp, header { background-color: #F4F9FD !important; }
    .logo-container { text-align: center; padding-top: 10px; margin-bottom: 20px; }
    .logo-text { font-size: 32px; font-weight: 800; color: #3A7CA5 !important; font-family: 'Arial', sans-serif; }
    .logo-badge { background: linear-gradient(90deg, #F39C12, #D35400) !important; color: white !important; padding: 4px 10px; border-radius: 8px; font-size: 18px; font-weight: bold; vertical-align: super; margin-left: 5px; }
    .hero-title { text-align: center; color: #3A7CA5 !important; font-size: 22px; margin-bottom: 20px; }
    .test-header-title { color: #1A5276 !important; font-size: 24px; font-style: italic; font-weight: bold; text-align: center; margin-top: 10px; margin-bottom: 15px; }
    .test-banner { background: linear-gradient(180deg, #D6EAF8, #EBF5FB) !important; color: #1A5276 !important; text-align: center; padding: 15px; border-radius: 12px; font-size: 16px; margin-bottom: 25px; font-weight: 600; }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important; border: none !important; border-radius: 35px !important;
        padding: 12px 20px !important; font-size: 20px !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4) !important; transition: transform 0.2s !important; width: 100% !important; 
    }
    div.stButton > button[kind="primary"]:hover { transform: scale(1.02) !important; }

    .question-title { color: #1A5276 !important; font-size: 16px; font-weight: bold; border-bottom: 1px solid #D4E6F1 !important; padding-bottom: 5px; margin-top: 20px; margin-bottom: 15px; }
    .stTextInput input { background-color: #FFFFFF !important; color: #1A5276 !important; border: 2px solid #D4E6F1 !important; border-radius: 8px !important; }
    .stCheckbox label, .stRadio label, .stCheckbox p, .stRadio p { color: #2C3E50 !important; }

    .flex-features-container { display: flex; justify-content: space-around; margin-top: 30px; padding-bottom: 30px; }
    .flex-feature-item { display: flex; flex-direction: column; align-items: center; }
    .feature-icon-circle-small { width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .bg-blue-small { background-color: #5DADE2 !important; color: white !important; }
    .bg-yellow-small { background-color: #F4D03F !important; color: white !important; }
    .bg-red-small { background-color: #E74C3C !important; color: white !important; }
    .feature-text-small { font-size: 13px; color: #555 !important; font-weight: 600; text-align: center;}

    .results-header { text-align: center; margin-bottom: 25px; color: #1A5276 !important; font-weight: bold;}
    .rec-card { background: white !important; border-radius: 15px; padding: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; display: flex; align-items: center; }
    .rec-card-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; margin-right: 15px; }
    .rec-card-title { color: #1A5276 !important; font-size: 17px; font-weight: 800; margin-bottom: 3px; line-height: 1.2;}
    .rec-card-desc { color: #555 !important; font-size: 13px; line-height: 1.3; }
    .rec-card-reason { color: #2980B9 !important; font-size: 12px; font-style: italic; margin-top: 5px; }

    .footer-nav-container { display: flex; justify-content: space-between; margin-top: 30px; border-top: 2px solid #EBF5FB !important; padding: 20px 0; }
    .footer-nav-item { text-align: center; width: 32%; }
    .footer-nav-icon { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white !important; margin: 0 auto 8px auto; }
    .icon-green { background: linear-gradient(180deg, #48C9B0, #17A589) !important; }
    .icon-orange { background: linear-gradient(180deg, #F39C12, #D35400) !important; }
    .icon-blue { background: linear-gradient(180deg, #2980B9, #1A5276) !important; }
    .footer-nav-text { font-size: 11px; color: #1A5276 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATA DE CARREIRAS (EXPANDIDA E CORRIGIDA) ---
# Agora temos opções extremamente precisas para CADA cruzamento de dados.
career_database = [
    # SAÚDE
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Pesquisador Científico Médico', 'description': 'Inovação e Estudos Clínicos', 'reason': 'Sua especialização permite atuar na vanguarda da ciência médica.', 'image': 'https://images.unsplash.com/photo-1532187863486-abf9db09e412?q=80&w=400'}}, # Imagem Microscópio
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Especialista Clínico', 'description': 'Atendimento e Cuidado Direto', 'reason': 'Aplica seus conhecimentos superiores no cuidado direto aos pacientes.', 'image': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=400'}}, # Imagem Médico/Hospital
    {'interests': ['Saúde'], 'education': ['Ensino Médio'], 'career': {'title': 'Técnico em Enfermagem', 'description': 'Apoio Fundamental em Saúde', 'reason': 'Excelente porta de entrada para uma carreira dedicada a salvar vidas.', 'image': 'https://images.unsplash.com/photo-1584432810601-6c7f27d2362b?q=80&w=400'}}, # Imagem Estetoscópio

    # TECNOLOGIA
    {'interests': ['Tecnologia'], 'education': ['Pós-Graduação'], 'career': {'title': 'Cientista de Dados (IA)', 'description': 'Modelagem e Machine Learning', 'reason': 'Ideal para liderar o futuro com análises e algoritmos complexos.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior'], 'career': {'title': 'Engenheiro de Software', 'description': 'Criação de Sistemas e Apps', 'reason': 'Sua afinidade tecnológica tem a base perfeita para construir softwares.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Analista de Suporte de TI', 'description': 'Manutenção de Redes e Sistemas', 'reason': 'Ótima posição prática para iniciar no mercado tech.', 'image': 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=400'}},

    # NEGÓCIOS
    {'interests': ['Negócios'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Consultor Estratégico', 'description': 'Gestão e Planejamento Corporativo', 'reason': 'Perfil focado em liderança e tomadas de decisão de alto impacto.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400'}},
    {'interests': ['Negócios'], 'education': ['Ensino Médio'], 'career': {'title': 'Empreendedor / Comercial', 'description': 'Vendas e Novos Negócios', 'reason': 'Sua visão de negócios permite crescer rápido na área comercial.', 'image': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?q=80&w=400'}},

    # ARTES & DESIGN
    {'interests': ['Artes & Design'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Designer de Produto (UX/UI)', 'description': 'Experiência do Usuário e Visual', 'reason': 'Une sua criatividade com metodologias de design avançadas.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Médio'], 'career': {'title': 'Assistente de Criação', 'description': 'Edição e Produção Visual', 'reason': 'Perfeito para exercitar habilidades criativas e portfólio prático.', 'image': 'https://images.unsplash.com/photo-1626785774573-4b799315345d?q=80&w=400'}},

    # ENGENHARIA (NOVO)
    {'interests': ['Engenharia'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Engenheiro de Projetos', 'description': 'Infraestrutura e Planejamento', 'reason': 'Mente focada em estruturação e cálculos de alta complexidade.', 'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=400'}},
    {'interests': ['Engenharia'], 'education': ['Ensino Médio'], 'career': {'title': 'Técnico em Mecatrônica', 'description': 'Automação e Processos', 'reason': 'Habilidade prática essencial para a indústria 4.0.', 'image': 'https://images.unsplash.com/photo-1581092335397-9583eb92d232?q=80&w=400'}},

    # COMUNICAÇÃO (NOVO)
    {'interests': ['Comunicação'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Diretor de Comunicação e RP', 'description': 'Estratégia de Imagem e Marca', 'reason': 'Sua facilidade de articulação é fundamental para conectar marcas e público.', 'image': 'https://images.unsplash.com/photo-1557425955-df376b5903c8?q=80&w=400'}},
    {'interests': ['Comunicação'], 'education': ['Ensino Médio'], 'career': {'title': 'Social Media Júnior', 'description': 'Gestão de Redes Sociais', 'reason': 'Uso inteligente das mídias para gerar engajamento.', 'image': 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=400'}},

    # EDUCAÇÃO (NOVO)
    {'interests': ['Educação'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Docente e Pedagogo', 'description': 'Ensino e Coordenação Acadêmica', 'reason': 'Missão focada no desenvolvimento humano e transferência de conhecimento.', 'image': 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=400'}},
    {'interests': ['Educação'], 'education': ['Ensino Médio'], 'career': {'title': 'Auxiliar de Desenvolvimento', 'description': 'Apoio em Treinamentos', 'reason': 'Oportunidade prática de iniciar no ambiente de aprendizado e suporte.', 'image': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?q=80&w=400'}},

    # MEIO AMBIENTE (NOVO)
    {'interests': ['Meio Ambiente'], 'education': ['Pós-Graduação', 'Ensino Superior'], 'career': {'title': 'Engenheiro Ambiental', 'description': 'Sustentabilidade e Gestão Ecológica', 'reason': 'Seu interesse se alinha com as urgências globais de sustentabilidade corporativa.', 'image': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400'}},
    {'interests': ['Meio Ambiente'], 'education': ['Ensino Médio'], 'career': {'title': 'Técnico Agrícola / Ambiental', 'description': 'Ações em Campo e Conservação', 'reason': 'Atuação direta e essencial com o meio ambiente e agro.', 'image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=400'}}
]

def get_career_recommendation(selected_interests, selected_education):
    matches = []
    for c in career_database:
        if any(i in c['interests'] for i in selected_interests) and selected_education in c['education']:
            matches.append(c['career'])
            
    if matches:
        return matches
    else:
        # Fallback de segurança 
        return [{'title': 'Empreendedor Inovador', 'description': 'Gestão de Novos Negócios', 'reason': 'Perfil versátil e adaptável a diversos cenários.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400'}]

# --- TELA 1: LANDING PAGE ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso Profissional</h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800" width="100%" style="max-width:380px; border-radius:20px;"></div>', unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Comece Agora", type="primary", use_container_width=True):
            st.session_state.page = 'test'
            st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-blue-small">👤</div><div class="feature-text-small">Teste</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-yellow-small">📋</div><div class="feature-text-small">Trilhas</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-red-small">🎓</div><div class="feature-text-small">Dicas</div></div>
        </div>
    """, unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO DE TESTE (ACRESCENTADO NOVOS INTERESSES) ---
def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    st.markdown("<div class='test-banner'>Nos ajude a conhecer você melhor para sugerir a melhor trilha.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='question-title'>Qual o seu nome?</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Digite seu nome...", label_visibility="collapsed")
    
    st.markdown("<div class='question-title'>Quais são seus principais interesses?</div>", unsafe_allow_html=True)
    
    # 8 Interesses divididos em 2 colunas como solicitado
    c1, c2 = st.columns(2)
    with c1:
        t = st.checkbox("Tecnologia")
        s = st.checkbox("Saúde")
        eng = st.checkbox("Engenharia")
        edu_area = st.checkbox("Educação")
    with c2:
        n = st.checkbox("Negócios")
        a = st.checkbox("Artes & Design")
        com = st.checkbox("Comunicação")
        amb = st.checkbox("Meio Ambiente")
    
    st.markdown("<div class='question-title'>Qual seu nível de escolaridade?</div>", unsafe_allow_html=True)
    edu = st.radio("", ["Ensino Médio", "Ensino Superior", "Pós-Graduação"], label_visibility="collapsed")
    
    # Lista atualizada capturando todos os novos botões
    interesses_lista = ["Tecnologia", "Saúde", "Engenharia", "Educação", "Negócios", "Artes & Design", "Comunicação", "Meio Ambiente"]
    valores_checkbox = [t, s, eng, edu_area, n, a, com, amb]
    selected_interests = [i for i, v in zip(interesses_lista, valores_checkbox) if v]

    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continuar", type="primary", use_container_width=True):
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
    st.markdown("""
        <div class="logo-container" style="text-align: left; padding-top: 0; margin-bottom: 0px;">
            <span class="logo-text" style="font-size: 24px;">AprendaJá</span><span class="logo-badge" style="font-size: 14px;">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='test-header-title' style='margin-top:20px;'>Resultados para {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.markdown("<div class='results-header'>Baseado no seu perfil, aqui estão as melhores opções:</div>", unsafe_allow_html=True)

    for career in st.session_state.recommended_careers:
        st.markdown(f"""
        <div class="rec-card">
            <img src="{career['image']}" class="rec-card-img">
            <div>
                <div class="rec-card-title">{career['title']}</div>
                <div class="rec-card-desc">{career['description']}</div>
                <div class="rec-card-reason">💡 {career['reason']}</div>
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

    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Refazer Teste", type="primary", use_container_width=True):
            st.session_state.page = 'test'
            st.rerun()

# --- CONTROLE DE NAVEGAÇÃO ---
if st.session_state.page == 'landing': show_landing_page()
elif st.session_state.page == 'test': show_profile_test_page()
elif st.session_state.page == 'results': show_results_page()

st.divider()
if st.checkbox("⚙️ Modo Administrador (Ver CSV)"):
    st.dataframe(carregar_dados())