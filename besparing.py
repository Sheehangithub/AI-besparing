import streamlit as st
import pandas as pd

# --- PAGINA CONFIGURATIE ---
# Stelt de basisconfiguratie voor de pagina in, zoals de titel en een brede layout.
st.set_page_config(
    page_title="AI Tijdswinst Quickscan",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATAMODEL ---
# Dit is het hart van de calculator, gebaseerd op Tabel 2 en Appendix A uit de blauwdruk.
# Het bevat de taken, de categorieën en de genormaliseerde besparingspercentages.
# Structuur: { 'taak_id': {'label': 'Taak Omschrijving', 'category': 'Hoofdcategorie', 'savings_pct': 0.XX} }
PRODUCTIVITY_DATA = {
    'writing_general': {'label': 'Contentcreatie (e-mails, blogs, rapporten)', 'category': 'Marketing & Verkoop',
                        'savings_pct': 0.68},
    'visual_design': {'label': 'Visueel Ontwerp (afbeeldingen, presentaties)', 'category': 'Marketing & Verkoop',
                      'savings_pct': 0.70},
    'data_analysis_marketing': {'label': 'Data-analyse & SEO (campagnedata, zoekwoorden)',
                                'category': 'Marketing & Verkoop', 'savings_pct': 0.40},
    'programming_general': {'label': 'Coderen & Programmeren (schrijven, debuggen, testen)',
                            'category': 'Softwareontwikkeling & IT', 'savings_pct': 0.99},
    'troubleshooting_it': {'label': 'IT-operaties & Probleemoplossing', 'category': 'Softwareontwikkeling & IT',
                           'savings_pct': 0.76},
    'customer_service': {'label': 'Klantenservice (e-mails, vragen beantwoorden)', 'category': 'Klantoperaties',
                         'savings_pct': 0.14},
    'admin_general': {'label': 'Algemene Administratie (plannen, data-invoer, samenvatten)',
                      'category': 'Administratie & HR', 'savings_pct': 0.62},
    'hr_recruitment': {'label': 'Werving & Selectie (HR)', 'category': 'Administratie & HR', 'savings_pct': 0.69},
    'finance_reporting': {'label': 'Financiële Analyse & Rapportage', 'category': 'Financiën & Boekhouding',
                          'savings_pct': 0.40},
}

# --- STATE MANAGEMENT & CALLBACKS ---
# Initialiseert de 'session_state' van Streamlit. Dit is cruciaal om de
# data van de gebruiker te onthouden terwijl ze door de verschillende stappen van de wizard navigeren.
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}


def set_stage(stage_number):
    """Callback functie om de huidige stap van de wizard te wijzigen."""
    st.session_state.stage = stage_number


def store_input(key, value):
    """Callback om een specifieke gebruikersinvoer op te slaan."""
    st.session_state.user_inputs[key] = value


# --- UI FUNCTIES ---
# Deze functies tekenen de verschillende "pagina's" of stappen van de wizard.

def display_welcome_page():
    """Toont de welkomstpagina en de 'Start' knop."""
    st.title("⏱️ AI Tijdswinst Quickscan")
    st.markdown("#### Ontdek hoeveel tijd en kosten uw bedrijf kan besparen door de inzet van AI.")
    st.markdown("""
    Deze tool helpt u in **minder dan 5 minuten** een realistische schatting te maken van de potentiële productiviteitswinst. 
    De berekeningen zijn gebaseerd op een synthese van recent onderzoek van o.a. **McKinsey, Stanford University en de Wereldbank**.

    **Hoe het werkt:**
    1.  **Selecteer taken** die relevant zijn voor uw bedrijf.
    2.  **Voer het aantal uren** in dat uw team wekelijks aan deze taken besteedt.
    3.  **Ontvang direct een gepersonaliseerd dashboard** met uw potentiële tijd- en kostenbesparing.
    """)
    st.button("Start de Quickscan", on_click=set_stage, args=[1], type="primary")


def display_task_input_page():
    """Toont de invoervelden voor de taken en uren."""
    st.header("Stap 1: Wekelijkse Tijdsbesteding")
    st.markdown(
        "Voer in hoeveel uur uw team *gemiddeld per week* besteedt aan de volgende taken. Laat velden op 0 staan als ze niet van toepassing zijn.")

    # Maak een dictionary om de categorieën te groeperen
    categories = {}
    for task_id, task_info in PRODUCTIVITY_DATA.items():
        if task_info['category'] not in categories:
            categories[task_info['category']] = []
        categories[task_info['category']].append((task_id, task_info['label']))

    # Toon de invoervelden per categorie in uitklapbare secties
    for category, tasks in categories.items():
        with st.expander(f"**{category}**", expanded=True):
            for task_id, label in tasks:
                st.number_input(
                    label,
                    min_value=0,
                    step=1,
                    key=f"hours_{task_id}",  # Sla de waarde direct op in session_state
                    help=f"Gemiddeld aantal uren per week besteed aan: {label}"
                )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Terug naar Welkomstpagina", on_click=set_stage, args=[0])
    with col2:
        st.button("Volgende Stap: Kosten & Investering", on_click=set_stage, args=[2], type="primary")


def display_cost_input_page():
    """Toont de (optionele) invoervelden voor kosten en herinvestering."""
    st.header("Stap 2: Financiële Context (Optioneel)")
    st.markdown(
        "Om de financiële impact te berekenen, kunt u een gemiddeld uurtarief invoeren. Deze data wordt **niet** opgeslagen.")

    st.number_input(
        "Gemiddelde uurkost van een medewerker (€)",
        min_value=0,
        step=5,
        key='hourly_rate',
        help="Dit is een gemiddelde om de waarde van de bespaarde tijd te kunnen berekenen."
    )

    st.selectbox(
        "Waarin zou u de bespaarde tijd idealiter herinvesteren?",
        ("Innovatie & productontwikkeling", "Klantrelaties versterken", "Strategische planning",
         "Training & ontwikkeling van medewerkers"),
        key='reinvestment_goal',
        help="Dit helpt om de resultaten in een strategisch kader te plaatsen."
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Terug naar Taken", on_click=set_stage, args=[1])
    with col2:
        st.button("Bekijk Resultaten", on_click=set_stage, args=[3], type="primary")


def display_results_page():
    """Berekent en toont het uiteindelijke resultatendashboard."""
    st.header("📊 Uw Gepersonaliseerde Resultaten")

    # --- BEREKENINGEN ---
    results = []
    total_hours_input = 0
    total_hours_saved = 0

    for task_id, task_info in PRODUCTIVITY_DATA.items():
        hours_input = st.session_state.get(f"hours_{task_id}", 0)
        if hours_input > 0:
            saved_hours = hours_input * task_info['savings_pct']
            results.append({
                'Taak': task_info['label'],
                'Categorie': task_info['category'],
                'Ingevoerde Uren': hours_input,
                'Bespaarde Uren': saved_hours,
                'Uren na AI': hours_input - saved_hours
            })
            total_hours_input += hours_input
            total_hours_saved += saved_hours

    if not results:
        st.warning("U heeft geen uren ingevoerd. Ga terug naar de vorige stap om uw data in te vullen.")
        st.button("Terug naar Taken", on_click=set_stage, args=[1])
        return

    hourly_rate = st.session_state.get('hourly_rate', 0)
    total_cost_saving_yearly = total_hours_saved * hourly_rate * 52
    regained_fte = total_hours_saved / 40

    # --- VISUALISATIE ---
    st.markdown("### Samenvatting van uw Potentieel")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Totaal Bespaarde Uren per Week",
        value=f"{total_hours_saved:.1f} uur",
        help="Het totale aantal uren dat wekelijks kan worden bespaard."
    )
    col2.metric(
        label="Jaarlijkse Financiële Waarde",
        value=f"€ {total_cost_saving_yearly:,.0f}",
        help="De geschatte jaarlijkse besparing, gebaseerd op het door u ingevoerde uurtarief." if hourly_rate > 0 else "Voer een uurtarief in bij de vorige stap voor deze berekening."
    )
    col3.metric(
        label="Teruggewonnen FTE",
        value=f"{regained_fte:.2f}",
        help="Het aantal full-time medewerkers aan productiviteit dat u terugwint."
    )

    st.markdown("---")

    # Dataframe voor de grafiek
    df_results = pd.DataFrame(results)

    st.markdown("### Besparingspotentieel per Taak")

    # Maak een nieuwe dataframe voor de staafdiagram
    df_chart = df_results[['Taak', 'Uren na AI', 'Bespaarde Uren']].copy()
    df_chart.set_index('Taak', inplace=True)

    st.bar_chart(
        df_chart,
        color=["#1f77b4", "#ff7f0e"]  # Kleuren voor 'Uren na AI' en 'Bespaarde Uren'
    )
    st.caption(
        "De grafiek toont de huidige uren (totale hoogte van de staaf), opgesplitst in de uren die overblijven na AI-implementatie en de uren die worden bespaard.")

    st.markdown("---")

    # Strategische aanbeveling
    reinvestment_goal = st.session_state.get('reinvestment_goal', 'uw doelen')
    st.markdown(f"""
    ### Van Tijdswinst naar Bedrijfsgroei
    De **{total_hours_saved:.1f} uur** die u wekelijks bespaart, is meer dan een kostenreductie; het is vrijgemaakt kapitaal. 
    Deze tijd kan direct worden geherinvesteerd in uw focusgebied: **{reinvestment_goal}**. 

    Dit creëert een groeicyclus: AI-efficiëntie financiert innovatie en strategische initiatieven, wat leidt tot groei die verdere investeringen mogelijk maakt.
    """)

    with st.expander("Gedetailleerd overzicht en bronvermelding"):
        st.dataframe(df_results.style.format({
            'Ingevoerde Uren': '{:.0f}',
            'Bespaarde Uren': '{:.1f}',
            'Uren na AI': '{:.1f}'
        }))
        st.markdown("""
        **Methodologie:** De besparingspercentages zijn genormaliseerde gemiddelden, gebaseerd op een analyse van onderzoeken van o.a. McKinsey (The economic potential of generative AI, 2023), Stanford University (Experimental evidence on the productivity effects of generative artificial intelligence, 2024), en de Wereldbank. De tool is bedoeld als een realistische schatting om een strategische discussie te starten.
        """)

    st.button("Opnieuw Beginnen", on_click=set_stage, args=[0])


# --- HOOFD ROUTER ---
# Deze logica bepaalt welke pagina wordt weergegeven op basis van de 'stage' in de session_state.
if st.session_state.stage == 0:
    display_welcome_page()
elif st.session_state.stage == 1:
    display_task_input_page()
elif st.session_state.stage == 2:
    display_cost_input_page()
elif st.session_state.stage == 3:
    display_results_page()
import streamlit as st
import pandas as pd

# --- PAGINA CONFIGURATIE ---
# Stelt de basisconfiguratie voor de pagina in, zoals de titel en een brede layout.
st.set_page_config(
    page_title="AI Tijdswinst Quickscan",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATAMODEL ---
# Dit is het hart van de calculator, gebaseerd op Tabel 2 en Appendix A uit de blauwdruk.
# Het bevat de taken, de categorieën en de genormaliseerde besparingspercentages.
# Structuur: { 'taak_id': {'label': 'Taak Omschrijving', 'category': 'Hoofdcategorie', 'savings_pct': 0.XX} }
PRODUCTIVITY_DATA = {
    'writing_general': {'label': 'Contentcreatie (e-mails, blogs, rapporten)', 'category': 'Marketing & Verkoop',
                        'savings_pct': 0.68},
    'visual_design': {'label': 'Visueel Ontwerp (afbeeldingen, presentaties)', 'category': 'Marketing & Verkoop',
                      'savings_pct': 0.70},
    'data_analysis_marketing': {'label': 'Data-analyse & SEO (campagnedata, zoekwoorden)',
                                'category': 'Marketing & Verkoop', 'savings_pct': 0.40},
    'programming_general': {'label': 'Coderen & Programmeren (schrijven, debuggen, testen)',
                            'category': 'Softwareontwikkeling & IT', 'savings_pct': 0.99},
    'troubleshooting_it': {'label': 'IT-operaties & Probleemoplossing', 'category': 'Softwareontwikkeling & IT',
                           'savings_pct': 0.76},
    'customer_service': {'label': 'Klantenservice (e-mails, vragen beantwoorden)', 'category': 'Klantoperaties',
                         'savings_pct': 0.14},
    'admin_general': {'label': 'Algemene Administratie (plannen, data-invoer, samenvatten)',
                      'category': 'Administratie & HR', 'savings_pct': 0.62},
    'hr_recruitment': {'label': 'Werving & Selectie (HR)', 'category': 'Administratie & HR', 'savings_pct': 0.69},
    'finance_reporting': {'label': 'Financiële Analyse & Rapportage', 'category': 'Financiën & Boekhouding',
                          'savings_pct': 0.40},
}

# --- STATE MANAGEMENT & CALLBACKS ---
# Initialiseert de 'session_state' van Streamlit. Dit is cruciaal om de
# data van de gebruiker te onthouden terwijl ze door de verschillende stappen van de wizard navigeren.
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}


def set_stage(stage_number):
    """Callback functie om de huidige stap van de wizard te wijzigen."""
    st.session_state.stage = stage_number


def store_input(key, value):
    """Callback om een specifieke gebruikersinvoer op te slaan."""
    st.session_state.user_inputs[key] = value


# --- UI FUNCTIES ---
# Deze functies tekenen de verschillende "pagina's" of stappen van de wizard.

def display_welcome_page():
    """Toont de welkomstpagina en de 'Start' knop."""
    st.title("⏱️ AI Tijdswinst Quickscan")
    st.markdown("#### Ontdek hoeveel tijd en kosten uw bedrijf kan besparen door de inzet van AI.")
    st.markdown("""
    Deze tool helpt u in **minder dan 5 minuten** een realistische schatting te maken van de potentiële productiviteitswinst. 
    De berekeningen zijn gebaseerd op een synthese van recent onderzoek van o.a. **McKinsey, Stanford University en de Wereldbank**.

    **Hoe het werkt:**
    1.  **Selecteer taken** die relevant zijn voor uw bedrijf.
    2.  **Voer het aantal uren** in dat uw team wekelijks aan deze taken besteedt.
    3.  **Ontvang direct een gepersonaliseerd dashboard** met uw potentiële tijd- en kostenbesparing.
    """)
    st.button("Start de Quickscan", on_click=set_stage, args=[1], type="primary")


def display_task_input_page():
    """Toont de invoervelden voor de taken en uren."""
    st.header("Stap 1: Wekelijkse Tijdsbesteding")
    st.markdown(
        "Voer in hoeveel uur uw team *gemiddeld per week* besteedt aan de volgende taken. Laat velden op 0 staan als ze niet van toepassing zijn.")

    # Maak een dictionary om de categorieën te groeperen
    categories = {}
    for task_id, task_info in PRODUCTIVITY_DATA.items():
        if task_info['category'] not in categories:
            categories[task_info['category']] = []
        categories[task_info['category']].append((task_id, task_info['label']))

    # Toon de invoervelden per categorie in uitklapbare secties
    for category, tasks in categories.items():
        with st.expander(f"**{category}**", expanded=True):
            for task_id, label in tasks:
                st.number_input(
                    label,
                    min_value=0,
                    step=1,
                    key=f"hours_{task_id}",  # Sla de waarde direct op in session_state
                    help=f"Gemiddeld aantal uren per week besteed aan: {label}"
                )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Terug naar Welkomstpagina", on_click=set_stage, args=[0])
    with col2:
        st.button("Volgende Stap: Kosten & Investering", on_click=set_stage, args=[2], type="primary")


def display_cost_input_page():
    """Toont de (optionele) invoervelden voor kosten en herinvestering."""
    st.header("Stap 2: Financiële Context (Optioneel)")
    st.markdown(
        "Om de financiële impact te berekenen, kunt u een gemiddeld uurtarief invoeren. Deze data wordt **niet** opgeslagen.")

    st.number_input(
        "Gemiddelde uurkost van een medewerker (€)",
        min_value=0,
        step=5,
        key='hourly_rate',
        help="Dit is een gemiddelde om de waarde van de bespaarde tijd te kunnen berekenen."
    )

    st.selectbox(
        "Waarin zou u de bespaarde tijd idealiter herinvesteren?",
        ("Innovatie & productontwikkeling", "Klantrelaties versterken", "Strategische planning",
         "Training & ontwikkeling van medewerkers"),
        key='reinvestment_goal',
        help="Dit helpt om de resultaten in een strategisch kader te plaatsen."
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Terug naar Taken", on_click=set_stage, args=[1])
    with col2:
        st.button("Bekijk Resultaten", on_click=set_stage, args=[3], type="primary")


def display_results_page():
    """Berekent en toont het uiteindelijke resultatendashboard."""
    st.header("📊 Uw Gepersonaliseerde Resultaten")

    # --- BEREKENINGEN ---
    results = []
    total_hours_input = 0
    total_hours_saved = 0

    for task_id, task_info in PRODUCTIVITY_DATA.items():
        hours_input = st.session_state.get(f"hours_{task_id}", 0)
        if hours_input > 0:
            saved_hours = hours_input * task_info['savings_pct']
            results.append({
                'Taak': task_info['label'],
                'Categorie': task_info['category'],
                'Ingevoerde Uren': hours_input,
                'Bespaarde Uren': saved_hours,
                'Uren na AI': hours_input - saved_hours
            })
            total_hours_input += hours_input
            total_hours_saved += saved_hours

    if not results:
        st.warning("U heeft geen uren ingevoerd. Ga terug naar de vorige stap om uw data in te vullen.")
        st.button("Terug naar Taken", on_click=set_stage, args=[1])
        return

    hourly_rate = st.session_state.get('hourly_rate', 0)
    total_cost_saving_yearly = total_hours_saved * hourly_rate * 52
    regained_fte = total_hours_saved / 40

    # --- VISUALISATIE ---
    st.markdown("### Samenvatting van uw Potentieel")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Totaal Bespaarde Uren per Week",
        value=f"{total_hours_saved:.1f} uur",
        help="Het totale aantal uren dat wekelijks kan worden bespaard."
    )
    col2.metric(
        label="Jaarlijkse Financiële Waarde",
        value=f"€ {total_cost_saving_yearly:,.0f}",
        help="De geschatte jaarlijkse besparing, gebaseerd op het door u ingevoerde uurtarief." if hourly_rate > 0 else "Voer een uurtarief in bij de vorige stap voor deze berekening."
    )
    col3.metric(
        label="Teruggewonnen FTE",
        value=f"{regained_fte:.2f}",
        help="Het aantal full-time medewerkers aan productiviteit dat u terugwint."
    )

    st.markdown("---")

    # Dataframe voor de grafiek
    df_results = pd.DataFrame(results)

    st.markdown("### Besparingspotentieel per Taak")

    # Maak een nieuwe dataframe voor de staafdiagram
    df_chart = df_results[['Taak', 'Uren na AI', 'Bespaarde Uren']].copy()
    df_chart.set_index('Taak', inplace=True)

    st.bar_chart(
        df_chart,
        color=["#1f77b4", "#ff7f0e"]  # Kleuren voor 'Uren na AI' en 'Bespaarde Uren'
    )
    st.caption(
        "De grafiek toont de huidige uren (totale hoogte van de staaf), opgesplitst in de uren die overblijven na AI-implementatie en de uren die worden bespaard.")

    st.markdown("---")

    # Strategische aanbeveling
    reinvestment_goal = st.session_state.get('reinvestment_goal', 'uw doelen')
    st.markdown(f"""
    ### Van Tijdswinst naar Bedrijfsgroei
    De **{total_hours_saved:.1f} uur** die u wekelijks bespaart, is meer dan een kostenreductie; het is vrijgemaakt kapitaal. 
    Deze tijd kan direct worden geherinvesteerd in uw focusgebied: **{reinvestment_goal}**. 

    Dit creëert een groeicyclus: AI-efficiëntie financiert innovatie en strategische initiatieven, wat leidt tot groei die verdere investeringen mogelijk maakt.
    """)

    with st.expander("Gedetailleerd overzicht en bronvermelding"):
        st.dataframe(df_results.style.format({
            'Ingevoerde Uren': '{:.0f}',
            'Bespaarde Uren': '{:.1f}',
            'Uren na AI': '{:.1f}'
        }))
        st.markdown("""
        **Methodologie:** De besparingspercentages zijn genormaliseerde gemiddelden, gebaseerd op een analyse van onderzoeken van o.a. McKinsey (The economic potential of generative AI, 2023), Stanford University (Experimental evidence on the productivity effects of generative artificial intelligence, 2024), en de Wereldbank. De tool is bedoeld als een realistische schatting om een strategische discussie te starten.
        """)

    st.button("Opnieuw Beginnen", on_click=set_stage, args=[0])


# --- HOOFD ROUTER ---
# Deze logica bepaalt welke pagina wordt weergegeven op basis van de 'stage' in de session_state.
if st.session_state.stage == 0:
    display_welcome_page()
elif st.session_state.stage == 1:
    display_task_input_page()
elif st.session_state.stage == 2:
    display_cost_input_page()
elif st.session_state.stage == 3:
    display_results_page()
