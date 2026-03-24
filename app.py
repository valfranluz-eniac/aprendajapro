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
    .stApp { background-color: #F4F9FD; }
    
    .logo-container { text-align: center; padding-top: 10px; margin-bottom: 20px; }
    .logo-text { font-size: 32px; font-weight: 800; color: #3A7CA5; }
    .logo-badge {
        background: linear-gradient(90deg, #F39C12, #D35400); 
        color: white; padding: 4px 10px; border-radius: 8px;
        font-size: 18px; font-weight: bold; vertical-align: super; margin-left: 5px;
    }

    .hero-title { text-align: center; color: #3A7CA5; font-size: 22px; margin-bottom: 20px; }
    
    .test-header-title { 
        color: #1A5276; font-size: 28px; font-style: italic; font-weight: bold; 
        text-align: center; margin-top: -15px; margin-bottom: 15px; 
    }

    /* CENTRALIZAÇÃO DOS BOTÕES - CORREÇÃO CRÍTICA */
    div.stButton {
        text-align: center;
        display: flex;
        justify-content: center;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #F39C12, #D35400) !important;
        color: white !important;
        border: none !important;
        border-radius: 35px !important;
        padding: 12px 60px !important; 
        font-size: 20px !important; 
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.4) !important;
        transition: transform 0.2s !important;
        width: auto !important;
        margin: 10px auto !important;
    }

    div.stButton > button:hover { transform: scale(1.05) !important; }

    .test-banner { 
        background: linear-gradient(180deg, #D6EAF8, #EBF5FB); 
        color: #1A5276; text-align: center; padding: 15px; 
        border-radius: 12px; margin-bottom: 25px; 
    }

    .question-title { 
        color: #1A5276; font-size: 16px; font-weight: bold; 
        border-bottom: 1px solid #D4E6F1; padding-bottom: 5px; 
        margin-top: 20px; margin-bottom: 15px;
    }

    .flex-features-container { display: flex; justify-content: space-around; margin-top: 30px; padding-bottom: 30px; }
    .flex-feature-item { display: flex; flex-direction: column; align-items: center; }
    .feature-icon-circle-small {
        width: 55px; height: 55px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 8px;
    }
    .bg-blue-small { background-color: #5DADE2; color: white; }
    .bg-yellow-small { background-color: #F4D03F; color: white; }
    .bg-red-small { background-color: #E74C3C; color: white; }

    .rec-card { 
        background: white; border-radius: 15px; padding: 15px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06); margin-bottom: 20px; 
        display: flex; align-items: center;
    }
    .rec-card-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; margin-right: 15px; }
    .rec-card-title { color: #1A5276; font-size: 17px; font-weight: 800; }
    
    .footer-nav-container { 
        display: flex; justify-content: space-between; margin-top: 30px; 
        border-top: 2px solid #EBF5FB; padding: 20px 0; 
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
</style>
""", unsafe_allow_html=True)

# --- LOGICA ---
career_database = [
    {'interests': ['Tecnologia'], 'education': ['Ensino Superior'], 'career': {'title': 'Dev FullStack', 'description': 'Web & Mobile', 'reason': 'Alta demanda.', 'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400'}},
    {'interests': ['Negócios'], 'education': ['Ensino Superior'], 'career': {'title': 'Gestor Ágil', 'description': 'Projetos modernos', 'reason': 'Perfil líder.', 'image': 'https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?q=80&w=400'}}
]

def get_career_recommendation(interests, education):
    m = [c['career'] for c in career_database if any(i in c['interests'] for i in interests)]
    return m if m else [{'title': 'Consultor', 'description': 'Novos Negócios', 'reason': 'Perfil inovador.', 'image': 'https://images.unsplash.com/photo-1542744094-3a31f2f31d4d?q=80&w=400'}]

# --- TELAS ---
def show_landing_page():
    st.markdown('<div class="logo-container"><span class="logo-text">AprendaJá</span><span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'><b>Seu Caminho</b> para o Sucesso</h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><img src="https://img.freepik.com/free-vector/team-work-concept-landing-page_52683-20165.jpg?w=800" width="380" style="border-radius:20px;"></div>', unsafe_allow_html=True)
    
    if st.button("Comece Agora"):
        st.session_state.page = 'test'
        st.rerun()
        
    st.markdown("""
        <div class="flex-features-container">
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-blue-small">👤</div><div style="font-size:11px;">Teste</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-yellow-small">📋</div><div style="font-size:11px;">Trilhas</div></div>
            <div class="flex-feature-item"><div class="feature-icon-circle-small bg-red-small">🎓</div><div style="font-size:11px;">Dicas</div></div>
        </div>
    """, unsafe_allow_html=True)

def show_profile_test_page():
    st.markdown("<div class='test-header-title'>Teste de Perfil Profissional</div>", unsafe_allow_html=True)
    st.markdown("<div class='test-banner'>Nos ajude a conhecer você melhor.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='question-title'>Qual o seu nome?</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Nome...", label_visibility="collapsed")
    
    st.markdown("<div class='question-title'>Interesses:</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        t = st.checkbox("Tecnologia")
        s = st.checkbox("Saúde")
    with c2:
        n = st.checkbox("Negócios")
        a = st.checkbox("Artes")
    
    st.markdown("<div class='question-title'>Escolaridade:</div>", unsafe_allow_html=True)
    edu = st.radio("", ["Ensino Médio", "Ensino Superior", "Pós-Graduação"], label_visibility="collapsed")
    
    sel = [i for i, v in zip(["Tecnologia", "Negócios", "Saúde", "Artes"], [t, n, s, a]) if v]

    if st.button("Continuar"):
        if name and sel:
            st.session_state.user_name = name
            st.session_state.recommended_careers = get_career_recommendation(sel, edu)
            salvar_recomendacao(name, sel, edu, st.session_state.recommended_careers[0]['title'])
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.warning("Preencha tudo!")

def show_results_page():
    st.markdown(f"<div class='test-header-title'>Resultados para {st.session_state.user_name}</div>", unsafe_allow_html=True)
    for career in st.session_state.recommended_careers:
        st.markdown(f"""
        <div class="rec-card">
            <img src="{career['image']}" class="rec-card-img">
            <div><div class="rec-card-title">{career['title']}</div><div>{career['description']}</div></div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Refazer"):
        st.session_state.page = 'test'
        st.rerun()

if st.session_state.page == 'landing': show_landing_page()
elif st.session_state.page == 'test': show_profile_test_page()
elif st.session_state.page == 'results': show_results_page()

st.divider()
if st.checkbox("⚙️ Admin"): st.dataframe(carregar_dados())