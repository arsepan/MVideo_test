import streamlit as st
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache_data
def df_load(filename):
    return pd.read_csv(filename, index_col=0)

@st.cache_data
def add_data(value_1, value_2, value_3, df):
       new_df = {'Количество больничных дней': value_1, 'Возраст': value_2, 'Пол': value_3}
       df = df.append(new_df, ignore_index=True)
       return df

df_file = st.file_uploader('Загрузить CSV файл', type='csv')
if df_file:

    df = df_load(df_file)

    with st.sidebar:
        st.header('Ввод параметров')
        wd_number = st.text_input('Количество рабочих дней', '')
        age = st.text_input('Возраст', '')
        sex = st.text_input('Пол', '')
    st.write('**Указанные значения**')
    st.write('Количество рабочих дней:', wd_number)
    st.write('Возраст:', age)
    st.write('Пол', sex)
    if st.button('Ввести данные'):
        df = add_data(wd_number, age, sex, df)
        st.header("Загруженные данные:")
        st.table(df.tail())
        st.dataframe(df.describe())
    else:
        st.header("Загруженные данные:")
        st.table(df.tail())
        st.dataframe(df.describe())

    if st.button('Проверить гипотезы'):
        df.loc[df['Возраст'] > 35, 'Возрастная группа'] = 'Старше 35 лет'
        df.loc[df['Возраст'] <= 35, 'Возрастная группа'] = 'Младше 35 лет' 

        st.header('Проверка гипотез')
        st.subheader('Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.')

        men = df.loc[(df['Пол'] == 'М') & (df['Количество больничных дней'] > 2), 'Количество больничных дней']
        women = df.loc[(df['Пол'] == 'Ж') & (df['Количество больничных дней'] > 2), 'Количество больничных дней']

        ax = sns.histplot(men, label = 'М', stat='probability', kde=True, bins = np.arange(3, 9))
        sns.histplot(women, label = 'Ж', stat='probability', kde=True, bins = np.arange(3, 9), ax = ax)
        plt.legend()
        plt.title('Вероятность количества пропущенных дней Мужчин и Женщин')
        st.pyplot()
        
        result = stats.ttest_ind(men, women, equal_var = False)
        pvalue = result.pvalue/2
        alpha = .05

        st.write(f'p-value: {pvalue * 2}')
        st.write(f't-statistics: {result[0]}')

        if (pvalue < alpha) and (men.count() > women.count()):
            st.write('**Вывод**: Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин')
        else:
            st.write('**Вывод**: Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни также или реже женщин')


        st.subheader('Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.')
        old = df.loc[(df['Возрастная группа'] == 'Старше 35 лет') & (df['Количество больничных дней'] > 2), 'Количество больничных дней']
        yng = df.loc[(df['Возрастная группа'] == 'Младше 35 лет') & (df['Количество больничных дней'] > 2), 'Количество больничных дней']

        ax = sns.histplot(old, label = 'Older', stat='probability', kde=True, bins = np.arange(3, 9))
        sns.histplot(yng, label = 'Ynger', stat='probability', kde=True, bins = np.arange(3, 9), ax = ax)
        plt.legend()
        plt.title('Вероятность количества пропущенных дней')
        st.pyplot()

        result = stats.ttest_ind(old, yng, equal_var = False, alternative='greater')
        pvalue = result.pvalue / 2
        alpha = .05

        st.write(f'p-value: {pvalue * 2}')
        st.write(f't-statistics: {result[0]}')

        if (pvalue < alpha):
            st.write('**Вывод**: Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.')
        else:
            st.write('**Вывод**: Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни также или реже своих более молодых коллег')