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

# --- CONFIGURAÇÃO DA PÁGINA (Estado da Sessão) ---
if 'page' not in st.session_state:
    st.session_state.page = 'test' 
if 'recommended_careers' not in st.session_state:
    st.session_state.recommended_careers = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.set_page_config(page_title="AprendaJá PRO - Seu Caminho", page_icon="🎯", layout="centered")

# --- INJEÇÃO DE CSS PERSONALIZADO (A Mágica do Design) ---
st.markdown("""
<style>
    /* Estilo para os Cards de Teste e Resultado */
    .stContainer {
        border: 2px solid #A32E2E;
        border-radius: 15px;
        padding: 20px;
        background-color: #2D2D31;
        margin-bottom: 20px;
    }
    
    /* Estilo para Títulos dentro dos Cards */
    .career-title {
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 5px !important;
    }
    
    /* Estilo para Descrições */
    .career-description {
        color: #DEDEDE !important;
        font-size: 15px;
        margin-bottom: 15px;
        line-height: 1.4;
    }

    /* Estilo para a justificativa do perfil */
    .career-reason {
        color: #FF8A8A !important;
        font-size: 14px;
        font-style: italic;
        margin-top: 5px;
    }

    /* Estilo para os botões de Navegação (Vinho) */
    .stButton > button {
        background-color: #A32E2E;
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #7A2222;
        color: white !important;
    }
    
    /* Centralizar ícones nas colunas de interesse */
    .interest-icon {
        font-size: 50px;
        text-align: center;
        display: block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DE CARREIRAS ---
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

# --- FUNÇÕES DE PÁGINA ---

def show_profile_test_page():
    st.markdown("## AprendaJá **PRO** 🎯")
    st.divider()
    st.markdown("## Perfil Profissional: Nos ajude a conhecer você melhor.")
    
    name = st.text_input("Qual seu nome?")
    
    st.write("Quais são seus principais interesses?")
    int_col1, int_col2, int_col3, int_col4 = st.columns(4)
    
    with int_col1:
        st.markdown("<span class='interest-icon'>💻</span>", unsafe_allow_html=True)
        tech_check = st.checkbox("Tecnologia")
    with int_col2:
        st.markdown("<span class='interest-icon'>🤝</span>", unsafe_allow_html=True)
        biz_check = st.checkbox("Negócios")
    with int_col3:
        st.markdown("<span class='interest-icon'>🩺</span>", unsafe_allow_html=True)
        health_check = st.checkbox("Saúde")
    with int_col4:
        st.markdown("<span class='interest-icon'>🎨</span>", unsafe_allow_html=True)
        design_check = st.checkbox("Artes & Design")
    
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
    selected_education_label = st.radio("Escolha uma opção:", list(education_options.keys()))
    selected_education = education_options[selected_education_label]
    
    # Validação do formulário
    if st.button("Continuar"):
        if not name.strip():
            st.warning("⚠️ Por favor, digite seu nome antes de continuar.")
        elif len(selected_interests) == 0:
            st.warning("⚠️ Por favor, escolha pelo menos um interesse (Tecnologia, Negócios, Saúde ou Artes).")
        else:
            # Se passou na validação, avança!
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
            
            if st.session_state.recommended_careers:
                 salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
                 
            st.session_state.page = 'results'
            st.rerun() # Força a tela a atualizar imediatamente

def show_results_page():
    st.markdown("## AprendaJá **PRO** 🎯")
    
    # Removido o <
    if st.button("Voltar para o Teste"): 
        st.session_state.page = 'test'
        st.rerun()
        
    st.title("Suas Recomendações de Carreira")
    st.subheader(f"Escolhas alinhadas ao seu perfil, {st.session_state.user_name}!")
    
    st.divider()

    for i in range(0, len(st.session_state.recommended_careers), 2):
        card_col1, card_col2 = st.columns(2)
        
        if i < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i]
            with card_col1.container():
                inner_col1, inner_col2 = st.columns([1, 2])
                with inner_col1:
                    st.image(career['image'], use_column_width=True)
                with inner_col2:
                    st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='career-reason'>💡 <b>Por que combina?</b><br>{career['reason']}</p>", unsafe_allow_html=True)
                    # Botão Saiba Mais removido daqui

        if i+1 < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i+1]
            with card_col2.container():
                inner_col1, inner_col2 = st.columns([1, 2])
                with inner_col1:
                    st.image(career['image'], use_column_width=True)
                with inner_col2:
                    st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='career-reason'>💡 <b>Por que combina?</b><br>{career['reason']}</p>", unsafe_allow_html=True)
                    # Botão Saiba Mais removido daqui

# --- FLUXO PRINCIPAL DO APP ---
if st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()

st.divider()
if st.checkbox("⚙️ Modo Administrador: Ver Banco de Dados (CSV)"):
    df = carregar_dados()
    st.dataframe(df)