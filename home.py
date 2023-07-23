import streamlit as st
from pytrends.request import TrendReq
from japanmap import picture
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

#input_num = st.number_input('Input a number', value=0)
keyword= st.text_input('Input any words')

flgButton = st.button('Send')

#result = input_num ** 2
#st.write('Result: ', result)
if flgButton:
    pytrends = TrendReq(hl='ja-JP',tz=-540)

    kw_list = [keyword]

    pytrends.build_payload(kw_list,cat=0,timeframe='2022-06-01 2022-12-30',geo='JP',gprop='')
    df = pytrends.interest_by_region(resolution='JP', inc_low_vol=True,inc_geo_code=True)
    df['geoCode']=df['geoCode'].str.replace('JP-','').astype(int)


    cmap = plt.get_cmap('jet')
    norm = plt.Normalize(vmin=df[keyword].min(),vmax=df[keyword].max())

    mappable = cm.ScalarMappable(cmap=cmap,norm=norm)
    mappable._A = []

    fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()


    plt.figure(figsize=(10,8))
    plt.colorbar(mappable)
    plt.imsave('map.png', picture(df[keyword].apply(fcol)))

    img = Image.open('map.png')
    st.image(img)




