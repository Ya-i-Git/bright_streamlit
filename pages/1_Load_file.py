import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

with st.sidebar:
    uploaded_files = st.file_uploader(
        label="Загрузить свой csv file",
        accept_multiple_files=False,
        type=['csv']
    )

if uploaded_files:
    df = pd.read_csv(uploaded_files)

    with st.sidebar:
        x_option = st.selectbox(
            'Выбери данные для оси X:',
            (df.columns)
        )

        y_option = st.selectbox(
            'Выбери данные для оси Y:',
            (df.columns)
        )
    
    fig, ax = plt.subplots(dpi=500)
    ax.plot(df[x_option], df[y_option])
    ax.set_xlabel(x_option)
    ax.set_ylabel(y_option)
    ax.set_title(f"{y_option} от {x_option}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    with st.sidebar:

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        st.write('__________')

        st.download_button(
            label=f"'{y_option}' - cкачать график 📉",
            data=buf,
            file_name="report.png",
            mime="image/png"
        )
else:
    st.info("Загрузите CSV файл через боковую панель.")