from database import criar_conexao
import bcrypt

def cadastrar_usuario(cpf, nome, email, celular, senha, idade, peso, sexo):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO usuarios (cpf, nome, email, celular, senha, idade, peso, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (cpf, nome, email, celular, senha_hash.decode('utf-8'), idade, peso, sexo)
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def autenticar_usuario(cpf, senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    sql = "SELECT senha FROM usuarios WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if resultado:
        senha_hash = resultado[0]
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
    else:
        return False

def obter_dados_usuario(cpf):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    sql = "SELECT nome, email, celular, idade, peso, sexo FROM usuarios WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def atualizar_dados_usuario(cpf, nome, email, celular, senha, idade, peso, sexo):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    if senha:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        sql = "UPDATE usuarios SET nome=%s, email=%s, celular=%s, senha=%s, idade=%s, peso=%s, sexo=%s WHERE cpf=%s"
        valores = (nome, email, celular, senha_hash, idade, peso, sexo, cpf)
    else:
        sql = "UPDATE usuarios SET nome=%s, email=%s, celular=%s, idade=%s, peso=%s, sexo=%s WHERE cpf=%s"
        valores = (nome, email, celular, idade, peso, sexo, cpf)
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def excluir_usuario(cpf):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    # Primeiro, deletar os registros relacionados
    sql_delete_detalhes = """
    DELETE dr FROM detalhes_refeicao dr
    JOIN refeicoes r ON dr.id_refeicao = r.id
    WHERE r.cpf_usuario = %s
    """
    cursor.execute(sql_delete_detalhes, (cpf,))

    sql_delete_refeicoes = "DELETE FROM refeicoes WHERE cpf_usuario = %s"
    cursor.execute(sql_delete_refeicoes, (cpf,))

    # Deletar o usuário
    sql_delete_usuario = "DELETE FROM usuarios WHERE cpf = %s"
    cursor.execute(sql_delete_usuario, (cpf,))

    conexao.commit()
    cursor.close()
    conexao.close()
