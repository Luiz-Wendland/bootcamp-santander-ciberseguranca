"""Exemplo reduzido para revisão estática de uma consulta de usuário."""

import sqlite3


def buscar_usuario(conn: sqlite3.Connection, username: str):
    query = f"SELECT id FROM usuarios WHERE username = '{username}'"
    return conn.execute(query).fetchone()
