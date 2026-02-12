import pandas as pd
import streamlit as st
from pandasql import sqldf
import functions as fn
from code_editor import code_editor

st.set_page_config(layout="wide")


# =============================================================================================================
# Store data
# =============================================================================================================

if 'data' not in st.session_state:
    
    st.session_state['data'] = []

if 'sql_result' not in st.session_state:
    
    st.session_state['sql_result'] = []


if 'sql_input_name' not in st.session_state  :
    st.session_state['sql_input_name']= ''


if 'sql_query' not in st.session_state:
    st.session_state['sql_query']= ''



if 'result_path' not in st.session_state:
    st.session_state['result_path'] = 'demo_files'


# =============================================================================================================
# 1. Upload files and define save sql result path
# =============================================================================================================

st.title('Path to save sql result as csv')
csv_path = st.text_input('', value = st.session_state['result_path'])

if csv_path != st.session_state['result_path']:
    
    st.session_state['result_path'] = csv_path


split_window = st.columns(2)

# -------------------------------------------------------------------------------
# Method 1: Search file 
# -------------------------------------------------------------------------------

with split_window[0]:
    

    with st.form("search_form", clear_on_submit=True):
        
        st.header('Search File by Path')

        input_name = st.text_input('Name the Dataframe:' , key = "name_input")
        input_path = st.text_input("File path:", key = "path_input")


        btn_search = st.form_submit_button('Search')


        if btn_search:        

            fn.Fn_Read_Data(input_path , input_name , 1)

# -------------------------------------------------------------------------------
# Method 2: Upload files
# -------------------------------------------------------------------------------

with split_window[1]:

    with st.form("upload_form", clear_on_submit=True):

        st.header('Upload File')
 
        upload_name = st.text_input('Name the Dataframe:' , key = "name_input2")
        uploader = st.file_uploader("Choose a csv/xlsx file" , accept_multiple_files=True, key="uploader" )

        submitted = st.form_submit_button("Submit")
    
        if uploader and submitted: 
            
            for upload_path in uploader:
                
                if upload_name == "" or upload_name == None:                

                    aliasName = upload_path.name.split('.')[0]

                else:
                    
                    aliasName = upload_name

                fn.Fn_Read_Data(upload_path, aliasName, 2)




if len(st.session_state['data']) > 0:
    
    st.badge('<< Expand the sidebar and check the table list.', color = "yellow")


# =============================================================================================================
# Preview data in Sidebar
# =============================================================================================================

if len(st.session_state['data'] ) > 0:
    
    st.sidebar.header('Your Uploaded files:')


    fileList = [{"id": id , "Name": item['Name'], "IsPreview": False } for id,item in enumerate(st.session_state['data'])]
    df_fileList = pd.DataFrame(fileList)
    
    data_edit = st.sidebar.data_editor(df_fileList, hide_index=True )
    previous_id = data_edit.loc[data_edit['IsPreview'] == True]['id'].to_list()

    if len(previous_id) != 0:       
        
        preview_containter = st.sidebar.container(border=True)

        data_display = [item for id, item in enumerate( st.session_state['data']) if id in previous_id]

        for item in data_display:

            name = item['Name']
            data = item['data'].head(3)

            preview_containter.write(f'{name}: ')
            preview_containter.dataframe(data)


# =============================================================================================================
# Input SQL
# =============================================================================================================

if len(st.session_state['data'] ) > 0:

    sql_container = st.container(border=True)

    with sql_container:
        
        
        with st.form("submit_sql", border=False, clear_on_submit=True):

            st.subheader('SQL')

            st.write( 'Input your SQL (sqlite engine) query')


            if 'code_editor' in st.session_state and st.session_state['code_editor'] is not None:
                
                if 'text' in st.session_state['code_editor']:
                    
                    st.session_state['sql_query'] = st.session_state['code_editor']['text']

            code_editor(
                code = st.session_state['sql_query'],
                lang='sql',
                height=[10, 7000],
                allow_reset=True,
                response_mode=["debounce"],
                key = 'code_editor',
            )
                        
            cols = st.columns([10,1] , vertical_alignment='bottom')

            with cols[0]:
                
                input_tb_name = st.text_input('Table Name : **(Fill in to save this result to uploaded file list)**', value='')
            
            with cols[1]:                   

                submitted_sql = st.form_submit_button("Submit")

            
            
            if submitted_sql and st.session_state['sql_query'] != '':
                
                for tb in st.session_state['data']:
                    
                    globals()[tb['Name']] = tb['data']
                        
                
                try:
                    
                    resultdf = sqldf(st.session_state['sql_query'])
                    
                    st.session_state['sql_result'] = resultdf            
                
                except Exception as e:
                        
                    raise Exception(e)

                if input_tb_name != '':
                    
                    fn.Fn_Save_df_To_List(resultdf, input_tb_name, save_path = '')

                    st.rerun()


        if len(st.session_state['sql_result']) != 0:
            
            st.subheader('Result')

            st.dataframe(st.session_state['sql_result'])


# =============================================================================================================
# Download SQL query result if needed
# ============================================================================================================

if 'sql_result' in st.session_state and len(st.session_state['sql_result']) > 0:


    with st.form("download", clear_on_submit=True):

        split_down = st.columns(2, vertical_alignment='bottom')
        
        with split_down[0]:
            
            name_download = st.text_input('Download Data File Name:', key = 'input_download_name')


        with split_down[1]:
            
            btn_download = st.form_submit_button('Download Data')


        if btn_download:
            
            resultdf = st.session_state['result_path']

            final_result_path = resultdf + '\\' + name_download + '.csv' if resultdf !='' else name_download + '.csv'
            
            st.session_state['sql_result'].to_csv(final_result_path, index = False)

            st.write('Done !')

