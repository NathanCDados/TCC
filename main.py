# main.py

import pandas as pd
import warnings
from data_processor import process_data
from visualizer import plot_top_n_languages, plot_all_languages_distribution

# Constantes de Arquivo
INPUT_FILE = "comentarios_youtube_com_datas (1).csv"
OUTPUT_FILE = "comentarios_youtube_classificados.xlsx"

def main():
    """
    Função principal para coordenar o fluxo de trabalho.
    """
    # ------------------------------------------------------------------
    # 1. LEITURA DE DADOS E ANÁLISE INICIAL
    # ------------------------------------------------------------------
    print("-" * 50)
    print(f"Iniciando Processamento de Dados do arquivo: {INPUT_FILE}")
    print("-" * 50)
    
    try:
        # Lê o CSV. O uso de .copy() aqui é opcional, mas seguro.
        df_youtube = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{INPUT_FILE}' não encontrado. Verifique o caminho.")
        return

    print("--- ANÁLISE INICIAL ---")
    total_comentarios = len(df_youtube)
    total_comentarios_validos = df_youtube['comentario'].notna().sum()
    print(f"Total de comentários: {total_comentarios}")
    print(f"Total de comentários válidos: {total_comentarios_validos}")
    print("\n" + "="*50 + "\n")

    # ------------------------------------------------------------------
    # 2. PROCESSAMENTO (Classificação e Detecção de Idioma OTIMIZADA)
    # ------------------------------------------------------------------
    # process_data retorna o DF principal completo e o DF dos escritos
    df_youtube_final, df_escritos_processado = process_data(df_youtube.copy())
    
    num_indefinidos = (df_escritos_processado["idioma"] == "Indefinido").sum()
    print(f"\nTotal de comentários escritos com idioma 'Indefinido': {num_indefinidos}")
    print("\n" + "="*50 + "\n")

    # ------------------------------------------------------------------
    # 3. VISUALIZAÇÃO
    # ------------------------------------------------------------------
    print("--- VISUALIZAÇÃO DE DADOS ---")
    
    # Gráfico Top 10
    plot_top_n_languages(df_escritos_processado, n=10)
    
    # Gráfico de Distribuição Completa (Atenção: pode ser ilegível com muitos idiomas)
    plot_all_languages_distribution(df_escritos_processado)

    # ------------------------------------------------------------------
    # 4. SALVAMENTO
    # ------------------------------------------------------------------
    print("--- SALVAMENTO DE DADOS ---")
    try:
        # Garante que o DataFrame final com as colunas 'tipo' e 'idioma' será salvo
        df_youtube_final.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
        print(f"Processo concluído. DataFrame final salvo em: {OUTPUT_FILE}")
    except Exception as e:
        print(f"ERRO ao salvar o arquivo Excel: {e}")


if __name__ == "__main__":
    main()