import pandas as pd
import streamlit as st
from actors_db_helper import insert_actors_in_bulk


def extract_performances_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file, sheet_name="Funciones")
        st.write("Funciones teatrales cargadas correctamente.")
    except Exception as e:
        st.write(f"Error al leer el archivo Excel (Hoja Funciones): {e}")
        return pd.DataFrame()

    df = df.rename(columns={
        'Fecha de la Función': 'Performances_Date',
        'Hora de la Función': 'Performances_Hour',
        'Nombre de la Obra': 'Name_Performances',
        'Pago al Actor': 'Performances_Price' 
    })

    df['Performances_Hour'] = df['Performances_Hour'].astype(str)
    
    return df


def extract_actors_from_excel(excel_file, performances_dict):
    try:
        df = pd.read_excel(excel_file, sheet_name="Actores")
        st.write("Datos de actores cargados correctamente.")
    except Exception as e:
        st.write(f"Error al leer el archivo Excel (Hoja Actores): {e}")
        return pd.DataFrame()  

    df = df.rename(columns={
        'Nombre': 'first_name',
        'Apellido': 'last_name',
        'cedula': 'Code',
        'Numero_telefono': 'Phone_Number',
        'Correo_Electronico': 'Email',
        'Nombre de la Obra': 'Name_Performances'
    })


    df['FullName'] = df['first_name'] + ' ' + df['last_name']

    required_columns = ['FullName', 'Code', 'Phone_Number', 'Email', 'Name_Performances']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.write(f"Error: Las siguientes columnas faltan en el archivo de actores: {', '.join(missing_columns)}")
        return pd.DataFrame()  

    df = df[required_columns]

    for index, row in df.iterrows():
        performance_name = row['Name_Performances']
        performance_id = None

        for perf_id, perf_name in performances_dict.items():
            if performance_name == perf_name:
                performance_id = perf_id
                break

        if performance_id:
            actor_data = row[['FullName', 'Code', 'Phone_Number', 'Email']].to_frame().T
            insert_actors_in_bulk(actor_data, performance_id, table_name='actors')
        else:
            st.write(f"Error: No se encontró el performance_id para la obra {performance_name}")

    st.write("Actores procesados correctamente.")
    st.write(df)
