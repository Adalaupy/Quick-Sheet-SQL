# Table of contents

- [General Information](#general-information)
- [Features](#features)
- [Installation](#installation)
- [Run](#run)
- [Local Development Note](#local-development-note)
- [Remark](#remark)

# General Information

Streamlit web app for uploading CSV, Parquet, or Excel files, querying them with SQL (pandasql), saving results as named dataframes for further queries, and downloading results as CSV.

# Features

- Upload multiple files at once (CSV, .parquet, .xlsx/.xls)<br>
  <img src="/asset/image.png" width="500" alt="description">
- Auto-register uploaded files as queryable tables with preview function<br>
  <img src="/asset/image1.png" width="500" alt="description">
- Write and run SQL queries using pandasql (SQLite syntax) + Preview results<br>
  <img src="/asset/image2.png" width="800" alt="description">
- Save query results as persistent named dataframes in session state<br>
  <img src="/asset/image3.png" width="900" alt="description">  
- Download any result table as CSV<br>
  <img src="/asset/image4.png" width="600" alt="description">

  
# Installation

```
pip install -r requirements.txt
```

OR

```
python.exe -m pip install --upgrade pip
pip install streamlit
pip install openpyxl
pip install pandasql
pip install streamlit_code_editor
```

# Run

```
streamlit run app.py
```

# Local Development Note

When running locally, you can specify custom upload and download folders by editing the paths directly in `app_local.py`.

```
streamlit run app_local.py
```

# Remark

For Excel files with multiple worksheets, each sheet is registered as a separate table using this naming format:<br>
**{filename}\_{worksheet_name}**<br>
<br>
**Example:**<br>
File: sales_data.xlsx<br>
Sheets: Jan, Feb, Summary<br>
→ Tables become: sales_data_Jan, sales_data_Feb, sales_data_Summary




