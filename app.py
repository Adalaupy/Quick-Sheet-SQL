import pandas as pd
import streamlit as st
from pandasql import sqldf
import functions as fn
from code_editor import code_editor

st.set_page_config(layout="wide", page_title="Quick Sheet SQL", page_icon="💻")

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



# =============================================================================================================
# Upload files
# =============================================================================================================

with st.columns([1,2,1])[1]:
    
    with st.form("upload_form", clear_on_submit=True):

        st.header('Upload File')

        upload_name = st.text_input('Name the Dataframe:' , key = "name_input2")
        uploader = st.file_uploader("Choose a csv/xlsx file" , accept_multiple_files=True, key="uploader" )


        with st.columns([3,1,3])[-2]:
            
            submitted = st.form_submit_button("Submit")

            if uploader and submitted: 
                

                with st.spinner("Wait for it...", show_time=True):                    

                    for upload_path in uploader:
                        
                        if upload_name == "" or upload_name == None:                

                            aliasName = upload_path.name.split('.')[0]

                        else:
                            
                            aliasName = upload_name

                        fn.Fn_Read_Data(upload_path, aliasName, 2)



st.space()


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


            # Code Editor part
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



            cols = st.columns([5,3,2,1] , vertical_alignment='bottom')

            with cols[-3]:
                
                st.html('Table Name : <br>(Fill in and save this result to uploaded list)')
    

            with cols[-2]:
                
                input_tb_name = st.text_input('', value='')
            
            with cols[-1]:                   

                submitted_sql = st.form_submit_button("Submit")

            
            # After click submit
            if submitted_sql and st.session_state['sql_query'] != '':
                
                for tb in st.session_state['data']:
                    
                    # assign the tables into variable
                    globals()[tb['Name']] = tb['data']
                        
                
                try:
                    
                    resultdf = sqldf(st.session_state['sql_query'])
                    
                    st.session_state['sql_result'] = resultdf            
                
                except Exception as e:
                        
                    raise Exception(e)


                # Add this query result as table into the list
                if input_tb_name != '':
                    
                    fn.Fn_Save_df_To_List(resultdf, input_tb_name, save_path = '')

                    st.rerun()



        # Display the dataframe result
        if len(st.session_state['sql_result']) != 0:
            
            st.divider()

            st.subheader('Result')

            st.dataframe(st.session_state['sql_result'])



  
        # Download SQL query result if needed

        if 'sql_result' in st.session_state and len(st.session_state['sql_result']) > 0:

            split_down = st.columns([5,5,3,2], vertical_alignment='bottom')
            


            with split_down[-2]:
                
                name_download = st.text_input('', placeholder='File Name', key = 'input_download_name')


            with split_down[-1]:
                

                def Fn_handle_csv():
                                
                    file_csv  = st.session_state['sql_result'].to_csv().encode("utf-8")

                    return file_csv
                

                isDisable = name_download == ''

                st.download_button(
                    label="Download CSV",
                    data = Fn_handle_csv() ,
                    file_name=name_download + '.csv',
                    disabled = isDisable,
                    mime="text/csv",
                    icon=":material/download:",

                )
