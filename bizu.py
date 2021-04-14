import pandas as pd
from PIL import Image
import numpy as np
import streamlit as st

niveis = ['','Ensino fundamental','Ensino Médio e Pré-vestibular','Concurso']
materias = ['','Matemática','Física','Química','Inglês','Redação']

dict_materias = {
    'Matemática':'mat',
    'Física':'fis',
    'Química':'quim',
    'Inglês':'ing',
    'Redação':'red'
}

dict_niveis = {
    'Ensino fundamental':'ef',
    'Ensino Médio e Pré-vestibular':'em',
    'Concurso':'con'
}

# Ler base
url = 'https://github.com/soilmo/Bizu/raw/main/profs.csv?raw=true'
df = pd.read_csv(url, encoding='utf-8')

#image = Image.open("https://github.com/soilmo/Bizu/blob/main/bizu_logo_pq_trans.png")
#st.sidebar.image(image,use_column_width=True,  width= 20, )

st.title("Bizu Aulas Particulares")

st.markdown("Confira os professores cadastrados e agende sua aula :smile:")

nivel = st.selectbox("Nível da aula",niveis)

# Matéria
materia = st.selectbox('Disciplina', materias)

# Tipo de aula
tipo = st.selectbox("Presencial ou online?",['','Presencial','Online'])

# Se presencial, cidade?
if tipo == "Presencial":
    cidade = st.selectbox("Em qual cidade quer ter aula?", list(df['cidade'].unique()))
    filtro = df['cidade'] == cidade
    df = df[filtro]

# Genero do prof
genero = st.selectbox("Preferência pelo gênero do professor?", ['', 'Tanto faz', 'Mulher', 'Homem'])

flag = 0
#(nivel != '' and materia != '' and tipo == "Presencial" and cidade != '' and genero != '')
if  (nivel != '' and materia != '' and tipo != "" and genero != ''):

    # Filtro tipo
    if tipo == 'Presencial':
        filtro = df['presencial']=="Sim"
        df = df[filtro]
    else:
        filtro = df['online']=="Sim"
        df = df[filtro]
    # Filtro genero
    if genero == 'Mulher':
        filtro = df['genero']=="Feminino"
        df = df[filtro]
    elif genero == 'Homem':
        filtro = df['genero']=="Masculino"
        df = df[filtro]
    
    # Nivel_materia
    filtro = df[dict_niveis[nivel]+"_"+dict_materias[materia]]==1
    df = df[filtro]
    
    if genero == 'Mulher' and df.shape[0] > 0:
        st.header("Total de "+str(df.shape[0])+" professoras nesse perfil :smile:")
        st.subheader("Marque a caixinha para ver o perfil completo do Professor")
    elif genero == 'Mulher' and df.shape[0] == 1:
        st.header("Total de "+str(df.shape[0])+" professora nesse perfil :smile:")
    elif (genero == 'Homem' or genero == "Tanto faz") and df.shape[0] == 1:
        st.header("Total de "+str(df.shape[0])+" professor nesse perfil :smile:")
        st.subheader("Marque a caixinha para ver o perfil completo do Professor")
    elif (genero == 'Homem' or genero == "Tanto faz") and df.shape[0] > 0:
        st.header("Total de "+str(df.shape[0])+" professores nesse perfil :smile:")
        st.subheader("Marque a caixinha para ver o perfil completo do Professor")
    elif df.shape[0]==0:
        st.header("Ainda não temos nenhum professor nesse perfil")

    # Ordenar pelo valor
    if tipo == 'Presencial' and df.shape[0] > 0:
        df = df.sort_values(by = ['valor_presencial_'+str(dict_niveis[nivel]),'idade'], ascending = True)
        #maximo = st.slider('Faixa de preço da aula presencial. Mova o intervalo para filtrar os professores.', min_value=0, max_value=int(df['valor_presencial_'+str(dict_niveis[nivel])].max()),step=5)
        #maximo=int(df['valor_presencial_'+str(dict_niveis[nivel])].max()
        #filtro = df['valor_presencial_'+str(dict_niveis[nivel])]<=maximo
        #df = df[filtro]
        flag = 1
    elif tipo == "Online" and df.shape[0] > 0:
        df = df.sort_values(by = ['valor_online_'+dict_niveis[nivel],'idade'], ascending = True)
        #maximo = st.slider('Faixa de preço da aula online. Mova o intervalo para filtrar os professores.', min_value=0, max_value=int(df['valor_online_'+str(dict_niveis[nivel])].max()), step =5)
        #filtro = df['valor_online_'+str(dict_niveis[nivel])]<=maximo
        #df = df[filtro]
        flag = 1

    if df.shape[0]>0:

        for i in range(df.shape[0]):
            
            nome = df['nome'].iloc[i]
            titulo = df['titulo'].iloc[i]
            metodologia = df['metodologia'].iloc[i]
            motivacao = df['motivacao'].iloc[i]
            curriculo = df['curriculo'].iloc[i]
            link_zap = df['link_zap'].iloc[i]
            idade = df['idade'].iloc[i]

            if tipo == 'Presencial':
                valor = df['valor_presencial_'+str(dict_niveis[nivel])].iloc[i]
            elif tipo == "Online":
                valor = df['valor_online_'+str(dict_niveis[nivel])].iloc[i]

            
            if st.checkbox(str(nome) +" - R$ "+ str(valor) + "/hora"):
                st.markdown("*Titulo: *" + str(titulo))
                st.markdown("*Metodologia: *" + str(metodologia))
                st.markdown("*Motivação: *" + str(motivacao))
                st.markdown("*Currículo: *" + str(curriculo))
                st.markdown("*Idade: *" + str(idade))
                t = '*Mandar mensagem no Whatsapp de ' +str(nome.split(" ")[0])+ '*'
                link = f'[{t}]({link_zap})'
                st.markdown(link, unsafe_allow_html=True)
    elif flag == 1:
        st.markdown("Nenhum professor nessa faixa de valores :(")
            
else:
    st.header("Aguardando o preenchimento das preferências para mostrar os resultados :smile:")