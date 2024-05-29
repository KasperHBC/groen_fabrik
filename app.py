import streamlit as st
import pandas as pd
import numpy as np
import os
from helpers import get_dynamic_color, vis_billede, beregn_totaler, vis_valg, vis_resultater, vis_tiltag, gem_highscore, vis_highscore

# Filstier
highscore_path = 'highscore.csv'

# Funktion til at initialisere highscore-filen
def init_highscore_file():
    if not os.path.exists(highscore_path) or os.path.getsize(highscore_path) == 0:
        highscore_df = pd.DataFrame(columns=['Navn', 'Kapital_år1', 'Kapital_år10', 'CO2_år1', 'CO2_år10', 'Score'])
        highscore_df.to_csv(highscore_path, index=False)

# Initialiser highscore-filen
init_highscore_file()

# Læs highscore data
highscore_df = pd.read_csv(highscore_path)

# Funktion til at navigere mellem sider
def navigate_to(page):
    st.session_state.page = page

def vis_forside():
    st.title("Velkommen til Grøn Fabrik Simulation")
    st.markdown("""
    Velkommen til Grøn Fabrik Simulation! Her kan du lære om at drive en miljøvenlig fabrik. Vælg en af følgende muligheder for at komme i gang:
    - Gå til spillet og prøv at skabe den grønneste og mest rentable fabrik.
    - Se highscore listen og sammenlign dine resultater med andre.
    """)
    if st.button("Gå til spillet"):
        navigate_to("spillet")
    if st.button("Se highscore"):
        navigate_to("highscore")

def vis_spillet():
    st.title("Grøn Fabrik Simulation")

    # Initial startkapital
    startkapital = 1000000

    # Læs data fra CSV
    df = pd.read_csv('data.csv')

    # Energikilder
    col1, col2 = st.columns([1, 2])
    energi, energi_antal = vis_valg(col1, col2, df, 'Energikilder', "Vælg en energikilde")

    # Produktionsmetoder
    col3, col4 = st.columns([1, 2])
    produktion, produktion_antal = vis_valg(col3, col4, df, 'Produktionsmetoder', "Vælg en produktionsmetode", multiple=True)

    # Materialevalg
    col5, col6 = st.columns([1, 2])
    materiale, materiale_antal = vis_valg(col5, col6, df, 'Materialevalg', "Vælg materialevalg")

    # Transportmetoder
    col7, col8 = st.columns([1, 2])
    transport, transport_antal = vis_valg(col7, col8, df, 'Transportmetoder', "Vælg en transportmetode", multiple=True)

    # Affaldshåndtering
    col9, col10 = st.columns([1, 2])
    affald, affald_antal = vis_valg(col9, col10, df, 'Affaldshåndtering', "Vælg en affaldshåndteringsmetode")

    # Udstyrsopdatering
    col11, col12 = st.columns([1, 2])
    total_udstyr_opstart, total_udstyr_årlig, total_udstyr_opstart_co2, total_udstyr_løbende_co2, total_udstyr_reduktion = vis_tiltag(col11, col12, df, 'Udstyrsopdatering', "Vælg en udstyrsopdatering")

    # CO2-reducerende tiltag
    col13, col14 = st.columns([1, 2])
    total_tiltag_opstart, total_tiltag_årlig, total_tiltag_opstart_co2, total_tiltag_løbende_co2, total_tiltag_reduktion = vis_tiltag(col13, col14, df, 'CO2-Reducerende tiltag', "Vælg CO2-reducerende tiltag")

    # Beregn totaler
    total_opstart, total_årlig, total_opstart_co2, total_løbende_co2, total_indtjening, total_co2_reduktion = beregn_totaler(
        [energi, energi_antal], [produktion, produktion_antal], [materiale, materiale_antal], [transport, transport_antal], [affald, affald_antal]
    )

    # Inkluder de valgte CO2-reducerende tiltag og udstyrsopdateringer i totalerne
    total_opstart += total_tiltag_opstart + total_udstyr_opstart
    total_årlig += total_tiltag_årlig + total_udstyr_årlig
    total_opstart_co2 += total_tiltag_opstart_co2 + total_udstyr_opstart_co2
    total_løbende_co2 += total_tiltag_løbende_co2 + total_udstyr_løbende_co2
    total_co2_reduktion += total_tiltag_reduktion + total_udstyr_reduktion

    # Beregn statistik for hvert år fra 0 til 10
    years = range(11)
    penge_aar = [startkapital - total_opstart]  # Penge tilbage efter opstart
    for year in years[1:]:
        penge_aar.append(penge_aar[-1] + total_indtjening - total_årlig)

    co2_aar = [total_opstart_co2 + (total_løbende_co2 - total_co2_reduktion) * year for year in years]

    # Valg af år
    valgt_aar = st.sidebar.selectbox("Vælg år", years)

    # Vis resultater for det valgte år
    vis_resultater(valgt_aar, startkapital, total_opstart, penge_aar[0], total_årlig, total_indtjening, total_opstart_co2, total_løbende_co2, total_co2_reduktion, penge_aar[valgt_aar], co2_aar[valgt_aar])

    # Indtast navn og gem highscore
    with st.sidebar:
        st.header("Gem din highscore")
        navn = st.text_input("Indtast dit navn")
        if st.button("Gem highscore"):
            gem_highscore(highscore_df, highscore_path, navn, penge_aar[1], penge_aar[10], co2_aar[1], co2_aar[10])
            st.success("Highscore gemt!")

    # Gå tilbage til forsiden eller se highscore liste
    if st.button("Tilbage til forsiden"):
        navigate_to("forside")
    if st.button("Se highscore"):
        navigate_to("highscore")

def vis_highscore_side():
    st.title("Highscore Liste")
    vis_highscore(st, highscore_df)
    if st.button("Tilbage til forsiden"):
        navigate_to("forside")
    if st.button("Gå til spillet"):
        navigate_to("spillet")

# Initialiser session state for side
if 'page' not in st.session_state:
    st.session_state.page = "forside"

# Vis den valgte side
page = st.session_state.page
if page == "forside":
    vis_forside()
elif page == "spillet":
    vis_spillet()
elif page == "highscore":
    vis_highscore_side()
