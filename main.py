import os
import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO

from settings import *


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def main():

    df = pd.read_excel(os.path.join(os.getcwd(), 'data', 'something_table.xlsx'), sheet_name='Лист1')
    st.dataframe(df)

    selector_by_org = df['org'].unique()
    selector = st.multiselect('Выберите селект', selector_by_org, selector_by_org)
    indexes_founder = []
    for i, val in df.iterrows():
        if val['org'] not in selector:
            continue
        indexes_founder.append(i)
    new_df = df.iloc[indexes_founder]
    new_df = new_df.loc[:, ['name', 'something']]
    new_df = new_df.groupby(by='something').count().reset_index()
    st.dataframe(new_df)

    something_names = [val for val in new_df['something']]
    ratio_button = st.radio('Выберите', ('Убрать выборки', 'Выбрать все'))
    indexes = []
    if ratio_button == 'Выбрать все':
        selector = st.multiselect('Выберите селект', something_names, something_names)
        indexes = [idx for idx, val in enumerate(something_names) if val in selector]
    elif ratio_button == 'Убрать выборки':
        selector = st.multiselect('Выберите селект', something_names)
        indexes = [idx for idx, val in enumerate(something_names) if val in selector]

    new_df = new_df.iloc[indexes]
    fig = px.pie(data_frame=new_df, names='something', values='name')
    st.plotly_chart(fig)
    # df_xlsx = to_excel(test_df)
    # st.download_button(label='📥 Download Current Result',
    #                    data=df_xlsx,
    #                    file_name='df_test.xlsx',
    #                    mime="application/vnd.ms-excel")


if __name__ == '__main__':
    main()
