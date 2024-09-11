import streamlit as st
import pandas as pd
from upload_actors_page import extract_performances_from_excel, extract_actors_from_excel
from actors_db_helper import get_joined_data, insert_performances_in_bulk

def main():

    uploaded_file = st.file_uploader("Subir archivo Excel con las funciones y actores", type=["xls", "xlsx"])

    if uploaded_file:

        performances_df = extract_performances_from_excel(uploaded_file)
        
        if not performances_df.empty:

            insert_performances_in_bulk(performances_df)


            performances_dict = {index + 1: row['Name_Performances'] for index, row in performances_df.iterrows()}
            performances_ids = list(performances_dict.keys())

            st.write("Detalles de las funciones:")
            st.dataframe(performances_df)

            if st.button("Guardar actores"):
                extract_actors_from_excel(uploaded_file, performances_dict)
        else:
            st.write("No se encontraron funciones en el archivo Excel.")


        joined_data = get_joined_data()
        if joined_data:
            joined_df = pd.DataFrame(joined_data, columns=[
                'FullName', 'Code', 'Phone_Number', 'Email', 
                'Performances_Date', 'Performances_Hour', 'Name_Performances', 'Performances_Price'
            ])
            st.write("Datos combinados de Funciones y Actores:")
            st.dataframe(joined_df)
    else:
        st.write("Por favor sube un archivo Excel.")

if __name__ == "__main__":
    main()
