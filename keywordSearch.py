import streamlit as st
from pytrends.request import TrendReq
from japanmap import picture
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
from time import sleep
import datetime

st.title('The prefecture where this word was most interasted')

def main(start_day, end_day):
    keyword= st.text_input('Input any words')

    flgButton = st.button('Send')

    st.button('Reload')

    if flgButton:
            st.info('processing')
            sleep(5)
            try:

                pytrends = TrendReq(hl='ja-JP', tz=-540)

                kw_list = [keyword]

                pytrends.build_payload(kw_list, cat=0, timeframe=str(start_day)+" "+str(end_day), geo='JP', gprop='')
                df = pytrends.interest_by_region(resolution='City', inc_low_vol=True, inc_geo_code=True)
                df['geoCode']=df['geoCode'].str.replace('JP-','').astype(int)

                cmap = plt.get_cmap('jet')
                norm = plt.Normalize(vmin=df[keyword].min(),vmax=df[keyword].max())

                mappable = cm.ScalarMappable(cmap=cmap,norm=norm)
                mappable._A = []

                fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

                plt.figure(figsize=(10,8))
                plt.colorbar(mappable)
                plt.imshow(picture(df[keyword].apply(fcol)))
                plt.savefig('map.png')
                try:
                    img = Image.open('map.png')
                    st.image(img)
                except:
                    st.error("Error occured while displaying picture")

            except Exception as e:
                print("Error occured:",e)
                st.error("Error occured while processing, Please try again 5 minutes later")

    else:
        pass

if __name__=="__main__":
    today=datetime.date.today()
    timedelta = datetime.timedelta(days=365)
    last_year_today=today-timedelta
    main(start_day=last_year_today, end_day=today)
    
