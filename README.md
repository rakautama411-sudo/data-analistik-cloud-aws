# Aplikasi Data Analitik Sederhana Berbasis Cloud

Proyek ini merupakan implementasi aplikasi data analitik sederhana
menggunakan layanan Amazon Web Services (AWS).

## Teknologi yang Digunakan
- Amazon EC2
- Amazon S3
- Amazon CloudWatch
- Python (pandas, boto3)

## Fitur
- Mengambil data dari Amazon S3
- Analisis data sederhana (total penjualan)
- Monitoring sistem menggunakan CloudWatch
- Logging aplikasi

## Cara Menjalankan
1. Jalankan instance EC2
2. Install dependency:
   pip install -r requirements.txt
3. Jalankan aplikasi:
   python analistik.py

## Arsitektur Cloud
Lihat folder `diagram/`

## Monitoring
Monitoring dilakukan menggunakan Amazon CloudWatch Logs dan EC2 Monitoring.
