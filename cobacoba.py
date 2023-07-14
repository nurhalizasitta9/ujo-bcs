import streamlit as st
import math

st.write("""
# Aplikasi Uang Jalan Operasional
## Selamat Datang!
Ini adalah aplikasi menghitung uang jalan operasional PT. Buana Centra Swakarsa 

note: angka ribuan ditulis tanpa titik dan angka desimal ditulis dengan titik
""")

tgl = st.date_input('Tanggal Keberangkatan')
jam = st.time_input('Jam keberangkatan')
unit = ['Trailer','Tronton']
option = st.selectbox('Pilih unit: ',unit)
origin = st.text_input('Origin: ')
destination = st.text_input('Destination: ')

jarak = st.number_input('Masukkan jarak: ')
adj_jarak = math.ceil((5/100 * jarak) + jarak)

if adj_jarak <= 400:
    KPJ = 35 #km/jam
elif adj_jarak > 400:
    KPJ = 50 #km/jam

tol = st.number_input('Biaya tol: ')
penyebrangan = st.number_input('Biaya penyebrangan: ')
komisi = st.number_input('Komisi: ')
helper = st.number_input('Biaya helper: ')

solar = 6800 #per liter
LooL = 2 #jam
waktu_tempuh = (adj_jarak/KPJ) + LooL

tph = math.floor(24/waktu_tempuh) #trip per hari

hpt = waktu_tempuh/16
if hpt <= 0.35:
    hpt = 0.35
elif hpt > 0.35:
    hpt = waktu_tempuh/16

hari = waktu_tempuh/8
if hari <= 0.35:
    hari = 0.35
elif hari > 0.35:
    hari = waktu_tempuh/8


uang_makan = hari * 120000
st.write(f'uang makan: Rp. {uang_makan}')
retribusi = math.ceil(hari * 75000)

ritase = hari * 100000

kehadiran = math.ceil(hari * 10000)


if option == 'Trailer':
    fuel = 2.25
    bongkarmuat = 90000
elif option == 'Tronton':
    fuel = 2.7
    bongkarmuat = 70000


bbm = adj_jarak/fuel
st.write(f'bbm: {math.ceil(bbm)}')
uang_bbm = bbm * solar
st.write(f'uang bbm: Rp. {math.ceil(uang_bbm)}')

hitung = st.button('Hitung UJO')
if hitung:
    total = uang_bbm + tol + bongkarmuat + uang_makan + retribusi + ritase + kehadiran + komisi + helper + penyebrangan
    st.success(f'Jadi, total uang jalan operasional yang dibutuhkan adalah Rp. {math.ceil(total)}.')