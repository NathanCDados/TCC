# visualizer.py

import pandas as pd
import matplotlib.pyplot as plt

def plot_top_n_languages(df_escritos: pd.DataFrame, n: int = 10, title_suffix: str = ""):
    """
    Gera um gráfico de barras horizontal dos Top N idiomas.
    """
    # Filtra apenas idiomas definidos
    df_plot = df_escritos[df_escritos["idioma"] != "Indefinido"]

    # Top N idiomas
    idioma_counts = df_plot["idioma"].value_counts().head(n).sort_values(ascending=True)
    
    if idioma_counts.empty:
        print(f"Aviso: Não há dados suficientes para gerar o gráfico Top {n} idiomas.")
        return

    # Gráfico horizontal
    plt.figure(figsize=(10,6))
    plt.barh(idioma_counts.index, idioma_counts.values, color="#4A90E2", edgecolor="gray")

    plt.title(f"Top {n} Idiomas dos Comentários Escritos{title_suffix}", fontsize=14)
    plt.xlabel("Quantidade de Comentários", fontsize=12)
    plt.ylabel("Idioma", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # Exibir os valores no final das barras
    max_val = max(idioma_counts.values)
    for i, v in enumerate(idioma_counts.values):
        # Ajusta a posição do texto com base no valor máximo
        plt.text(v + (max_val * 0.01), i, str(v), va='center', fontsize=10)

    plt.tight_layout()
    plt.show()

def plot_all_languages_distribution(df_escritos: pd.DataFrame):
    """
    Gera um gráfico de barras horizontal com a distribuição de TODOS os idiomas.
    """
    # Filtra apenas idiomas definidos
    df_plot = df_escritos[df_escritos["idioma"] != "Indefinido"]
    
    idioma_counts_todos = df_plot["idioma"].value_counts().sort_values(ascending=True)

    if idioma_counts_todos.empty:
        return 

    # Cria gráfico horizontal (altura dinâmica para caber todos)
    altura_figura = max(6, len(idioma_counts_todos) * 0.3)
    plt.figure(figsize=(10, altura_figura)) 
    plt.barh(idioma_counts_todos.index, idioma_counts_todos.values, color="skyblue", edgecolor="gray")

    plt.title("Distribuição de Todos os Idiomas (Escritos)", fontsize=14)
    plt.xlabel("Quantidade de Comentários", fontsize=12)
    plt.ylabel("Idioma", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # Mostra valores no final das barras
    max_val = max(idioma_counts_todos.values)
    for i, v in enumerate(idioma_counts_todos.values):
        # Ajusta a posição do texto com base no valor máximo
        plt.text(v + (max_val * 0.01), i, str(v), va='center', fontsize=10)

    plt.tight_layout()
    plt.show()