import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")

def create_bypayment_type_df(df):
    bypayment_type_df = df.groupby(by="payment_type_y").order_id.nunique().reset_index()
    bypayment_type_df.rename(columns={"order_id": "payment_type_count"}, inplace=True)
    return bypayment_type_df

def create_grouped_df(df):
    df_grouped = df.groupby('order_id')['payment_value_y'].sum().reset_index()
    df_top_10 = df_grouped.sort_values(by='payment_value_y', ascending=False).head(10)
    return df_top_10

def create_filter_result_answer(df):
    df['days'] = df['result_answer'].dt.days
    byresult_answer_df = df.groupby(by="days").order_id.nunique().reset_index()
    byresult_answer_df.rename(columns={"order_id": "result_answer_count"}, inplace=True)
    filter_result_answer_df = byresult_answer_df[(byresult_answer_df["days"] >= 0) & (byresult_answer_df["days"] <= 7)]
    return filter_result_answer_df

# Memuat data yang telah dibersihkan
all_df = pd.read_csv("all_data.csv")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("../logo.png")

    option = st.sidebar.selectbox(
    'Please Select:',
    ('Home','Dataframe','Chart')
)

# Membuat dashboard
st.header("Sa'adah Dashboard")
st.markdown("<br>", unsafe_allow_html=True)  # untuk jarak

# Memanggil fungsi untuk mendapatkan DataFrame
bypayment_type_df = create_bypayment_type_df(all_df)

# Memanggil fungsi untuk mendapatkan df_top_10
df_top_10 = create_grouped_df(all_df)  # Pastikan df_top_10 didefinisikan

col1 = st.columns(1)[0]

with col1:
    colors = ['#973131', '#E0A75E', '#F9D689', '#F5E7B2']

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(
        y="payment_type_count",
        x="payment_type_y",
        data=bypayment_type_df.sort_values(by="payment_type_count", ascending=False),
        palette=colors
    )
    ax.set_title("Well-Known Payment Types", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    
    # Menampilkan plot di Streamlit
    st.pyplot(plt)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors_2 = ["#973131", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2", "#F5E7B2"]  # Memperbarui warna untuk memastikan konsistensi
    sns.barplot(
        x="payment_value_y",
        y="order_id",
        data=df_top_10.sort_values(by="payment_value_y", ascending=False),
        palette=colors_2
    )
    ax.set_title("Gift for Customers", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    
    st.pyplot(fig)
