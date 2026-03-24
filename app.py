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
        color: #FFFFFF;
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
    }
    
    /* Estilo para Descrições */
    .career-description {
        color: #DEDEDE;
        font-size: 16px;
        margin-bottom: 15px;
    }

    /* Estilo para os botões de Saiba Mais (Vinho) */
    .stButton > button {
        background-color: #A32E2E;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #7A2222;
        color: white;
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

# --- BASE DE DADOS DE CARREIRAS (O Especialista Simbólico) ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Programador de Softwares', 'description': 'Crie aplicativos e sistemas de alta tecnologia.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/codificacao.png'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Analista de Dados Júnior', 'description': 'Comece na área de dados transformando números em decisões.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/analise-de-dados.png'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior'], 'career': {'title': 'Gerente de Produto (PM)', 'description': 'Launch and manage your own product or business.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/gerenciamento-de-produtos.png'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'UX/UI Designer Sênior', 'description': 'Projete interfaces digitais intuitivas e inovadoras.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/design-ux-ui.png'}},
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Enfermeiro de UTI', 'description': 'Atue em uma área médica crítica e de alta demanda.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/enfermeiro.png'}},
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Médico Especialista', 'description': 'Torne-se referência em sua área médica.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/medico.png'}}
]

# Função que gera a recomendação com base nas regras do especialista
def get_career_recommendation(selected_interests, selected_education):
    if not selected_interests or not selected_education:
        return [{'title': 'Orientador de Carreiras Geral', 'description': 'Poxa, você não escolheu nada!', 'image': 'https://streamlit-career-images.s3.amazonaws.com/orientador-de-carreira.png'}]
        
    possible_careers = []
    # Percorre o banco de dados de regras
    for option in career_database:
        # Se houver UM interesse correspondente E a escolaridade bater, é uma opção!
        if any(interest in option['interests'] for interest in selected_interests) and selected_education in option['education']:
            possible_careers.append(option['career'])
    
    # Se não houver correspondência, damos um perfil versátil
    if possible_careers:
        return possible_careers # Devolve a lista completa de correspondências
    else:
        return [{'title': 'Empreendedor Geral', 'description': 'Um perfil versátil! Vamos conversar mais sobre sua trilha.', 'image': 'https://streamlit-career-images.s3.amazonaws.com/empreendedor.png'}]

# --- FUNÇÕES DE PÁGINA (Réplicas do Design) ---

def show_profile_test_page():
    # Navegação e Título (Design Réplica)
    st.markdown("## AprendaJá **PRO** 🎯")
    st.markdown("<h3 style='color: #888;'>Home > <span style='color: #FFFFFF;'>Teste de Perfil</span> > Recomendações</h3>", unsafe_allow_html=True)
    st.divider()
    st.markdown("## Perfil Profissional: Nos ajude a conhecer você melhor.")
    
    # Cadastro de nome
    name = st.text_input("Qual seu nome?")
    
    st.write("Quais são seus principais interesses?")
    # Layout de Colunas para os Interesses (Design Réplica - simulação dos branching lines)
    # Usamos st.columns para criar o grid de 4 colunas
    int_col1, int_col2, int_col3, int_col4 = st.columns(4)
    
    # Usaremos st.container() dentro das colunas para simular os cards com borda
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
    # Usaremos st.radio com ícones nas labels para o design
    education_options = {
        "📖 Ensino Médio": "Ensino Médio",
        "🎓 Ensino Superior": "Ensino Superior",
        "🏅 Pós-Graduação": "Pós-Graduação"
    }
    selected_education_label = st.radio("Escolha uma opção:", list(education_options.keys()))
    selected_education = education_options[selected_education_label]
    
    # Botão principal (Vinho)
    if st.button("Continuar"):
        st.session_state.user_name = name
        st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
        # Salva o cadastro no banco de dados CSV
        if st.session_state.recommended_careers:
             salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
        st.session_state.page = 'results'

def show_results_page():
    # Navegação e Título
    st.markdown("## AprendaJá **PRO** 🎯")
    if st.button("< Voltar para o Teste"): 
        st.session_state.page = 'test'
        
    st.title("Suas Recomendações de Carreira")
    st.subheader("Escolhas alinhadas ao seu perfil!")
    
    st.divider()

    # Gerar os cards com base nas recomendações do especialista
    # Nós usamos o loop para criar o grid de 2x2 cards de design
    for i in range(0, len(st.session_state.recommended_careers), 2):
        # Cria uma linha de 2 colunas
        card_col1, card_col2 = st.columns(2)
        
        # Primeiro Card da linha
        if i < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i]
            # Usamos st.container() para aplicar a borda vinho do design
            with card_col1.container():
                # Layout interno do card (1 parte para imagem, 2 para texto)
                with st.container(): # Novo container interno para alinhar
                    inner_col1, inner_col2 = st.columns([1, 2])
                    with inner_col1:
                        st.image(career['image'], width=100)
                    with inner_col2:
                        st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                        st.button(f"Saiba Mais", key=f"know_more_{i}")

        # Segundo Card da linha (se houver)
        if i+1 < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i+1]
            with card_col2.container():
                with st.container():
                    inner_col1, inner_col2 = st.columns([1, 2])
                    with inner_col1:
                        st.image(career['image'], width=100)
                    with inner_col2:
                        st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                        st.button(f"Saiba Mais", key=f"know_more_{i+1}")

# --- FLUXO PRINCIPAL DO APP ---
if st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()

# Seção escondida (Modo Administrador) para o professor ver que o banco funciona
st.divider()
if st.checkbox("⚙️ Modo Administrador: Ver Banco de Dados (CSV)"):
    df = carregar_dados()
    st.dataframe(df)