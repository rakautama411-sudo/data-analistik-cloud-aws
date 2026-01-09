import boto3
import pandas as pd

logging.basicConfig(
    filename = 'analistik.log',
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)'
)

logging.info('aplikasi analistik dijalankan')

s3 = boto3.client('s3')
bucket = 'data-analistik-urlz'
file = 'anilisis_valid.xlsx'

s3.download_file(bucket, file, 'analisis_valid.xlsx')

df = pd.read_excel('analisis_valid.xlsx')
df['total'] = df['sales_amount'] * df['unit_price']

print("Data berhasil diproses:")
print(df.head())