import mysql.connector

def criar_conexao():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='leo2003',
        database='controle_alimentacao'
    )
    return conexao
