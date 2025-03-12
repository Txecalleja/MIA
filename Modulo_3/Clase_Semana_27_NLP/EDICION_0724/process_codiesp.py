import openai
import os
from os.path import join
import pandas as pd

api_key = ''

def ask_custom_assistant(prompt):
    try:

        client = openai.OpenAI(api_key=api_key)

        # Create a new thread
        my_thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
                thread_id=my_thread.id,
                role="user",
                content=prompt
                )

        run = client.beta.threads.runs.create_and_poll(
                thread_id=my_thread.id,
                assistant_id='asst_7SV0nwg1t0xe3DX8P5T04ciE',
                )

        while run.status != 'completed':
            os.wait(1)

        messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
                )

        text = messages.data[0].content[0].text.value

        return text


    except Exception as e:
        return f"Error: {e}"


dir_codiesp = '/Users/jsilva/repositories/MIA/Modulo_3/Clase_Semana_27_NLP/final_dataset_v4_to_publish/train/text_files'
list_files = os.listdir(dir_codiesp)

df = pd.DataFrame(columns = ['Archivo','Término clínico','Tipo',' Código'])

for file_ in list_files [0:3]:

    file_path = join(dir_codiesp,file_)

    with (open(file_path, "r", encoding="utf-8") as text_file):

        text = text_file.read()

        respuesta = ask_custom_assistant(text)
        filas = respuesta.split('\n')

        for fila_ in filas [2:]:
            terminos_ = fila_.split('|')
            df = pd.concat([df, pd.DataFrame({'Archivo':[file_], 'Término clínico': [terminos_[0]], 'Tipo': [terminos_[1]], 'Código':[terminos_[2]]})],ignore_index=True)

    print(df)

df.to_csv('example.csv')