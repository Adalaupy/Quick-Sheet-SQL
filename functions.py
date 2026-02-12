import pandas as pd
import streamlit as st


readers = {
    'csv' : pd.read_csv,
    'xlsx': pd.read_excel,
    'xls' : pd.read_excel,
    'parquet' : pd.read_parquet,
}    


def Fn_Save_df_To_List(df, save_name, save_path = ''):
    
    this_data = {"Path" : save_path , "Name":  save_name , "data": df }

    Full_Data_List = st.session_state['data']

    # Remove the previous one with the same table name
    Full_Data_List = [item for item in Full_Data_List if item['Name'] != save_name]
    Full_Data_List.append(this_data)

    st.session_state['data'] = Full_Data_List


def Fn_Each_Data(ext, name, path , save_path, sheet = None):
    
    if sheet:
        
        df =  readers[ext](path, sheet )
        name = f"{name}_{sheet}"
   
    else:
        
        df =  readers[ext](path)

    save_name = name.replace(' ', '_')

    Fn_Save_df_To_List(df, save_name, save_path)



# Type: 1=Search, 2=Upload
def Fn_Read_Data(path, name, type):
        
    if type == 1:
        
        ext = path.split('.')[-1]
        save_path = path

    else:
        
        ext = path.name.split('.')[-1]
        save_path = ''


    if ext in ['xlsx', 'xls']:
        
        sheets = pd.ExcelFile(path).sheet_names

        if len(sheets) == 1:
            
            Fn_Each_Data(ext, name, path, save_path)
            
        else:
            
            for sheet in sheets:
                
                Fn_Each_Data(ext, name, path, save_path , sheet = sheet)

    else :
        
        Fn_Each_Data(ext, name, path, save_path)