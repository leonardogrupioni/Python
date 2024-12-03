from database import criar_conexao

def obter_alimentos():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, calorias_por_porcao FROM alimentos")
    alimentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return alimentos

def registrar_refeicao(cpf_usuario, tipo_refeicao, data_refeicao, alimentos_selecionados):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    # Insere a refeição
    sql_refeicao = "INSERT INTO refeicoes (cpf_usuario, tipo_refeicao, data_refeicao) VALUES (%s, %s, %s)"
    cursor.execute(sql_refeicao, (cpf_usuario, tipo_refeicao, data_refeicao))
    id_refeicao = cursor.lastrowid
    # Insere os detalhes da refeição
    sql_detalhes = "INSERT INTO detalhes_refeicao (id_refeicao, id_alimento, proporcao) VALUES (%s, %s, %s)"
    for alimento_id, proporcao in alimentos_selecionados.items():
        cursor.execute(sql_detalhes, (id_refeicao, alimento_id, proporcao))
    conexao.commit()
    cursor.close()
    conexao.close()

def calcular_calorias(alimentos_selecionados):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    total_calorias = 0
    for alimento_id, proporcao in alimentos_selecionados.items():
        cursor.execute("SELECT calorias_por_porcao FROM alimentos WHERE id = %s", (alimento_id,))
        calorias_por_porcao = float(cursor.fetchone()[0])
        total_calorias += calorias_por_porcao * proporcao
    cursor.close()
    conexao.close()
    return total_calorias

def obter_historico_refeicoes(cpf_usuario, tipo_refeicao, data_refeicao):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    sql = """
    SELECT a.nome, a.calorias_por_porcao, dr.proporcao
    FROM refeicoes r
    JOIN detalhes_refeicao dr ON r.id = dr.id_refeicao
    JOIN alimentos a ON dr.id_alimento = a.id
    WHERE r.cpf_usuario = %s AND r.tipo_refeicao = %s AND r.data_refeicao = %s
    """
    cursor.execute(sql, (cpf_usuario, tipo_refeicao, data_refeicao))
    historico = cursor.fetchall()
    cursor.close()
    conexao.close()
    return historico

def adicionar_alimento(nome, calorias_por_porcao):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    sql = "INSERT INTO alimentos (nome, calorias_por_porcao) VALUES (%s, %s)"
    cursor.execute(sql, (nome, calorias_por_porcao))
    conexao.commit()
    cursor.close()
    conexao.close()
