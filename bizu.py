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
    'Inglês':'ingles',
    'Redação':'red'
}

dict_niveis = {
    'Ensino fundamental':'ef',
    'Ensino Médio e Pré-vestibular':'em',
    'Concurso':'con'
}

# Coluna do lado

#image = Image.open("https://github.com/soilmo/Bizu/blob/main/bizu_logo_pq_trans.png")
#st.sidebar.image(image,use_column_width=True,  width= 20, )

st.title("Bizu Aulas Particulares")

st.markdown("Confira os professores cadastrados e agende sua aula :smile:")

nivel = st.selectbox("Nível da aula",niveis)

# Matéria
materia = st.selectbox('Disciplina', materias)

# Tipo de aula
tipo = st.selectbox("Presencial ou online?",['','Presencial','Online'])

# Genero do prof
genero = st.selectbox("Preferência pelo gênero do professor?", ['', 'Tanto faz', 'Mulher', 'Homem'])

if nivel != '' and materia != '' and tipo != ''  and genero != '':
    
    # Ler base
    url = 'https://github.com/soilmo/Bizu/raw/main/profs.csv?raw=true'
    df = pd.read_csv(url, sep =';', encoding='latin-1')
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
    
    if genero == 'Mulher':
        st.header("Total de "+str(df.shape[0])+" professoras nesse perfil :smile:")
    else:
        st.header("Total de "+str(df.shape[0])+" professores nesse perfil :smile:")

    # Ordenar pelo valor
    if tipo == 'Presencial':
        df = df.sort_values(by = ['valor_presencial_'+dict_niveis[nivel],'idade'], ascending = True)
        maximo = st.slider('Faixa de preço da aula presencial. Mova o intervalo para filtrar os professores.', min_value=int(df['valor_presencial_'+dict_niveis[nivel]].min()), max_value=int(df['valor_presencial_'+dict_niveis[nivel]].max()))
        filtro = df['valor_presencial_'+dict_niveis[nivel]]<=maximo
        df = df[filtro]
    elif tipo == "Online":
        df = df.sort_values(by = ['valor_online_'+dict_niveis[nivel],'idade'], ascending = True)
        maximo = st.slider('Faixa de preço da aula online. Mova o intervalo para filtrar os professores.', min_value=int(df['valor_online_'+dict_niveis[nivel]].min()), max_value=int(df['valor_online_'+dict_niveis[nivel]].max()))
        filtro = df['valor_online_'+dict_niveis[nivel]]<=maximo
        df = df[filtro]

    # Filtro idade
    max_idade = st.slider('Faixa de idade. Mova o intervalo para filtrar os professores.', min_value=int(df['idade'].min()), max_value=int(df['idade'].max()))
    filtro = df['idade']<=max_idade
    df = df[filtro]

    for i in range(df.shape[0]):
        
        nome = df['nome'].iloc[i]
        titulo = df['titulo'].iloc[i]
        metodologia = df['metodologia'].iloc[i]
        motivacao = df['motivacao'].iloc[i]
        curriculo = df['curriculo'].iloc[i]
        link_zap = df['link_zap'].iloc[i]
        idade = df['idade'].iloc[i]

        if tipo == 'Presencial':
            valor = df['valor_presencial_'+dict_niveis[nivel]].iloc[i]
        elif tipo == "Online":
            valor = df['valor_online_'+dict_niveis[nivel]].iloc[i]

        st.subheader(str(nome) +" - R$ "+ str(valor) + "/hora")
        st.text(titulo)

        if st.checkbox("Ver perfil completo de " + str(nome)):
            st.markdown("*Metodologia:*\n" + str(metodologia))
            st.markdown("*Motivação:*\n" + str(motivacao))
            st.markdown("*Currículo:*\n" + str(curriculo))
            st.markdown("*Idade:*\n" + str(idade))
            t = '*Mandar mensagem no Whatsapp de ' +str(nome.split(" ")[0])+ '*'
            link = f'[{t}]({link_zap})'
            st.markdown(link, unsafe_allow_html=True)
            
else:
    st.header("Aguardando o preenchimento das preferências para mostrar os resultados :smile:")