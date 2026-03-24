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
    st.session_state.page = 'test' 
if 'recommended_careers' not in st.session_state:
    st.session_state.recommended_careers = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.set_page_config(page_title="AprendaJá PRO - Seu Caminho", page_icon="🎯", layout="centered")

# --- INJEÇÃO DE CSS PERSONALIZADO (Cores do Logo e Design Responsivo) ---
st.markdown("""
<style>
    /* Estilo para os Cards de Resultado - Borda Laranja do Logo */
    .stContainer {
        border: 2px solid #D35400;
        border-radius: 15px;
        padding: 20px;
        background-color: #2D2D31;
        margin-bottom: 20px;
    }
    
    /* Estilo para Títulos dentro dos Cards */
    .career-title {
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: bold !important;
        margin-bottom: 5px !important;
    }
    
    /* Estilo para Descrições */
    .career-description {
        color: #DEDEDE !important;
        font-size: 15px;
        margin-bottom: 10px;
        line-height: 1.4;
    }

    /* Estilo para a justificativa do perfil - Laranja claro */
    .career-reason {
        color: #D98880 !important;
        font-size: 14px;
        font-style: italic;
        margin-top: 5px;
    }

    /* Estilo para os botões de Navegação (Laranja do Logo) */
    .stButton > button {
        background-color: #D35400;
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%; /* Faz o botão ocupar a largura toda no celular */
    }
    .stButton > button:hover {
        background-color: #A04000;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DE CARREIRAS (Com justificativas dinâmicas e detalhadas) ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior', 'Pós-Graduação'], 'career': {'title': 'Programador de Softwares', 'description': 'Crie aplicativos e sistemas de alta tecnologia.', 'reason': 'Com seu interesse em tecnologia e formação acadêmica avançada, você possui a base ideal para criar lógicas complexas e inovar no mercado digital.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400&auto=format&fit=crop'}},
    
    {'interests': ['Tecnologia'], 'education': ['Ensino Médio'], 'career': {'title': 'Analista de Dados Júnior', 'description': 'Comece na área de dados transformando números em decisões.', 'reason': 'Você tem afinidade com tecnologia e está no momento perfeito para iniciar uma trilha técnica muito requisitada pelas empresas.', 'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400&auto=format&fit=crop'}},
    
    {'interests': ['Negócios'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Gestor de Projetos', 'description': 'Lidere equipes e gerencie negócios de sucesso.', 'reason': 'Seu foco em negócios demonstra um perfil de liderança e visão estratégica, essencial para gerenciar processos e pessoas.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400&auto=format&fit=crop'}},
    
    {'interests': ['Artes & Design'], 'education': ['Ensino Superior', 'Pós-Graduação', 'Ensino Médio'], 'career': {'title': 'Designer Criativo', 'description': 'Projete interfaces e experiências visuais inovadoras.', 'reason': 'Sua escolha por artes indica alta criatividade e empatia visual, habilidades chave para se destacar no mercado criativo.', 'image': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=400&auto=format&fit=crop'}},
    
    {'interests': ['Saúde'], 'education': ['Ensino Superior'], 'career': {'title': 'Especialista em Saúde', 'description': 'Atue no cuidado e bem-estar em áreas clínicas.', 'reason': 'O interesse em saúde e sua formação superior refletem sua dedicação técnica e vocação para o cuidado humano.', 'image': 'https://images.unsplash.com/photo-1581056771107-24ca5f033842s?q=80&w=400&auto=format&fit=crop'}},
    
    {'interests': ['Saúde'], 'education': ['Pós-Graduação'], 'career': {'title': 'Pesquisador em Saúde', 'description': 'Desenvolva soluções avançadas para a área médica.', 'reason': 'Sua pós-graduação aliada à saúde te coloca em uma posição de destaque para pesquisas e inovações científicas.', 'image': 'https://images.unsplash.com/photo-1584447128309-b66b7a14890c?q=80&w=400&auto=format&fit=crop'}}
]

def get_career_recommendation(selected_interests, selected_education):
    # Lógica de recomendação com base nas regras do especialista. Devolve todas as carreiras correspondentes.
    possible_careers = []
    for option in career_database:
        if any(interest in option['interests'] for interest in selected_interests) and selected_education in option['education']:
            possible_careers.append(option['career'])
    
    if possible_careers:
        return possible_careers 
    else:
        # Perfil de Empreendedor/Inovador como padrão para perfis versáteis
        return [{'title': 'Empreendedor Inovador', 'description': 'Crie seu próprio caminho unindo diferentes áreas do conhecimento.', 'reason': 'Seu perfil é versátil e não se prende a padrões! Essa combinação única te dá a base para empreender e inovar.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400&auto=format&fit=crop'}]

# --- FUNÇÕES DE PÁGINA ---

def show_profile_test_page():
    # Cabeçalho com o logo e título (Design Réplica)
    st.markdown("## AprendaJá **PRO** 🎯")
    st.divider()
    st.markdown("### Nos ajude a conhecer você melhor.")
    
    # Campo de Nome com validação
    name = st.text_input("Qual seu nome?")
    
    st.write("Quais são seus principais interesses?")
    
    # Grid responsivo 2x2 para celular com ícones embutidos (Design Otimizado)
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
    
    st.write("") # Espaço em branco para respirar o layout
    
    # Botão de Validação e Sálvamento (Laranja do Logo)
    if st.button("Continuar"):
        if not name.strip():
            st.warning("⚠️ Por favor, digite seu nome antes de continuar.")
        elif len(selected_interests) == 0:
            st.warning("⚠️ Por favor, escolha pelo menos um interesse (Tecnologia, Negócios, Saúde ou Artes).")
        else:
            # Se passou na validação, sálva os dados e gera a recomendação
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(selected_interests, selected_education)
            
            # Salva o cadastro no banco de dados CSV
            if st.session_state.recommended_careers:
                 salvar_recomendacao(name, selected_interests, selected_education, st.session_state.recommended_careers[0]['title'])
                 
            # Navega para a tela de resultados
            st.session_state.page = 'results'
            st.rerun() # Força a tela a atualizar imediatamente

def show_results_page():
    # Cabeçalho com o logo
    st.markdown("## AprendaJá **PRO** 🎯")
    
    st.title("Suas Recomendações")
    # Subheader dinâmico com o nome do usuário
    st.subheader(f"Escolhas alinhadas ao seu perfil, {st.session_state.user_name}!")
    
    st.divider()

    # Loop para gerar os cards de resultado em um grid de 2 colunas
    for i in range(0, len(st.session_state.recommended_careers), 2):
        card_col1, card_col2 = st.columns(2)
        
        # Exibe o primeiro card na linha (Design Réplica com borda laranja)
        if i < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i]
            with card_col1.container():
                # O layout responsivo embutido no container funciona perfeito no celular
                st.image(career['image'], use_column_width=True)
                st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='career-reason'>💡 <b>Por que combina?</b><br>{career['reason']}</p>", unsafe_allow_html=True)

        # Exibe o segundo card na linha (se houver)
        if i+1 < len(st.session_state.recommended_careers):
            career = st.session_state.recommended_careers[i+1]
            with card_col2.container():
                st.image(career['image'], use_column_width=True)
                st.markdown(f"<p class='career-title'>{career['title']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='career-description'>{career['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='career-reason'>💡 <b>Por que combina?</b><br>{career['reason']}</p>", unsafe_allow_html=True)

    # Após exibir todas as recomendações, adiciona um divisor e o botão no final
    st.divider()
    # Botão "Voltar ao Teste" no final (Design Réplica)
    if st.button("Voltar para o Teste"): 
        st.session_state.page = 'test'
        st.rerun()

# --- FLUXO PRINCIPAL DO APP ---
# O 'if' controla qual função de página será exibida na tela
if st.session_state.page == 'test':
    show_profile_test_page()
elif st.session_state.page == 'results':
    show_results_page()

# Seção escondida (Modo Administrador) para o professor ver que o banco de dados CSV funciona
st.divider()
if st.checkbox("⚙️ Modo Administrador: Ver Banco de Dados (CSV)"):
    df = carregar_dados()
    st.dataframe(df)