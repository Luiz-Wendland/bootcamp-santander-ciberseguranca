"""Versão parametrizada da consulta de usuário usada no exemplo."""

import sqlite3


def buscar_usuario(conn: sqlite3.Connection, username: str):
    query = "SELECT id FROM usuarios WHERE username = ?"
    return conn.execute(query, (username,)).fetchone()
