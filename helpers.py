import streamlit as st
import pandas as pd
import numpy as np
import os

def get_dynamic_color(value, values, lower_is_better=True):
    low, high = np.min(values), np.max(values)
    ratio = (value - low) / (high - low) if high != low else 0
    if lower_is_better:
        ratio = 1 - ratio
    r = int(255 * (1 - ratio))
    g = int(255 * ratio)
    b = 0
    return f'rgb({r},{g},{b})'

def vis_billede(billede_sti, caption):
    if os.path.exists(billede_sti):
        st.image(billede_sti, caption=caption)
    else:
        st.text(f"No image available for {caption}")

def vis_valg(col1, col2, df, kategori, prompt, multiple=False):
    with col1:
        data = df[df['Kategori'] == kategori]
        valg = st.selectbox(prompt, data['Valg'].tolist())
        valgt_data = data[data['Valg'] == valg]
        billede = valgt_data['Billede'].values[0]
        vis_billede(billede, valg)
        antal = 1
        if multiple:
            antal = st.number_input(f"Antal {kategori.lower()}", min_value=1, step=1, value=1)
    with col2:
        st.subheader(f"Valgt {kategori.lower()}")
        st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['Opstartsudgift'].values[0], data['Opstartsudgift'].values, lower_is_better=True)}; padding:10px;'>Opstartsudgift: {valgt_data['Opstartsudgift'].values[0]:,} kr.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['ÅrligUdgift'].values[0], data['ÅrligUdgift'].values, lower_is_better=True)}; padding:10px;'>Årlig udgift: {valgt_data['ÅrligUdgift'].values[0]:,} kr.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['OpstartsCO2'].values[0], data['OpstartsCO2'].values, lower_is_better=True)}; padding:10px;'>Opstarts CO2: {valgt_data['OpstartsCO2'].values[0]:,} ton</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['LøbendeCO2'].values[0], data['LøbendeCO2'].values, lower_is_better=True)}; padding:10px;'>Løbende CO2: {valgt_data['LøbendeCO2'].values[0]:,} ton/år</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['Indtjening'].values[0], data['Indtjening'].values, lower_is_better=False)}; padding:10px;'>Indtjening: {valgt_data['Indtjening'].values[0]:,} kr.</div>", unsafe_allow_html=True)
        if 'CO2Reduktion' in valgt_data.columns:
            st.markdown(f"<div style='background-color:{get_dynamic_color(valgt_data['CO2Reduktion'].values[0], data['CO2Reduktion'].values, lower_is_better=False)}; padding:10px;'>CO2 Reduktion: {valgt_data['CO2Reduktion'].values[0]:,} ton/år</div>", unsafe_allow_html=True)
    return valgt_data, antal

def vis_tiltag(col1, col2, df, kategori, prompt):
    total_opstartsudgift = 0
    total_årligudgift = 0
    total_opstartsco2 = 0
    total_løbendeco2 = 0
    total_reduktion = 0
    
    with col1:
        data = df[df['Kategori'] == kategori]
        tiltag_valg = {}
        for i, row in data.iterrows():
            tiltag_valg[row['Valg']] = st.checkbox(row['Valg'], key=row['Valg'])
            if tiltag_valg[row['Valg']]:
                total_opstartsudgift += row['Opstartsudgift']
                total_årligudgift += row['ÅrligUdgift']
                total_opstartsco2 += row['OpstartsCO2']
                total_løbendeco2 += row['LøbendeCO2']
                if 'CO2Reduktion' in row:
                    total_reduktion += row['CO2Reduktion']
    
    with col2:
        st.subheader(f"Valgte {kategori.lower()} tiltag")
        st.markdown(f"<div style='background-color:{get_dynamic_color(total_opstartsudgift, data['Opstartsudgift'].values, lower_is_better=True)}; padding:10px;'>Samlet opstartsudgift: {total_opstartsudgift:,} kr.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(total_årligudgift, data['ÅrligUdgift'].values, lower_is_better=True)}; padding:10px;'>Samlet årlig udgift: {total_årligudgift:,} kr.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(total_opstartsco2, data['OpstartsCO2'].values, lower_is_better=True)}; padding:10px;'>Samlet opstarts CO2: {total_opstartsco2:,} ton</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(total_løbendeco2, data['LøbendeCO2'].values, lower_is_better=True)}; padding:10px;'>Samlet løbende CO2: {total_løbendeco2:,} ton/år</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:{get_dynamic_color(total_reduktion, data['CO2Reduktion'].values, lower_is_better=False)}; padding:10px;'>Samlet CO2 reduktion: {total_reduktion:,} ton/år</div>", unsafe_allow_html=True)
    
    return total_opstartsudgift, total_årligudgift, total_opstartsco2, total_løbendeco2, total_reduktion

def beregn_totaler(energi, produktion, materiale, transport, affald):
    total_opstart = (energi[0]['Opstartsudgift'].values[0] * energi[1] +
                     produktion[0]['Opstartsudgift'].values[0] * produktion[1] +
                     materiale[0]['Opstartsudgift'].values[0] * materiale[1] +
                     transport[0]['Opstartsudgift'].values[0] * transport[1] +
                     affald[0]['Opstartsudgift'].values[0] * affald[1])

    total_årlig = (energi[0]['ÅrligUdgift'].values[0] * energi[1] +
                   produktion[0]['ÅrligUdgift'].values[0] * produktion[1] +
                   materiale[0]['ÅrligUdgift'].values[0] * materiale[1] +
                   transport[0]['ÅrligUdgift'].values[0] * transport[1] +
                   affald[0]['ÅrligUdgift'].values[0] * affald[1])

    total_opstart_co2 = (energi[0]['OpstartsCO2'].values[0] * energi[1] +
                         produktion[0]['OpstartsCO2'].values[0] * produktion[1] +
                         materiale[0]['OpstartsCO2'].values[0] * materiale[1] +
                         transport[0]['OpstartsCO2'].values[0] * transport[1] +
                         affald[0]['OpstartsCO2'].values[0] * affald[1])

    total_løbende_co2 = (energi[0]['LøbendeCO2'].values[0] * energi[1] +
                         produktion[0]['LøbendeCO2'].values[0] * produktion[1] +
                         materiale[0]['LøbendeCO2'].values[0] * materiale[1] +
                         transport[0]['LøbendeCO2'].values[0] * transport[1] +
                         affald[0]['LøbendeCO2'].values[0] * affald[1])

    total_indtjening = (produktion[0]['Indtjening'].values[0] * produktion[1] +
                        materiale[0]['Indtjening'].values[0] * materiale[1])

    total_co2_reduktion = (energi[0].get('CO2Reduktion', 0).values[0] * energi[1] +
                           produktion[0].get('CO2Reduktion', 0).values[0] * produktion[1] +
                           materiale[0].get('CO2Reduktion', 0).values[0] * materiale[1] +
                           transport[0].get('CO2Reduktion', 0).values[0] * transport[1] +
                           affald[0].get('CO2Reduktion', 0).values[0] * affald[1])

    return total_opstart, total_årlig, total_opstart_co2, total_løbende_co2, total_indtjening, total_co2_reduktion


def vis_resultater(valgt_aar, startkapital, total_opstart, penge_efter_opstart, total_årlig, total_indtjening, total_opstart_co2, total_løbende_co2, total_co2_reduktion, penge, co2):
    st.sidebar.header(f"Resultater for år {valgt_aar}")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        st.markdown(f"### Opstart:")
        st.markdown(f"**Startkapital:** {startkapital:,} kr.")
        st.markdown(f"**Opstartudgifter:** {total_opstart:,} kr.")
        st.markdown(f"**Penge tilbage:** {penge_efter_opstart:,} kr.")
    
    with col2:
        st.markdown(f"### Løbende kapital")
        st.markdown(f"**Udgifter per år:** {total_årlig:,} kr.")
        st.markdown(f"**Indtjening per år:** {total_indtjening:,} kr.")
        forskel_per_aar = total_indtjening - total_årlig
        st.markdown(f"**Forskel per år:** {forskel_per_aar:,} kr.")
    
    with col3:
        st.markdown(f"### Løbende CO2")
        st.markdown(f"**Opstarts CO2:** {total_opstart_co2:,} ton")
        st.markdown(f"**Løbende CO2 per år:** {total_løbende_co2:,} ton")
        st.markdown(f"**Forskel per år:** {-total_co2_reduktion:,} ton")
    
    if valgt_aar > 0:
        st.sidebar.markdown(f"### Resultater for år {valgt_aar}")
        st.sidebar.markdown(f"**Total Kapital:** {penge:,} kr.")
        st.sidebar.markdown(f"**Total CO2:** {co2:,} ton")

def gem_highscore(highscore_df, highscore_path, navn, kapital_aar1, kapital_aar10, co2_aar1, co2_aar10):
    score_kapital_aar1 = kapital_aar1 / 10000
    score_kapital_aar10 = kapital_aar10 / 10000
    score_co2_aar1 = 0 - co2_aar1
    score_co2_aar10 = 0 - co2_aar10
    score = score_kapital_aar1 + score_kapital_aar10 + score_co2_aar1 + score_co2_aar10
    
    ny_highscore = pd.DataFrame({
        'Navn': [navn], 
        'Kapital_år1': [kapital_aar1], 
        'Kapital_år10': [kapital_aar10], 
        'CO2_år1': [co2_aar1], 
        'CO2_år10': [co2_aar10], 
        'Score': [score]
    })
    highscore_df = pd.concat([highscore_df, ny_highscore], ignore_index=True)
    highscore_df.to_csv(highscore_path, index=False)
    
    st.write(f"Scoreberegning:")
    st.write(f"Kapital år 1: {kapital_aar1} / 10000 = {score_kapital_aar1}")
    st.write(f"Kapital år 10: {kapital_aar10} / 10000 = {score_kapital_aar10}")
    st.write(f"CO2 år 1: 0 - {co2_aar1} = {score_co2_aar1}")
    st.write(f"CO2 år 10: 0 - {co2_aar10} = {score_co2_aar10}")
    st.write(f"Samlet score: {score}")


def vis_highscore(st, highscore_df):
    st.dataframe(highscore_df.style.format({"Kapital_år1": "{:,}", "Kapital_år10": "{:,}", "CO2_år1": "{:,}", "CO2_år10": "{:,}", "Score": "{:,.2f}"}))
