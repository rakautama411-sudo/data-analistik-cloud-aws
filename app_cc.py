import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import boto3
from io import BytesIO

st.set_page_config(
    page_title="Aplikasi Data Analitik Penjualan",
    page_icon="📊",
    layout="wide"
)


BUCKET_NAME = "data-analistik-urlz"
FILE_NAME = "analisis_valid.xlsx"   # nama file di S3

s3 = boto3.client("s3")


@st.cache_data
def load_data_from_s3():
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    df = pd.read_excel(BytesIO(obj["Body"].read()))
    df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
    return df


st.title("📊 Aplikasi Data Analitik Penjualan Berbasis Cloud")
st.markdown(
    """
    Aplikasi ini berjalan pada **Amazon EC2**,  
    mengambil data dari **Amazon S3**,  
    dan dimonitor menggunakan **Amazon CloudWatch**.
    """
)


df = None

try:
    df = load_data_from_s3()
    st.success("✅ Data berhasil dimuat dari Amazon S3")
except Exception as e:
    st.error(f"Gagal mengambil data dari S3: {e}")
    st.stop()


st.sidebar.header("🔍 Filter Data")

region = st.sidebar.multiselect(
    "Pilih Region",
    options=df["Region"].dropna().unique(),
    default=df["Region"].dropna().unique()
)

category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=df["Product_Category"].dropna().unique(),
    default=df["Product_Category"].dropna().unique()
)

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=[
        df["Sale_Date"].min().date(),
        df["Sale_Date"].max().date()
    ]
)

df_filter = df[
    (df["Region"].isin(region)) &
    (df["Product_Category"].isin(category)) &
    (df["Sale_Date"].between(
        pd.to_datetime(date_range[0]),
        pd.to_datetime(date_range[1])
    ))
]


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penjualan", f"Rp {df_filter['Sales_Amount'].sum():,.0f}")
col2.metric("Total Unit Terjual", int(df_filter["Quantity_Sold"].sum()))
col3.metric("Rata-rata Diskon", f"{df_filter['Discount'].mean():.2f}%")
col4.metric("Jumlah Transaksi", len(df_filter))


st.subheader("📄 Data Penjualan")
st.dataframe(df_filter, use_container_width=True)


st.subheader("📈 Total Penjualan per Region")

region_sales = df_filter.groupby("Region")["Sales_Amount"].sum()

fig1, ax1 = plt.subplots()
region_sales.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Region")
ax1.set_ylabel("Total Penjualan")
ax1.set_title("Total Penjualan per Region")
plt.xticks(rotation=45)

st.pyplot(fig1)


st.subheader("📊 Total Penjualan per Kategori Produk")

category_sales = df_filter.groupby("Product_Category")["Sales_Amount"].sum()

fig2, ax2 = plt.subplots()
category_sales.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Kategori Produk")
ax2.set_ylabel("Total Penjualan")
ax2.set_title("Total Penjualan per Kategori Produk")
plt.xticks(rotation=45)

st.pyplot(fig2)


st.markdown("---")
st.caption(
    "📌 Data Analitik Sederhana | Amazon EC2 • Amazon S3 • CloudWatch • Streamlit"
)
