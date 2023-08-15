import openpyxl
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import tkinter
import numpy as np
import seaborn as sns
sns.set_theme(style="darkgrid")

st.set_page_config(page_title="Defect Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

fkonzept = st.file_uploader("Upload a file", type=["csv", "xlsx", "txt"])
if fkonzept:
    wb = openpyxl.load_workbook(fkonzept, read_only=True)
    st.info(f"File uploaded: {fkonzept.name}")
    st.info(f"Sheet names: {wb.sheetnames}")

    df= pd.read_excel(io=fkonzept ,
        engine='openpyxl',
        sheet_name='Defect Data',
        skiprows=0,
        usecols='A:U',
        nrows=57,
    )
    # print(df)
    # st.dataframe(df) #to display the table without filter

    # --sidebar---
    st.sidebar.header("Please Filter here:")
    complexity= st.sidebar.multiselect(
        "Select the Complexity",
        options=df["complexity"].unique(),
        default=df["complexity"].unique()
    )

    criticality= st.sidebar.multiselect(
        "Select the Criticality",
        options=df["criticality"].unique(),
        default=df["criticality"].unique()
    )

    development_methodology= st.sidebar.multiselect(
        "Select the development methodology",
        options=df["development_methodology"].unique(),
        default=df["development_methodology"].unique()
    )

    type_of_requirement= st.sidebar.multiselect(
        "Select the type of requirement",
        options=df["type_of_requirement"].unique(),
        default=df["type_of_requirement"].unique()
    )

    df_selection=df.query(
        "complexity== @complexity & criticality == @criticality & development_methodology == @development_methodology & type_of_requirement == @type_of_requirement"
    )

    # st.dataframe(df_selection) #to display the table based on filters

    #--mainpage--
    st.title(":bar_chart: Defect Dashboard")
    st.markdown("##")

    #top KPI's
    # total no_of_requirements
    # average documentation_quality
    # total unit_test_defects
    # average build_quality

    total_no_of_requirements= int(df_selection["no_of_requirements"].sum())
    average_documentation_quality=round(df_selection["documentation_quality"].mean(), 1)
    star_documentation_quality= ":star:"*int(round(average_documentation_quality,0))
    total_unit_test_defects= int(df_selection["unit_test_defects"].sum())
    average_build_quality=round(df_selection["build_quality"].mean(),1)
    star_build_quality= ":star:"*int(round(average_build_quality,0))

    column1, column2, column3, column4 =st.columns(4)
    with column1:
        st.subheader("Total Number of Requirements")
        st.subheader(f"{total_no_of_requirements}")
    with column2:
        st.subheader("Average Documentation Qality")
        st.subheader(f"{average_documentation_quality}  {star_documentation_quality}")
    with column3:
        st.subheader("Total Number of Unit Test Defects")
        st.subheader(f"{total_unit_test_defects}")
    with column4:
        st.subheader("Average Build Quality")
        st.subheader(f"{average_build_quality}  {star_build_quality}")

    st.markdown("---")
    # Line graph
    # x='complexity', y='no_of_defects'
    # x='no_of_requirements', y='no_of_defects'
    # 
    # 
    # 
    # plt.scatter(x='complexity', y='no_of_defects')
    # temp=plt.show()
    # st.temp
    # test- ##This shows a bar graph on the screen- working 
    # arr = np.random.normal(1, 1, size=100)
    # fig, ax = plt.subplots()
    # ax.hist(arr, bins=20)
    # st.pyplot(fig)

    # tips = sns.load_dataset("tips")
    # sns.relplot(data=df,kind="scatter", x="complexity", y="no_of_defects")
    # fig, ax = plt.subplots()
    # st.pyplot(fig)

    fig= px.bar(df_selection, x="no_of_defects", y="complexity")
    st.plotly_chart(fig)

    fig2= px.bar(df_selection, x="no_of_defects", y="no_of_requirements") #px.scatter for scatterplot
    
    st.plotly_chart(fig2)
# Bar plot for 1rs graph, filter for each column in the excel
else: exit
