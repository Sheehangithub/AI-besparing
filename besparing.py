import streamlit as st
import pandas as pd

# Must be the very first Streamlit call
st.set_page_config(
    page_title="AI Tijdswinst Quickscan",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATAMODEL ---
PRODUCTIVITY_DATA = {
    'writing_general':       {'label': 'Contentcreatie (e-mails, blogs, rapporten)',           'category': 'Marketing & Verkoop',       'savings_pct': 0.68},
    'visual_design':         {'label': 'Visueel Ontwerp (afbeeldingen, presentaties)',         'category': 'Marketing & Verkoop',       'savings_pct': 0.70},
    'data_analysis_marketing': {'label': 'Data-analyse & SEO (campagnedata, zoekwoorden)',     'category': 'Marketing & Verkoop',       'savings_pct': 0.40},
    'programming_general':   {'label': 'Coderen & Programmeren (schrijven, debuggen, testen)', 'category': 'Softwareontwikkeling & IT', 'savings_pct': 0.99},
    'troubleshooting_it':    {'label': 'IT-operaties & Probleemoplossing',                    'category': 'Softwareontwikkeling & IT', 'savings_pct': 0.76},
    'customer_service':      {'label': 'Klantenservice (e-mails, vragen beantwoorden)',         'category': 'Klantoperaties',             'savings_pct': 0.14},
    'admin_general':         {'label': 'Algemene Administratie (plannen, data-invoer, samenvatten)', 'category': 'Administratie & HR','savings_pct': 0.62},
    'hr_recruitment':        {'label': 'Werving & Selectie (HR)',                             'category': 'Administratie & HR',        'savings_pct': 0.69},
    'finance_reporting':     {'label': 'Financiële Analyse & Rapportage',                      'category': 'Financiën & Boekhouding',    'savings_pct': 0.40},
}

# --- STATE MANAGEMENT & CALLBACKS ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}

def set_stage(stage_number):
    st.session_state.stage = stage_number

# --- UI FUNCTIONS ---
def display_welcome_page():
    st.title("⏱️ AI Tijdswinst Quickscan")
    st.markdown("#### Ontdek hoeveel tijd en kosten uw bedrijf kan besparen door de inzet van AI.")
    st.markdown("""
    Deze tool helpt u in **minder dan 5 minuten** een realistische schatting te maken van de potentiële productiviteitswinst. 
    """)
    st.button(
        "Start de Quickscan",
        on_click=set_stage, args=[1],
        key="btn_start_quickscan",
        type="primary"
    )

def display_task_input_page():
    st.header("Stap 1: Wekelijkse Tijdsbesteding")
    st.markdown("Voer in hoeveel uur uw team *gemiddeld per week* besteedt aan de volgende taken.")

    # Group tasks by category
    categories = {}
    for task_id, info in PRODUCTIVITY_DATA.items():
        categories.setdefault(info['category'], []).append((task_id, info['label']))

    for category, tasks in categories.items():
        with st.expander(f"**{category}**", expanded=True):
            for task_id, label in tasks:
                st.number_input(
                    label,
                    min_value=0, step=1,
                    key=f"hours_{task_id}",  # unique key per input
                    help=f"Uren/week aan: {label}"
                )

    c1, c2 = st.columns(2)
    with c1:
        st.button(
            "Terug naar Welkomstpagina",
            on_click=set_stage, args=[0],
            key="btn_back_to_welcome"
        )
    with c2:
        st.button(
            "Volgende Stap: Kosten & Investering",
            on_click=set_stage, args=[2],
            key="btn_next_to_cost",
            type="primary"
        )

def display_cost_input_page():
    st.header("Stap 2: Financiële Context (Optioneel)")
    st.markdown("Voer een gemiddeld uurtarief in om de financiële impact te berekenen.")

    st.number_input(
        "Gemiddelde uurkost (€)",
        min_value=0, step=5,
        key='hourly_rate',
        help="Gemiddeld uurtarief per medewerker"
    )
    st.selectbox(
        "Herinvestering van bespaarde tijd",
        ("Innovatie", "Klantrelaties", "Strategische planning", "Training"),
        key='reinvestment_goal'
    )

    c1, c2 = st.columns(2)
    with c1:
        st.button(
            "Terug naar Taken",
            on_click=set_stage, args=[1],
            key="btn_back_to_tasks"
        )
    with c2:
        st.button(
            "Bekijk Resultaten",
            on_click=set_stage, args=[3],
            key="btn_view_results",
            type="primary"
        )

def display_results_page():
    st.header("📊 Gepersonaliseerde Resultaten")

    results = []
    total_saved = 0
    for task_id, info in PRODUCTIVITY_DATA.items():
        hrs = st.session_state.get(f"hours_{task_id}", 0)
        if hrs > 0:
            saved = hrs * info['savings_pct']
            results.append({
                'Taak': info['label'],
                'Categorie': info['category'],
                'Ingevoerde Uren': hrs,
                'Bespaarde Uren': saved,
                'Uren na AI': hrs - saved
            })
            total_saved += saved

    if not results:
        st.warning("Geen uren ingevoerd.")
        st.button(
            "Terug naar Taken",
            on_click=set_stage, args=[1],
            key="btn_warning_back"
        )
        return

    rate = st.session_state.get('hourly_rate', 0)
    yearly_value = total_saved * rate * 52
    regained = total_saved / 40

    c1, c2, c3 = st.columns(3)
    c1.metric("Bespaarde Uren/week", f"{total_saved:.1f} uur")
    c2.metric(
        "Jaarlijkse Waarde",
        f"€ {yearly_value:,.0f}" if rate else "Uurtarief ontbreekt"
    )
    c3.metric("Teruggewonnen FTE", f"{regained:.2f}")

    df = pd.DataFrame(results)
    st.bar_chart(df.set_index('Taak')[['Uren na AI', 'Bespaarde Uren']])

    st.markdown(f"**Herinvestering:** {st.session_state.get('reinvestment_goal', '-')}")
    with st.expander("Details & Methodologie"):
        st.dataframe(df)
        st.markdown("Gebaseerd op McKinsey (2023), Stanford (2024), Wereldbank.")

    st.button(
        "Opnieuw beginnen",
        on_click=set_stage, args=[0],
        key="btn_restart"
    )

# --- ROUTER ---
stage = st.session_state.stage
if stage == 0:
    display_welcome_page()
elif stage == 1:
    display_task_input_page()
elif stage == 2:
    display_cost_input_page()
else:
    display_results_page()
