import streamlit as st
import pandas as pd
import math
from base64 import b64encode
from fpdf import FPDF

def creds_entered():
    if st.session_state['user'].strip() == 'bcslog' and st.session_state['passwd'].strip() == 'bdjaya':
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False
        if not st.session_state['passwd']:
            st.warning('Please enter password.')
        elif not st.session_state['user']:
            st.warning('Please enter username')
        else:
            st.error('Invalid Username/Password')

def authenticate_user():
        if 'authenticated' not in st.session_state:
            st.write('''
            ## Selamat Datang!
            Silahkan login terlebih dahulu.
            ''')
            st.text_input(label='Username', value="", key='user', on_change=creds_entered)
            st.text_input(label='Password', value="", key='passwd', type='password',on_change=creds_entered)
            st.button('Login')
            return False
        else:
            if st.session_state['authenticated']:
                return True
            else:
                st.write('''
                ## Selamat Datang!
                Silahkan login terlebih dahulu.
                ''')
                st.text_input(label='Username', value="", key='user', on_change=creds_entered)
                st.text_input(label='Password', value="", key='passwd', type='password',on_change=creds_entered)
                st.button('Login')
                return False

if authenticate_user():
    st.image('bcs.png')
    judul = st.write("""
    ## KALKULATOR TARIF & UJO TRUCKING
    
    note: angka ribuan ditulis tanpa titik dan angka desimal ditulis dengan titik
    """)
    unit = ['Pilih Unit','FL 10','FM 12','FM 12-420','HINO','Mercy Actros','Tronton FL 10','Tronton Mitsu','Tronton Hino','Mercy Axor']
    option = st.selectbox('Pilih Unit: ',unit)
    if option == 'Pilih Unit':
            st.write('Silahkan pilih unit yang akan digunakan!')
    elif option!=unit[0]:
        tgl = st.date_input('Tanggal Keberangkatan')
        customer = st.text_input('Nama Customer: ')
        origin = st.text_input('Origin: ')
        destination = st.text_input('Destination: ')
        jarak = st.number_input('Masukkan Jarak (KM): ')
        jarak2 = jarak*2
        adj_jarak = (5/100 * jarak2) + (jarak2)
        if jarak > 0:
            if adj_jarak <= 400:
                KPJ = 35 #km/jam
            elif adj_jarak > 400:
                KPJ = 50 #km/jam
            tol = st.number_input('Biaya Tol: ')
            tol_rp=f'{tol:,}'.replace(',','.')
            penyebrangan = st.number_input('Biaya Penyebrangan: ')
            penyebrangan_rp=f'{penyebrangan:,}'.replace(',','.')

            solar = 6800 #per liter
            LooL = 2 #jam
            waktu_tempuh = (adj_jarak/KPJ) + LooL
            if waktu_tempuh <= (math.floor(waktu_tempuh)+0.5):
                waktem = math.floor(waktu_tempuh)+0.5
            elif (math.floor(waktu_tempuh)+0.5) < waktu_tempuh < math.ceil(waktu_tempuh):
                waktem = math.ceil(waktu_tempuh)
            tph = 24/waktu_tempuh #trip per hari
            if tph <= 1:
                tph2 = 1
            elif tph == math.floor(tph):
                tph2 = tph
            elif tph > 1:
                if tph <= (math.floor(tph)+0.5):
                    tph2 = math.floor(tph) + 0.5
                elif (math.floor(tph)+0.5) < tph < math.ceil(tph):
                    tph2 = math.ceil(tph)
            hpt = waktu_tempuh/16
            if hpt <= 0.35 and hpt!=0:
                hpt = 0.35
            elif hpt > 0.35:
                hpt = waktu_tempuh/16
            if hpt == math.floor(hpt):
                hpt2 = hpt
            elif hpt <= (math.floor(hpt)+0.5):
                hpt2 = math.floor(hpt) + 0.5
            elif (math.floor(hpt)+0.5) < hpt < math.ceil(hpt):
                hpt2 = math.ceil(hpt)
            hari = waktu_tempuh/8
            if hari <= 0.35:
                hari3 = 0.35
            elif hari == 0:
                hari3 = 0
            elif hari > 0.35:
                hari3 = hari
                if hari3 != math.floor(hari3):
                    if hari3 <= (math.floor(hari3) + 0.5):
                        hari3 = math.floor(hari3) + 0.5
                    elif (math.floor(hari3) + 0.5) < hari3 < math.ceil(hari3):
                        hari3 = math.ceil(hari3)
            if 0 < jarak2 <= 20 and jarak2 != 0:
                komisi = 25000
                helper = 65000
            elif 20 < jarak2 <= 200:
                komisi = 75000
                helper = 65000
            elif jarak2 > 200:
                komisi = math.ceil(75000 * hari)
                helper = math.ceil(65000 * hari)
            
            if option == unit[1]:
                fuel = 2
            elif option == unit[2]:
                fuel = 2
            else:
                fuel = 2.5

            komisi_rp=f'{komisi:,}'.replace(',','.')
            helper_rp=f'{helper:,}'.replace(',','.')
            uang_makan = hari3 * 120000
            uang_makan_rp=f'{uang_makan:,}'.replace(',','.')
            retribusi = math.ceil(hari * 75000/500)*500
            retribusi_rp=f'{retribusi:,}'.replace(',','.')
            ritase = math.ceil(hari * 100000/500)*500
            ritase_rp=f'{ritase:,}'.replace(',','.')
            kehadiran = math.ceil(hari * 10000 /500)*500
            kehadiran_rp=f'{kehadiran:,}'.replace(',','.')
            
            bongkarmuat = 90000
            bongkarmuat_rp=f'{bongkarmuat:,}'.replace(',','.')
            bbm = adj_jarak/fuel
            uang_bbm = math.ceil(bbm * solar)
            bbm_rp = f'{uang_bbm:,}'.replace(',','.')

            total_ujo = math.ceil(uang_bbm + tol + bongkarmuat + uang_makan + retribusi + ritase + kehadiran + komisi + helper + penyebrangan)
            ujo_rp = f'{total_ujo:,}'.replace(',','.')
            fix_cost = 1700000 * hari3
            tarif = math.ceil((total_ujo+fix_cost)/1000)*1000
            tarif_rp = f'{tarif:,}'.replace(',','.')
            rasio = (total_ujo/tarif) * 100
            margin = st.number_input('Masukkan margin (tanda % tidak usah diinput):')
            tarifakhir = math.ceil((tarif + (tarif * margin/100))/1000)*1000
            tarifakhir_rp = f'{tarifakhir:,}'.replace(',','.')

            hitung = st.button('Hitung')
            def form_callback(data1, data2, data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15,data16,data17,data18,data19,data20,data21,data22,data23,data24,data25,data26,data27,data28,data29):    
                with open('notes.csv', 'a+') as f:    
                    f.write(f"{data1},{data2},{data3},{data4},{data5},{data6},{data7},{data8},{data9},{data10},{data11},{data12},{data13},{data14},{data15},{data16},{data17},{data18},{data19},{data20},{data21},{data22},{data23},{data24},{data25},{data26},{data27},{data28},{data29}\n")

            if hitung:
                st.info(f'Total UJO adalah Rp. {ujo_rp}.')
                st.error(f'Tarifnya adalah Rp. {tarif_rp}.')
                st.info(f'Tarif setelah diberikan margin {margin}% adalah Rp. {tarifakhir_rp}.')
                if rasio <= 50:
                    st.success (f'Rasio antara total UJO dengan tarif adalah {math.ceil(rasio)}%.')
                elif rasio > 50:
                    st.warning(f'Rasio antara total UJO dengan tarif adalah {math.ceil(rasio)}%.',icon='⚠️')
            
                @st.cache_data
                def gen_pdf():
                    pdf = FPDF()
                    pdf.add_page(orientation='P',format="a5")
                    
                    pdf.image('bcs.png',w=40,h=10,)

                    pdf.set_font("Arial",size=14)
                    pdf.cell(100,10,txt=f" ", ln=1,align="C")
                    pdf.cell(130,10,txt="UANG JALAN OPERASIONAL & TARIF", ln=1,align="C")

                    pdf.set_font("Arial",size=12)
                    pdf.cell(130,10,txt=f"{tgl}", ln=2,align="C")
                    pdf.cell(130,10,txt=f"Customer/Unit: {customer}/{option}", ln=1,align="L")
                    pdf.cell(130,10,txt=f"Origin - Destination: {origin} - {destination}",ln=1,align="L")
                    pdf.cell(130,10,txt=f" ", ln=1,align="C")

                    pdf.cell(130,10,txt=f"Tarif: Rp. {tarif_rp}", ln=2,align="L")
                    if margin>0:
                        pdf.cell(130,10,txt=f"Tarif dengan margin {margin}%: Rp. {tarifakhir_rp}", ln=2,align="L")
                    pdf.cell(130,10,txt=f"Total UJO: Rp. {ujo_rp}", ln=1,align="L")


                    pdf.cell(130,10,txt=f" ", ln=1,align="C")
                    pdf.cell(130,10,txt="Rincian Biaya", ln=1,align="C")
                    pdf.cell(130,10,txt=f"BBM/Biaya BBM: {math.ceil(bbm)} liter/Rp. {bbm_rp}", ln=1,align="L")
                    pdf.cell(130,10,txt=f"Uang Tol/Bongkat Muat: Rp. {tol_rp}/Rp. {bongkarmuat_rp}", ln=2,align="L")
                    pdf.cell(130,10,txt=f"Kehadiran/Uang Makan: Rp. {kehadiran_rp}/Rp. {uang_makan_rp}", ln=2,align="L")
                    pdf.cell(130,10,txt=f"Retribusi/Ritase: Rp. {retribusi_rp}/Rp. {ritase_rp}", ln=2,align="L")
                    if penyebrangan>0:
                        pdf.cell(130,10,txt=f"Penyebrangan: Rp. {penyebrangan_rp}", ln=2,align="L")
                    pdf.cell(130,10,txt=f" ", ln=1,align="C")

                    
                    return bytes(pdf.output())

                base64_pdf = b64encode(gen_pdf()).decode("utf-8")
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
                st.markdown(pdf_display, unsafe_allow_html=True)

                 

            with st.form(key="my_form",clear_on_submit=True):
                st.write('Pastikan semua data yang diinput sudah benar sebelum di-submit!')
                submitted = st.form_submit_button("Submit")
                if submitted:
                    form_callback(tgl,customer,origin,destination,option,jarak2,adj_jarak,KPJ,math.ceil(bbm),bbm_rp,LooL,waktem,tph2,hpt2,hari3,tol_rp,bongkarmuat_rp,uang_makan_rp,retribusi_rp,ritase_rp,kehadiran_rp,komisi_rp,helper_rp,penyebrangan_rp,ujo_rp,tarif_rp,margin,tarifakhir_rp,math.ceil(rasio))

            df=pd.read_csv("notes.csv",sep='delimiter',names=["Tanggal","Customer","Origin",'Destination','Unit','Jarak (Km)',' Adj. Jarak (Km)','KPJ','Solar (Liter)','Uang Solar','Lo/oL (Jam)','Waktu Tempuh(Jam)','Trip per Hari','Hari per Trip','Hari','Tol','B/M','U/M','Retribusi','Ritase','Kehadiran','Komisi','Helper','Penyebrangan','Total UJO','Tarif','Margin(%)','Tarif (dengan margin)','Rasio (%)'])
            def convert_df(df):
                    return df.to_csv(index=False).encode('utf-8')
            csv = convert_df(df)
            st.write("Silahkan submit data terlebih dahulu untuk mendownload file CSV!")
                    
                    
            st.download_button(
                "📥Press to Download CSV File",
                csv,
                "UJO.csv",
                "text/csv",
                key='download-csv'
            )

