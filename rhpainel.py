import pandas as pd
import streamlit as st
from datetime import *
import db

uploaded_file = st.file_uploader("Buscar Arquivo",type=['xlsx','xls','csv','txt'])

if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    #st.write(file_details)

    df = st.cache(pd.read_excel)(uploaded_file, 'Resultados')

    is_check = st.sidebar.checkbox("Férias a vencer no período de 90 dias:")
    if is_check:
        st.title('Aviso Férias a Vencer')
        #a_vencer = pd.DatetimeIndex(df['DataLimite']).strftime('%d/%m/%Y')
        a_vencer = pd.DatetimeIndex(df['Inicio'])
        calcula_prazo = datetime.today() + timedelta(days=90)
        quantidade = 0
        for prazo in a_vencer:
            dias = abs((calcula_prazo - prazo).days)
            if(dias < 90):
                st.error("Férias com data limite para vencer em " + str((dias-90)*-1) + " dias na data de " + str(prazo.strftime('%d/%m/%Y')))
                quantidade = quantidade + 1;
        st.info("A quantidade de férias a vencer no periodo de 90 dias é de : " + str(quantidade) + " colaboradores de um total de " + str(a_vencer.size) + " agendadas.")

        st.title('Segunda Férias a Vencer')
        a_vencer = pd.DatetimeIndex(df['Inicio']).strftime('%m/%Y').value_counts()
        st.table(a_vencer)
        st.bar_chart(a_vencer)

    is_check = st.sidebar.checkbox("Planilha")

    if is_check:
        st.header('Informações da Planilha Selecionada')
        st.write(df)

        if st.button("Carregar planilha no Banco"):
            resposta = db.TransactionObject()
            linha = 0
            for linha in df.index.values:
                resposta.insert(df.values[linha][6], df.values[linha][7], df.values[linha][8], df.values[linha][9],
                                df.values[linha][10], df.values[linha][11], df.values[linha][12], df.values[linha][13])
                resposta = db.TransactionObject()

        # #pessoa = st.sidebar.multiselect("Escolha as pessoas", df['Colaborador'].unique())
        # aviso = st.multiselect("Escolha o periodo", pd.DatetimeIndex(df['Inicio']).strftime('%m/%Y').unique())
        #
        # dados = st.multiselect("Escolha os dados", df.columns)
        #
        # selected_pessoa = df[pd.DatetimeIndex(df['Inicio']).strftime('%m/%Y').isin(aviso)]
        # pessoa_data = selected_pessoa[dados]
        # pessoa_dados_is_check = st.checkbox("Exibir os dados das pessoas selecionados")
        # if pessoa_dados_is_check:
        #     st.info("No mês selecionado " + str(len(pessoa_data)) + " pessoas agendaram férias.")
        #     vencimento = date.today() + timedelta(days=90)
        #     st.write(pessoa_data)
        #
        #     st.write(selected_pessoa)

# if st.sidebar.checkbox('Banco'):
#     st.subheader('Informações no Banco')
#     resposta2 = db.TransactionObject()
#     st.table(resposta2.view())

    if (st.sidebar.checkbox("Férias por setor")):
        st.title('Férias por setor')
        por_setor = pd.Index(df['Setor']).value_counts()
        st.table(por_setor)
        st.bar_chart(por_setor)

    if (st.sidebar.checkbox("Férias por mês/ano")):
        st.title('Férias por mês/ano 30 dias')
        ferias = pd.DatetimeIndex(df['Inicio']).strftime('%m/%Y').value_counts()
        st.table(ferias)
        st.bar_chart(ferias)

        st.title('Férias por mês/ano Primeira Parte')
        ferias = pd.DatetimeIndex(df['Primeira Parte']).strftime('%m/%Y').value_counts()
        st.table(ferias)
        st.bar_chart(ferias)

        st.title('Férias por mês/ano Segunda Parte')
        ferias = pd.DatetimeIndex(df['Segunda Parte']).strftime('%m/%Y').value_counts()
        st.table(ferias)
        st.bar_chart(ferias)

if st.sidebar.checkbox('Banco'):
    st.header('Informações contidas no banco de dados:')
    con = db.TransactionObject()
    df = pd.read_sql_query("SELECT * from ferias", con.connection())
    st.write(df)
    con.connection().close()

    if st.sidebar.button("Limpar Registros"):
        limpar = db.TransactionObject()
        ret, msg = limpar.dropTable()
        if ret:
            st.success(msg)
        else:
            st.warning(msg)