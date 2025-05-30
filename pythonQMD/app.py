# This file generated by Quarto; do not edit by hand.
# shiny_mode: core

from __future__ import annotations

from pathlib import Path
from shiny import App, Inputs, Outputs, Session, ui

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import reactive
from shiny.express import render, ui
from scipy import stats

# Carregar dados
df = sns.load_dataset("taxis").dropna()

# ========================================================================




def server(input: Inputs, output: Outputs, session: Session) -> None:
    # Input 1: Range slider para distância (diferente dos exemplos)
    ui.input_slider(
        "distancia",
        "Filtrar por distancia (milhas):",
        min=0,
        max=round(df["distance"].max()),
        value=[0, round(df["distance"].max())]
    )

    # Input 2: Radio buttons para método de pagamento (diferente dos exemplos)
    ui.input_radio_buttons(
        "payment_method",
        "Metodo de Pagamento:",
        choices=["Todos"] + sorted(df["payment"].unique().tolist()),
        selected="Todos"
    )

    ui.hr()
    ui.markdown("**Fonte:** Dataset `taxis` do Seaborn")

    # ========================================================================

    @reactive.calc
    def filtered_data():
        data = df.copy()
    
        # Filtrar por distância
        data = data[
            (data["distance"] >= input.distancia()[0]) &
            (data["distance"] <= input.distancia()[1])
        ]
    
        # Filtrar por método de pagamento
        if input.payment_method() != "Todos":
            data = data[data["payment"] == input.payment_method()]
        
        return data

    # ========================================================================

    @render.ui
    def metricas():
        dados = filtered_data()
    
        ui.h2("Metricas Principais")
    
        with ui.card(class_="bg-primary text-white p-3 m-2"):
            ui.card_header("Total de Corridas")
            ui.p(f"{len(dados)}", class_="h3")
    
        with ui.card(class_="bg-success text-white p-3 m-2"):
            ui.card_header("Valor Medio")
            ui.p(f"${dados['fare'].mean():.2f}", class_="h3")
    
        with ui.card(class_="bg-info text-white p-3 m-2"):
            ui.card_header("Distancia Media")
            ui.p(f"{dados['distance'].mean():.2f} milhas", class_="h3")
    
        return ui.TagList()


    # ========================================================================

    @render.plot
    def distance_value_plot():
        dados = filtered_data()
    
        # Criar figura e eixos
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Definir paleta de cores
        palette = {"cash": "#1f77b4", "credit card": "#ff7f0e"}
    
        # Plotar pontos
        if input.payment_method() == "Todos":
            sns.scatterplot(
                data=dados,
                x="distance",
                y="total",
                hue="payment",
                palette=palette,
                alpha=0.7,
                ax=ax
            )
        else:
            sns.scatterplot(
                data=dados,
                x="distance",
                y="total",
                color=palette.get(input.payment_method(), "#1f77b4"),
                alpha=0.7,
                ax=ax
            )
    
        # Adicionar linha de tendência
        x = dados["distance"]
        y = dados["total"]
    
        # Calcular a linha de tendência
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line_x = np.array([x.min(), x.max()])
        line_y = slope * line_x + intercept
    
        # Plotar a linha de tendência
        plt.plot(line_x, line_y, color="red", linestyle="--", linewidth=2)
    
        # Adicionar texto com equação da reta e R²
        equation = f"y = {slope:.2f}x + {intercept:.2f}"
        r_squared = f"R² = {r_value**2:.2f}"
        plt.annotate(
            f"{equation}\n{r_squared}",
            xy=(0.05, 0.95),
            xycoords="axes fraction",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8)
        )
    
        # Configurar o gráfico
        plt.title("Relacao entre Distancia e Valor Total", fontsize=14)
        plt.xlabel("Distancia (milhas)", fontsize=12)
        plt.ylabel("Valor Total ($)", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
    
        return fig

    # ========================================================================

    @render.plot
    def payment_analysis_plot():
        dados = filtered_data()
    
        # Agrupar dados por método de pagamento
        payment_summary = dados.groupby("payment").agg({
            "total": "mean",
            "tip": "mean",
            "distance": "mean"
        }).reset_index()
    
        # Definir paleta de cores
        colors = ["#1f77b4", "#ff7f0e"]
    
        # Criar figura e eixos
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Plotar barras
        bars = sns.barplot(
            data=payment_summary,
            x="payment",
            y="total",
            palette=colors,
            ax=ax
        )
    
        # Adicionar valores nas barras
        for i, bar in enumerate(bars.patches):
            value = payment_summary.iloc[i]["total"]
            text = f"${value:.2f}"
            bars.annotate(
                text,
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom",
                fontsize=10
            )
    
        # Configurações do gráfico
        plt.title("Valor Medio por Metodo de Pagamento", fontsize=14)
        plt.xlabel("Metodo de Pagamento", fontsize=12)
        plt.ylabel("Valor Medio ($)", fontsize=12)
        plt.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
    
        return fig

    # ========================================================================

    @render.data_frame
    def tabela():
        return filtered_data()[["pickup", "dropoff", "distance", "fare", "tip", "total", "payment"]]

    # ========================================================================



    return None


_static_assets = ["trabalho_correlacao_files","trabalho_correlacao_files\\libs\\quarto-html\\tippy.css","trabalho_correlacao_files\\libs\\quarto-html\\quarto-syntax-highlighting-dark-a5cd134f9b40a21b85be3e62cd27a8fe.css","trabalho_correlacao_files\\libs\\quarto-html\\quarto-syntax-highlighting-7b4406b7675125bc2ba204020e191172.css","trabalho_correlacao_files\\libs\\bootstrap\\bootstrap-icons.css","trabalho_correlacao_files\\libs\\bootstrap\\bootstrap-dark-5541884affe7b4a4e07fa92b3ba219ba.min.css","trabalho_correlacao_files\\libs\\bootstrap\\bootstrap-5541884affe7b4a4e07fa92b3ba219ba.min.css","trabalho_correlacao_files\\libs\\quarto-dashboard\\datatables.min.css","trabalho_correlacao_files\\libs\\clipboard\\clipboard.min.js","trabalho_correlacao_files\\libs\\quarto-html\\quarto.js","trabalho_correlacao_files\\libs\\quarto-html\\tabsets\\tabsets.js","trabalho_correlacao_files\\libs\\quarto-html\\popper.min.js","trabalho_correlacao_files\\libs\\quarto-html\\tippy.umd.min.js","trabalho_correlacao_files\\libs\\quarto-html\\anchor.min.js","trabalho_correlacao_files\\libs\\bootstrap\\bootstrap.min.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\quarto-dashboard.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\stickythead.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\datatables.min.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\pdfmake.min.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\vfs_fonts.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\web-components.js","trabalho_correlacao_files\\libs\\quarto-dashboard\\components.js"]
_static_assets = {"/" + sa: Path(__file__).parent / sa for sa in _static_assets}

app = App(
    Path(__file__).parent / "trabalho_correlacao.html",
    server,
    static_assets=_static_assets,
)
