#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 16:30:37 2025

@author: Éderson D'Martin Costa
"""

import streamlit as st
from error_propagation import Complex


def erroprog(Ti, sig_Ti, Td, sig_Td, PDi, sig_PDi, PDd, sig_PDd):
    """Calcula BMA e incertezas"""
    Ti = Complex(Ti, sig_Ti)
    Td = Complex(Td, sig_Td)

    PDi = Complex(PDi, sig_PDi)
    PDd = Complex(PDd, sig_PDd)

    BMA = 100 * (Td + PDd) / (Ti + PDi)

    txt = str(BMA)
    spt = txt.split()

    med = float(spt[0])  # média
    u = float(spt[2])    # incerteza padrão

    k = 2                # fator de expansão (95%)
    U = k * u            # incerteza expandida

    LI = med - U
    LS = med + U

    return med, u, U, LI, LS


# ================= Streamlit App =================
st.set_page_config(page_title="Balanço de Massas", page_icon="⚗️")

st.title("⚗️ Cálculo de Balanço de Massas Absoluto com Propagação de Incertezas")

st.write("Insira os valores abaixo para calcular o "
         "Balanço de Massas Absoluto (BMA) e propagar as incertezas")

# Entradas do usuário
st.header("📥 Entradas")

col1, col2 = st.columns(2)

with col1:

    st.write("### Antes da degradação")

    Ti = st.number_input("Teor inicial (%) - Ti",
                         min_value=0.0, step=0.1, value=97.2)
    PDi = st.number_input("Somatório dos Produtos de Degradação Inicial (%) - PDi",
                          min_value=0.0, step=0.1, value=0.3)

    st.write("### Desvio Padrão Relativo")
    DPR_T = st.number_input(
        "DPR% para o método de teor",
        min_value=0.0, step=0.1, value=2.0)
    DPR_PD = st.number_input(
        "DPR% para o método de produtos de degradação",
        min_value=0.0, step=0.1, value=10.0)

with col2:

    st.write("### Após a degradação")

    Td = st.number_input("Teor final (%) - Td",
                         min_value=0.0, step=0.1, value=80.6)
    PDd = st.number_input("Somatório dos Produtos de Degradação Final (%) - PDd",
                          min_value=0.0, step=0.1, value=5.7)

# Botão de cálculo
if st.button("📊 Calcular BMA"):
    # Validações
    if Td > Ti:
        st.error(
            "Erro: O teor após a degradação (Td) deve ser menor ou igual ao teor antes (Ti).")
    elif PDd < PDi:
        st.error("Erro: O somatório dos produtos de degradação final (PDd) deve ser maior ou igual ao somatório inicial (PDi).")
    else:
        # Desvios padrão absolutos
        sig_Ti = Ti * DPR_T / 100
        sig_Td = Td * DPR_T / 100
        sig_PDi = PDi * DPR_PD / 100
        sig_PDd = PDd * DPR_PD / 100

        med, u, U, LI, LS = erroprog(
            Ti, sig_Ti, Td, sig_Td, PDi, sig_PDi, PDd, sig_PDd)

        st.header("📈 Resultados")
        st.success(f"**BMA ± u:** {med:.2f}% ± {u:.2f}%".replace(".", ","))
        st.success(
            f"**BMA ± U (k=2, norm):** {med:.2f}% ± {U:.2f}%".replace(".", ","))
        st.info(
            f"**Intervalo de Confiança 95%:** [{LI:.2f}%; {LS:.2f}%]".replace(".", ","))

        with st.expander("🔍 Detalhes dos cálculos"):
            st.write("incerteza padrão Ti: " +
                     f"{sig_Ti:.4f}%".replace(".", ","))
            st.write("incerteza padrão Td: " +
                     f"{sig_Td:.4f}%".replace(".", ","))
            st.write("incerteza padrão PDi: " +
                     f"{sig_PDi:.4f}%".replace(".", ","))
            st.write("incerteza padrão PDd: " +
                     f"{sig_PDd:.4f}%".replace(".", ","))

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 10px;
        bottom: 5px;
        font-size: 11px;
        color: #999999;
        opacity: 0.8;
        user-select: none;
        pointer-events: none;
        z-index: 9999;
    }
    </style>
    <div class="footer">Desenvolvido por Éderson D'Martin Costa</div>
    """,
    unsafe_allow_html=True
)
