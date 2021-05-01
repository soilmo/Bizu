import pandas as pd
import numpy as np
import streamlit as st
import streamlit_analytics
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email(data, aluno, contato, nivel,materia,tipo, cidade, genero, nome):
    
    mail_content = "<br><b>Data</b>: " +data+"<br><b>Aluno</b>: " +aluno  +"<br><b>contato</b>: " +contato  +"<br><b>Nivel</b>: " +nivel +"<br><b>Materia</b>: " +materia + "<br><b>Tipo:</b> " +tipo+ "<br><b>Cidade:</b> " +cidade + "<br><b>Genero:</b> " + genero + "<br><b>Nome:</b> " +nome
    
    #The mail addresses and password
    sender_address = 'bizuaulasparticulares@gmail.com'
    sender_pass = '291096santiago'
    receiver_address = 'bizuaulasparticulares@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message.IsBodyHtml = True
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ACESSO | ' + data + " | " + nome   #The subject line
    #The body and the attachments for the mail
    #message.Body = mail_content
    message.attach(MIMEText(mail_content, 'html'))
    #message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

# Busca
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def filtro_busca(df, nivel,materia,tipo, genero):
    
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

    return df


#streamlit_analytics.start_tracking()

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

# Mudar título
st.set_page_config(page_title = "Bizu", page_icon=":nerd_face:")

# Esconder menu canto superior direito
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Carregar Logo
#st.image("https://github.com/soilmo/Bizu/blob/main/bizu_logo_pq_trans.png",width=400)
st.title("Bizu Aulas Particulares")

st.markdown("Confira os professores cadastrados e agende sua aula :smile:")

t = '*Dúvidas? Clique aqui para falar com a gente*'
link_bizu = 'https://api.whatsapp.com/send?phone=5585999408919&text=Oi%20Bizu%2C%20estou%20com%20d%C3%BAvidas.%20Pode%20me%20ajudar%3F'
st.markdown(f'[{t}]({link_bizu})', unsafe_allow_html=True)

# Contato
contato = st.text_input("Qual seu contato? E-mail, Whatsapp ou Instagram. É opcional.", "")

if contato=="":
    st.warning("Para receber avisos, dicas e promoções exclusivas, recomenda-se indicar algum contato :grimacing:")
else:
    st.success("Boa! Entraremos em contato para te informar as formas que a Bizu pode te ajudar :smile:")

# Nome solicitante
aluno = st.text_input("Qual seu nome?", "")
if aluno == "":
    st.warning("Preencha seu nome para prosseguir :pray:")
else:

    # Escolher preferencias --------------------------------

    # Nivel
    nivel = st.selectbox("Nível da aula",niveis)
    # Matéria
    materia = st.selectbox('Disciplina', materias)
    # Tipo de aula
    tipo = st.selectbox("Presencial ou online?",['','Presencial','Online'])
    # Se presencial, cidade?
    cidade = "NA"
    if tipo == "Presencial":
        cidade = st.selectbox("Em qual cidade quer ter aula?", list(df['cidade'].unique()))
        filtro = df['cidade'] == cidade
        df = df[filtro]
    # Genero do prof
    genero = st.selectbox("Preferência pelo gênero do professor?", ['', 'Tanto faz', 'Mulher', 'Homem'])
    # -------------------------------------------

    flag = 0
    if  (nivel != '' and materia != '' and tipo != "" and genero != ''):
        
        df = filtro_busca(df, nivel,materia,tipo, genero)
        
        if genero == 'Mulher' and df.shape[0] > 0:
            st.markdown("Total de "+str(df.shape[0])+" professoras nesse perfil :smile:")
        elif genero == 'Mulher' and df.shape[0] == 1:
            st.markdown("Total de "+str(df.shape[0])+" professora nesse perfil :smile:")
        elif (genero == 'Homem' or genero == "Tanto faz") and df.shape[0] == 1:
            st.markdown("Total de "+str(df.shape[0])+" professor nesse perfil :smile:")
        elif (genero == 'Homem' or genero == "Tanto faz") and df.shape[0] > 0:
            st.markdown("Total de "+str(df.shape[0])+" professores nesse perfil :smile:")
        elif df.shape[0]==0:
            st.markdown("Nenhum professor nesse perfil ainda :cry:")

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
            # Expand
            nome = st.selectbox("Professor",['Escolha o prof']+list(df['nome']))
            if nome != "Escolha o prof":

            #for i in range(df.shape[0]):
                filtro = df['nome']==nome

                titulo = df[filtro]['titulo'].iloc[0]
                metodologia = df[filtro]['metodologia'].iloc[0]
                motivacao = df[filtro]['motivacao'].iloc[0]
                curriculo = df[filtro]['curriculo'].iloc[0]
                link_zap = df[filtro]['link_zap'].iloc[0]
                idade = df[filtro]['idade'].iloc[0]

                if tipo == 'Presencial':
                    valor = df[filtro]['valor_presencial_'+str(dict_niveis[nivel])].iloc[0]
                elif tipo == "Online":
                    valor = df[filtro]['valor_online_'+str(dict_niveis[nivel])].iloc[0]

                #if st.checkbox(str(nome), False):
                st.markdown("__Valor hora aula:__ R$ " + str(valor))
                st.markdown("__Titulo:__ " + str(titulo))
                st.markdown("__Metodologia:__ " + str(metodologia))
                st.markdown("__Motivação:__ " + str(motivacao))
                st.markdown("__Currículo:__ " + str(curriculo))
                st.markdown("__Idade:__ " + str(idade))
                t = '*Mensagem no Zap de ' +str(nome.split(" ")[0])+ '*'
                link = f'[{t}]({link_zap})'
                st.markdown(link, unsafe_allow_html=True)
                
                # Enviar email
                date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                enviar_email(date_time,aluno, contato,nivel,materia,tipo, cidade, genero,str(nome))
                
        elif flag == 1:
            st.markdown("Nenhum professor nessa faixa de valores :cry:")

    else:
        st.markdown("Aguardando o preenchimento das preferências :sleeping:")

    #streamlit_analytics.stop_tracking(save_to_json="C:/Users/pedro/Dropbox/Bizu/metrics.json")
    #streamlit_analytics.stop_tracking()
