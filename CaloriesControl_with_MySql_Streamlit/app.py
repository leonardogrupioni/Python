import streamlit as st
from auth import cadastrar_usuario, autenticar_usuario, obter_dados_usuario, atualizar_dados_usuario, excluir_usuario
from alimentacao import (obter_alimentos, registrar_refeicao, calcular_calorias,
                         obter_historico_refeicoes, adicionar_alimento)
from datetime import date

def main():
    st.title("Controle de Alimentação Diária")

    # Inicializa o estado de sessão
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['cpf'] = ''

    if st.session_state['logged_in']:
        # Usuário logado
        st.sidebar.write(f"Usuário: {st.session_state['cpf']}")
        opcoes = ["Adicionar Alimentação", "Ver Histórico", "Adicionar Alimentos", "Gerenciar Conta", "Sair (Clique duas Vezes para Confirmar)"]
        opcao = st.sidebar.selectbox("Selecione uma opção", opcoes)

        if opcao == "Adicionar Alimentação":
            adicionar_alimentacao(st.session_state['cpf'])
        elif opcao == "Ver Histórico":
            ver_historico(st.session_state['cpf'])
        elif opcao == "Adicionar Alimentos":
            gerenciar_alimentos()
        elif opcao == "Gerenciar Conta":
            gerenciar_conta(st.session_state['cpf'])
        elif opcao == "Sair (Clique duas Vezes para Confirmar)":
            sair_button = st.button("Clique aqui para confirmar logout")
            if sair_button:
                st.session_state['logged_in'] = False
                st.session_state['cpf'] = ''
                st.success("Você saiu do sistema.")
    else:
        # Usuário não logado
        menu = ["Login", "Cadastro"]
        escolha = st.sidebar.selectbox("Menu", menu)

        if escolha == "Login":
            st.subheader("Login")

            cpf = st.text_input("CPF")
            senha = st.text_input("Senha", type='password')

            login_button = st.button("Entrar (Clique duas Vezes para Confirmar)")

            if login_button:
                if autenticar_usuario(cpf, senha):
                    st.session_state['logged_in'] = True
                    st.session_state['cpf'] = cpf
                    st.success(f"Bem-vindo(a), usuário de CPF {cpf}!")
                else:
                    st.warning("CPF ou senha incorretos.")

        elif escolha == "Cadastro":
            cadastro_usuario()

def cadastro_usuario():
    st.subheader("Cadastro de Novo Usuário")

    cpf = st.text_input("CPF")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    celular = st.text_input("Celular")
    senha = st.text_input("Senha", type='password')
    idade = st.number_input("Idade", min_value=0, value=0)
    peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f", value=0.0)
    sexo = st.selectbox("Sexo", ["M", "F", "Outro"])

    if st.button("Cadastrar"):
        cadastrar_usuario(cpf, nome, email, celular, senha, idade, peso, sexo)
        st.success("Usuário cadastrado com sucesso! Você já pode fazer login.")

def adicionar_alimentacao(cpf):
    st.subheader("Adicionar Alimentação")

    tipo_refeicao = st.selectbox("Tipo de Refeição", ["Almoço", "Jantar"])
    data_refeicao = st.date_input("Data", date.today())

    alimentos = obter_alimentos()
    alimentos_dict = {f"{nome} ({float(calorias)} kcal)": (id_alimento, float(calorias))
                      for id_alimento, nome, calorias in alimentos}

    alimentos_selecionados = st.multiselect("Selecione os alimentos", list(alimentos_dict.keys()))
    proporcoes = {}
    for alimento in alimentos_selecionados:
        proporcao = st.number_input(f"Proporção para {alimento} (em porções)",
                                    min_value=0.0, step=0.1)
        id_alimento = alimentos_dict[alimento][0]
        proporcoes[id_alimento] = proporcao

    if st.button("Registrar Refeição"):
        registrar_refeicao(cpf, tipo_refeicao, data_refeicao, proporcoes)
        total_calorias = calcular_calorias(proporcoes)
        st.success(f"Refeição registrada! Calorias totais: {total_calorias:.2f} kcal")

def ver_historico(cpf):
    st.subheader("Histórico de Alimentação")

    data_refeicao = st.date_input("Selecione a data")
    tipo_refeicao = st.selectbox("Tipo de Refeição", ["Almoço", "Jantar"])

    if st.button("Ver Histórico"):
        historico = obter_historico_refeicoes(cpf, tipo_refeicao, data_refeicao)
        if historico:
            st.write(f"Histórico de {tipo_refeicao} em {data_refeicao.strftime('%d/%m/%Y')}:")
            total_calorias = 0
            for alimento, calorias, proporcao in historico:
                calorias_totais = float(calorias) * float(proporcao)
                total_calorias += calorias_totais
                st.write(f"- {alimento}: {proporcao} porções, {calorias_totais:.2f} kcal")
            st.write(f"**Total de calorias ingeridas:** {total_calorias:.2f} kcal")
        else:
            st.info("Nenhum registro encontrado para esta data e refeição.")

def gerenciar_alimentos():
    st.subheader("Adicionar Alimentos")

    nome_alimento = st.text_input("Nome do Alimento")
    calorias_por_porcao = st.number_input("Calorias por Porção", min_value=0.0, step=0.1)

    if st.button("Adicionar Alimento"):
        adicionar_alimento(nome_alimento, calorias_por_porcao)
        st.success("Alimento adicionado com sucesso!")

def gerenciar_conta(cpf):
    st.subheader("Gerenciar Conta")

    dados_usuario = obter_dados_usuario(cpf)
    if dados_usuario:
        nome, email, celular, idade, peso, sexo = dados_usuario

        novo_nome = st.text_input("Nome", value=nome)
        novo_email = st.text_input("Email", value=email)
        novo_celular = st.text_input("Celular", value=celular)
        nova_senha = st.text_input("Senha", type='password')
        nova_idade = st.number_input("Idade", min_value=0, value=int(idade))
        novo_peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f", value=float(peso))
        novo_sexo = st.selectbox("Sexo", ["M", "F", "Outro"],
                                 index=["M", "F", "Outro"].index(sexo))

        if st.button("Atualizar Dados"):
            atualizar_dados_usuario(cpf, novo_nome, novo_email, novo_celular,
                                    nova_senha, nova_idade, novo_peso, novo_sexo)
            st.success("Dados atualizados com sucesso!")

        if st.button("Excluir Conta"):
            excluir_usuario(cpf)
            st.warning("Sua conta foi excluída.")
            st.session_state['logged_in'] = False
            st.session_state['cpf'] = ''
    else:
        st.error("Usuário não encontrado.")

if __name__ == '__main__':
    main()
