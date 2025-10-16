# data_processor.py

import pandas as pd
import emoji
import re
from langdetect import detect, DetectorFactory
import pycountry
import warnings
import swifter # <--- ADICIONADO PARA OTIMIZAÇÃO

# Fixar semente para resultados consistentes na detecção de idioma
DetectorFactory.seed = 0

# Suprime warnings do pycountry (opcional, mas limpa a saída)
warnings.filterwarnings(
    "ignore", 
    message=".*The package or module 'pycountry' does not seem to know.*"
)


def apenas_emoji(texto):
    """Retorna True se o texto contiver apenas emojis (ignorando espaços)."""
    if pd.isna(texto) or str(texto).strip() == "":
        return False
    
    texto_limpo = str(texto).strip()
    texto_limpo = re.sub(r"\s+", "", texto_limpo)  # remove espaços

    # Verifica se todos os caracteres são emojis e se há pelo menos um
    emoji_count = sum(1 for ch in texto_limpo if ch in emoji.EMOJI_DATA)
    return emoji_count > 0 and emoji_count == len(texto_limpo)


def detecta_idioma_nome(texto):
    """Detecta o idioma e retorna o nome completo (ou código/Indefinido)."""
    try:
        codigo = detect(texto)
        
        # Tenta buscar pelo código alpha_2 (mais comum)
        idioma = pycountry.languages.get(alpha_2=codigo)
        if idioma and hasattr(idioma, 'name'):
            return idioma.name.capitalize()
            
        # Tenta buscar pelo código alpha_3 (fallback)
        idioma = pycountry.languages.get(alpha_3=codigo)
        if idioma and hasattr(idioma, 'name'):
            return idioma.name.capitalize()
            
        return codigo  # fallback
    except Exception:
        # Captura erros de detecção
        return "Indefinido"


def process_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Classifica os comentários e detecta o idioma para os comentários 'escritos'.
    Retorna o DF principal e o DF filtrado de 'escritos' com a coluna 'idioma'.
    """
    print("--- 1. Classificação de Tipos (emoji, escrito, vazio) ---")
    
    # Cria a coluna 'tipo'
    df["tipo"] = df["comentario"].apply(
        lambda x: "vazio" if pd.isna(x) or str(x).strip() == "" 
        else ("emoji" if apenas_emoji(x) else "escrito")
    )
    
    print("Distribuição Percentual:")
    print(df["tipo"].value_counts(normalize=True) * 100)
    
    # Filtra e copia os comentários escritos para detecção de idioma
    df_escritos = df[df["tipo"] == "escrito"].copy()
    
    print("\n--- 2. Detecção de Idioma (apenas comentários escritos) ---")
    
    # APLICAÇÃO OTIMIZADA COM SWIFTER para evitar travamentos/lentidão
    print("Iniciando detecção paralelizada. Isso pode levar um tempo...")
    df_escritos["idioma"] = df_escritos["comentario"].swifter.apply(detecta_idioma_nome)
    print("Detecção de idioma concluída.")
    
    # Merge da coluna 'idioma' de volta ao DataFrame principal
    # Usamos merge por "comentario" para transferir a informação
    df = df.merge(
        df_escritos[["comentario", "idioma"]],
        on="comentario",
        how="left",
        suffixes=("_original", "")
    )

    # Preenche N/A na nova coluna 'idioma' para tipos 'emoji'/'vazio'
    df["idioma"] = df["idioma"].fillna("Não aplicável")
    
    return df, df_escritos