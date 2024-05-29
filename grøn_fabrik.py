import streamlit as st
import pandas as pd
import numpy as np
import os

# Initial startkapital
startkapital = 100000

# Læs data fra CSV
df = pd.read_csv('data.csv')

# Funktion til at beregne dynamiske grænser for farverne
def get_dynamic_color(value, values, is_good=True):
    low, high = np.min(values), np.max(values)
    mid = (low + high) / 2

    if is_good:
        if value <= mid:
            return 'green'
        elif value <= (mid + high) / 2:
            return 'yellow'
        else:
            return 'red'
    else:
        if value >= mid:
            return 'green'
        elif value >= (mid + low) / 2:
            return 'yellow'
        else:
            return 'red'

# Funktion til at vise billede eller fallback tekst
def vis_billede(billede_sti, caption):
    if os.path.exists(billede_sti):
        st.image(billede_sti, caption=caption)
    else:
        st.text(f"No image available for {caption}")

st.title("Grøn Fabrik Simulation")

# Energikilder
col1, col2 = st.columns([1, 2])
with col1:
    energikilder = df[df['Kategori'] == 'Energikilder']
    energi = st.selectbox("Vælg en energikilde", energikilder['Valg'].tolist())
    valgt_energi = energikilder[energikilder['Valg'] == energi]
    energi_billede = valgt_energi['Billede'].values[0]
    vis_billede(energi_billede, energi)
with col2:
    st.subheader("Valgt energikilde")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_energi['Opstartsudgift'].values[0], energikilder['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_energi['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_energi['ÅrligUdgift'].values[0], energikilder['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_energi['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_energi['CO2udledning'].values[0], energikilder['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_energi['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_energi['Energiforbrug'].values[0], energikilder['Energiforbrug'].values, is_good=False)}; padding:10px;'>Energiforbrug: {valgt_energi['Energiforbrug'].values[0]}</div>", unsafe_allow_html=True)

# Produktionsmetoder
col3, col4 = st.columns([1, 2])
with col3:
    produktionsmetoder = df[df['Kategori'] == 'Produktionsmetoder']
    produktion = st.selectbox("Vælg en produktionsmetode", produktionsmetoder['Valg'].tolist())
    valgt_produktionsmetode = produktionsmetoder[produktionsmetoder['Valg'] == produktion]
    produktion_billede = valgt_produktionsmetode['Billede'].values[0]
    vis_billede(produktion_billede, produktion)
with col4:
    st.subheader("Valgt produktionsmetode")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_produktionsmetode['Opstartsudgift'].values[0], produktionsmetoder['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_produktionsmetode['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_produktionsmetode['ÅrligUdgift'].values[0], produktionsmetoder['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_produktionsmetode['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_produktionsmetode['CO2udledning'].values[0], produktionsmetoder['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_produktionsmetode['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_produktionsmetode['Ressourceforbrug'].values[0], produktionsmetoder['Ressourceforbrug'].values, is_good=False)}; padding:10px;'>Ressourceforbrug: {valgt_produktionsmetode['Ressourceforbrug'].values[0]}</div>", unsafe_allow_html=True)

# Materialevalg
col5, col6 = st.columns([1, 2])
with col5:
    materialer = df[df['Kategori'] == 'Materialevalg']
    materiale = st.selectbox("Vælg materialevalg", materialer['Valg'].tolist())
    valgt_materiale = materialer[materialer['Valg'] == materiale]
    materiale_billede = valgt_materiale['Billede'].values[0]
    vis_billede(materiale_billede, materiale)
with col6:
    st.subheader("Valgt materialevalg")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_materiale['Opstartsudgift'].values[0], materialer['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_materiale['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_materiale['ÅrligUdgift'].values[0], materialer['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_materiale['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_materiale['CO2udledning'].values[0], materialer['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_materiale['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_materiale['Affaldsproduktion'].values[0], materialer['Affaldsproduktion'].values, is_good=False)}; padding:10px;'>Affaldsproduktion: {valgt_materiale['Affaldsproduktion'].values[0]}</div>", unsafe_allow_html=True)

# Transportmetoder
col7, col8 = st.columns([1, 2])
with col7:
    transportmetoder = df[df['Kategori'] == 'Transportmetoder']
    transport = st.selectbox("Vælg en transportmetode", transportmetoder['Valg'].tolist())
    valgt_transport = transportmetoder[transportmetoder['Valg'] == transport]
    transport_billede = valgt_transport['Billede'].values[0]
    vis_billede(transport_billede, transport)
with col8:
    st.subheader("Valgt transportmetode")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_transport['Opstartsudgift'].values[0], transportmetoder['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_transport['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_transport['ÅrligUdgift'].values[0], transportmetoder['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_transport['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_transport['CO2udledning'].values[0], transportmetoder['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_transport['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)

# Affaldshåndtering
col9, col10 = st.columns([1, 2])
with col9:
    affaldshandtering = df[df['Kategori'] == 'Affaldshåndtering']
    affald = st.selectbox("Vælg en affaldshåndteringsmetode", affaldshandtering['Valg'].tolist())
    valgt_affald = affaldshandtering[affaldshandtering['Valg'] == affald]
    affald_billede = valgt_affald['Billede'].values[0]
    vis_billede(affald_billede, affald)
with col10:
    st.subheader("Valgt affaldshåndtering")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_affald['Opstartsudgift'].values[0], affaldshandtering['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_affald['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_affald['ÅrligUdgift'].values[0], affaldshandtering['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_affald['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_affald['CO2udledning'].values[0], affaldshandtering['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_affald['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)

# Udstyrsopdatering
col11, col12 = st.columns([1, 2])
with col11:
    udstyr = df[df['Kategori'] == 'Udstyrsopdatering']
    udstyrsvalg = st.selectbox("Vælg en udstyrsopdatering", udstyr['Valg'].tolist())
    valgt_udstyr = udstyr[udstyr['Valg'] == udstyrsvalg]
    udstyr_billede = valgt_udstyr['Billede'].values[0]
    vis_billede(udstyr_billede, udstyrsvalg)
with col12:
    st.subheader("Valgt udstyrsopdatering")
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_udstyr['Opstartsudgift'].values[0], udstyr['Opstartsudgift'].values, is_good=False)}; padding:10px;'>Opstartsudgift: {valgt_udstyr['Opstartsudgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_udstyr['ÅrligUdgift'].values[0], udstyr['ÅrligUdgift'].values, is_good=False)}; padding:10px;'>Årlig udgift: {valgt_udstyr['ÅrligUdgift'].values[0]} kr.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_udstyr['CO2udledning'].values[0], udstyr['CO2udledning'].values)}; padding:10px;'>CO2-udledning: {valgt_udstyr['CO2udledning'].values[0]} ton</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_udstyr['Energiforbrug'].values[0], udstyr['Energiforbrug'].values, is_good=False)}; padding:10px;'>Energiforbrug: {valgt_udstyr['Energiforbrug'].values[0]}</div>", unsafe_allow_html=True)

# Beregn totaler
total_opstart = (valgt_energi['Opstartsudgift'].values[0] +
                 valgt_produktionsmetode['Opstartsudgift'].values[0] +
                 valgt_materiale['Opstartsudgift'].values[0] +
                 valgt_transport['Opstartsudgift'].values[0] +
                 valgt_affald['Opstartsudgift'].values[0] +
                 valgt_udstyr['Opstartsudgift'].values[0])

total_årlig = (valgt_energi['ÅrligUdgift'].values[0] +
               valgt_produktionsmetode['ÅrligUdgift'].values[0] +
               valgt_materiale['ÅrligUdgift'].values[0] +
               valgt_transport['ÅrligUdgift'].values[0] +
               valgt_affald['ÅrligUdgift'].values[0] +
               valgt_udstyr['ÅrligUdgift'].values[0])

total_co2 = (valgt_energi['CO2udledning'].values[0] +
             valgt_produktionsmetode['CO2udledning'].values[0] +
             valgt_materiale['CO2udledning'].values[0] +
             valgt_transport['CO2udledning'].values[0] +
             valgt_affald['CO2udledning'].values[0] +
             valgt_udstyr['CO2udledning'].values[0])

total_energiforbrug = (valgt_energi['Energiforbrug'].values[0] +
                       valgt_produktionsmetode['Energiforbrug'].values[0] +
                       valgt_materiale['Energiforbrug'].values[0] +
                       valgt_udstyr['Energiforbrug'].values[0])

total_ressourceforbrug = (valgt_produktionsmetode['Ressourceforbrug'].values[0] +
                          valgt_materiale['Ressourceforbrug'].values[0])

total_affaldsproduktion = (valgt_materiale['Affaldsproduktion'].values[0] +
                           valgt_affald['Affaldsproduktion'].values[0])

total_indtjening = (valgt_energi['Indtjening'].values[0] +
                    valgt_produktionsmetode['Indtjening'].values[0] +
                    valgt_materiale['Indtjening'].values[0] +
                    valgt_transport['Indtjening'].values[0] +
                    valgt_udstyr['Indtjening'].values[0])

# Vis resultater i en DataFrame
resultater = pd.DataFrame({
    "Parameter": ["Opstartsudgift", "Årlig udgift", "CO2-udledning", "Energiforbrug", "Ressourceforbrug", "Affaldsproduktion", "Indtjening"],
    "Værdi": [total_opstart, total_årlig, total_co2, total_energiforbrug, total_ressourceforbrug, total_affaldsproduktion, total_indtjening]
})

# Vis resultater i sidebaren
st.sidebar.header("Resultater")
st.sidebar.dataframe(resultater)

# Beregn overskud eller underskud
overskud = startkapital - total_opstart + total_indtjening
forventet_overskud = overskud - total_årlig

if forventet_overskud > startkapital:
    st.sidebar.success(f"Din fabrik er både økonomisk rentabel og grøn! Forventet kapital efter 1 år: {forventet_overskud} kr.")
else:
    st.sidebar.error(f"Din fabrik er ikke økonomisk rentabel eller ikke grøn nok. Forventet kapital efter 1 år: {forventet_overskud} kr.")
