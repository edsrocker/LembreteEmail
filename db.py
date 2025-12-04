import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "clientes.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                data_vencimento TEXT NOT NULL,  -- formato YYYY-MM-DD
                dias_antes INTEGER NOT NULL,
                horario_envio TEXT NOT NULL,    -- formato HH:MM (24h)
                caminho_boleto TEXT NOT NULL
            );
            """
        )
        conn.commit()


def inserir_cliente(nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO clientes (nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto),
        )
        conn.commit()


def listar_clientes():
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT id, nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto
            FROM clientes
            ORDER BY data_vencimento;
            """
        )
        return cur.fetchall()
