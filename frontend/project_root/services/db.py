# =========================================================
# services/db.py
# Gerencia a conexão com o MySQL.
# Carrega credenciais do .env na raiz do projeto.
# =========================================================
import os
import hashlib
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def conectar():
    """Abre e retorna uma nova conexão. Retorna None se falhar."""
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "SenhaPI@1234"),
            database=os.getenv("DB_NAME", "quimic_lab"),
        )
    except Error as e:
        print(f"[DB] Erro ao conectar: {e}")
        return None


def hash_senha(senha: str) -> str:
    """SHA-256 da senha em texto puro."""
    return hashlib.sha256(senha.encode()).hexdigest()
