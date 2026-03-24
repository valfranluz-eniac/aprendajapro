import streamlit as st
import pandas as pd
import os

# --- ARQUIVO DE BANCO DE DADOS (CSV) ---
CSV_FILE = "cadastros_recomendacoes.csv"

def carregar_dados():
    # Verifica se o arquivo existe
    if os.path.exists(CSV_FILE):
        try:
            # TENTA ler o arquivo. Se ele estiver perfeito, ótimo!
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        except:
            # SE DER ERRO (arquivo corrompido, vazio, zumbi), ele ignora e cria um novo!
            return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])
    else:
        # Se não existe, cria um DataFrame vazio com as colunas necessárias
        return pd.DataFrame(columns=["Nome", "Interesses", "Escolaridade", "Carreira Recomendada"])

def salvar_recomendacao(nome, interesses, escolaridade, recomendacao):
    df = carregar_dados()
    # Cria uma nova linha de dados
    new_entry = pd.DataFrame([{
        "Nome": nome, 
        "Interesses": ", ".join(interesses), # Transforma a lista de interesses em texto
        "Escolaridade": escolaridade, 
        "Carreira Recomendada": recomendacao
    }])
    # Concatena a nova linha ao DataFrame existente
    df_final = pd.concat([df, new_entry], ignore_index=True)
    df_final.to_csv(CSV_FILE, index=False)

# --- BASE DE DADOS DE CARREIRAS "REAIS" (O Conhecimento Especialista) ---
# Criamos um catálogo com as carreiras, descrições e links de imagens genéricas da internet.
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Desenvolvedor de Software', 'description': 'Crie aplicativos e sistemas de alta tecnologia.', 'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}},
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Analista de Dados Júnior', 'description': 'Comece na área de dados transformando números em decisões.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior'], 'career': {'title': 'Gerente de Produto (PM)', 'description': 'Lance e gerencie seu próprio produto ou negócio.', 'image': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}},
    {'interests': ['Artes & Design'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'UX/UI Designer Sênior', 'description': 'Projete interfaces digitais intuitivas e inovadoras.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}},
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Enfermeiro de UTI', 'description': 'Atue em uma área médica crítica e de alta demanda.', 'image': 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}},
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Médico Especialista', 'description': 'Torne-se referência em sua área médica.', 'image': 'https://images.unsplash.com/photo-1584447128309-b66b7a14890c?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}}
]

# Função que gera a recomendação com base nas regras do especialista
def get_career_recommendation(selected_interests, selected_education):
    # Se o usuário não selecionar nada, damos um padrão
    if not selected_interests or not selected_education:
        return [{'title': 'Orientador de Carreiras Geral', 'description': 'Poxa, você não escolheu nada!', 'image': 'https://images.unsplash.com/photo-1593062096033-9a26b09dd705?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}]
        
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
        return [{'title': 'Empreendedor Geral', 'description': 'Um perfil versátil! Vamos conversar mais sobre sua trilha.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}]

# --- CONFIGURAÇÃO DA PÁGINA (Estado da Sessão) ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing' # Página inicial padrão
if 'recommended_careers' not in st.session_state:
    st.session_state.recommended_careers = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.set_page_config(page_title="AprendaJá PRO - Seu Caminho", page_icon="🎯", layout="centered")

# --- FUNÇÕES DE PÁGINA (Réplicas do Design) ---

# Título do design (brevemente simulado)
st.markdown("## AprendaJá **PRO** 🎯")

def show_landing_page():
    # Ilustração do design (placeholder de imagem)
    st.image("https://streamlit-career-images.s3.amazonaws.com/landing_page_illustration.png")
    st.title("Seu Caminho para o Sucesso Profissional")
    
    # Botão principal
    if st.button("Comece Agora"):
        st.session_state.page = 'test' # Navega para a página do teste

def show_profile_test_page():
    # Navegação e Título
    st.header("< Teste de Perfil Profissional")
    if st.button("Voltar", key="voltar_landing"): 
        st.session_state.page = 'landing'
    
    st.subheader("Nos ajude a conhecer você melhor.")
    
    # Cadastro de nome (para salvar no CSV)
    name = st.text_input("Qual seu nome?")
    
    st.write("Quais são seus principais interesses?")
    # Checkboxes do design
    interest_options = ["Tecnologia", "Negócios", "Saúde", "Artes & Design"]
    # Usamos o st.multiselect que é mais amigável para Streamlit
    selected_interests = st.multiselect("Selecione seus interesses:", interest_options)
    
    st.write("Qual seu nível de escolaridade?")
    # Radio buttons do design
    education_options = ["Ensino Médio", "Ensino Superior", "Pós-Graduação"]
    selected_education = st.radio("Escolha uma opção:", education_options)
    
    # Botão principal para continuar
    if st.button("Continuar"):
        # Armazena o nome, gera a recomendação e navega para os resultados
        st.session_state.user_name = name
        st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
        # Salva o cadastro no banco de dados CSV
        salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
        st.session_state.page = 'results'

def show_results_page():
    # Navegação e Título
    st.header("< Voltar")
    if st.button("Voltar", key="voltar_teste"): 
        st.session_state.page = 'test'
        
    st.title("Suas Recomendações de Carreira")
    st.subheader("Escolhas alinhadas ao seu perfil!")
    
    st.divider()

    # Gerar os cards com base nas recomendações do especialista
    for career in st.session_state.recommended_careers:
        # Layout do card em colunas (1 parte para imagem, 2 para texto)
        card_col1, card_col2 = st.columns([1, 2])
        with card_col1:
            st.image(career['image'], width=150)
        with card_col2:
            st.write(f"### {career['title']}")
            st.write(career['description'])
            # Botão genérico do design
            if st.button(f"Saiba Mais - {career['title']}", key=f"know_more_{career['title']}"):
                st.info("Poxa! O link 'Saiba Mais' ainda não está funcional neste protótipo.")
        st.divider()

# --- FLUXO PRINCIPAL DO APP ---
# O 'if' controla qual função de página será exibida na tela
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()

# Seção escondida (Modo Administrador) para o professor ver que o banco funciona
st.divider()
if st.checkbox("⚙️ Modo Administrador: Ver Banco de Dados (CSV)"):
    df = carregar_dados()
    st.dataframe(df)
