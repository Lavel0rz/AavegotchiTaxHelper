import streamlit as st
from web3 import Web3
import base64
from ABI import *
import json
import pandas as pd
import numpy as np
wear_df = pd.read_csv('TestingWEAR.csv')
df_merged = pd.read_csv('RealWear.csv')
df_merged['Wearables'] = df_merged['Wearables'].apply(lambda x : ast.literal_eval(x))
df_ghst = pd.read_csv('GHST.csv')
wear_id = pd.read_csv('WearID.csv')
web3 = Web3(Web3.HTTPProvider(st.secrets['api']))
address = '0x86935F11C86623deC8a25696E1C19a8659CbF95d'
df_merged['Buyer'] = df_merged['Buyer'].apply(lambda x: x.lower())
df_merged['Seller'] = df_merged['Seller'].apply(lambda x: x.lower())
contract = web3.eth.contract(address=address, abi=abi)


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


contract2 = web3.eth.contract(address=address, abi=abi2)
contract3 = web3.eth.contract(address=address, abi=abi3)
try:
    user_address = st.text_input('Input Address', placeholder='0x...').lower()
except:
    st.warning('Input a valid Polygon Address')
ls_IDS = list(df_merged[df_merged['Seller']==user_address.lower()]['ID'].values)



Gotchid = st.selectbox('Select a Gotcher ID',(ls_IDS))


if Gotchid!= None :
    try:
        cost_ghst= df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['precio'].values[0]
        Cost_dollar = df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['precio'].values[0]*(df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['Price'].values[0])
        date = df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['Date'].values[0]

        st.markdown(f'Gotchi Buy Price {round(cost_ghst,2)}GHST, {round(Cost_dollar, 2)}($) \n Purchase Day: {date}')
    except:st.warning('No buys found for this GotchiID!')
    try:
        sell_ghst = df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['precio'].values[0]
        sell_dollar = df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['precio'].values[0]*(df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['Price'].values[0])
        sell_date = df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['Date'].values[0]

        st.markdown(f'Gotchi sell price {round(sell_ghst,2)}GHST, {round(sell_dollar, 2)}($) \n Sell Day: {sell_date}')
    except:st.warning('No sells found for this GotchiID!')
try:
    gotchi_wears = df_merged[df_merged['Buyer']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()][df_merged[df_merged['Buyer']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()]['ID']==Gotchid]['Wearables']
    gotchi_wears = gotchi_wears.iloc[0]


    total = 0
    total2 = 0
    wear_d ={}
except:st.warning('No Wearable sales found for this gotchi')
for ids in gotchi_wears:

    try:
        sell_date = wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()][wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()]['WearID']==ids]['Date'].values[0]
        wear_sell = wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()][wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()]['WearID']==ids]['precio'].values[0]
        wear_sell_usd = wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()][wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()]['WearID']==ids]['precio'].values[0]*wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()][wear_df[wear_df['Seller']=='0x39292E0157EF646cc9EA65dc48F8F91Cae009EAe'.lower()]['WearID']==ids]['Price'].values[0]
        wear_d[ids] = [wear_sell,round(wear_sell_usd,2),sell_date]
        total += wear_sell
        total2 += wear_sell_usd
    except:''

st.title('Found Wearable sales')
try:
    for k,v in wear_d.items():
        graph = graphviz.Digraph()
        graph.edge(wear_id[wear_id['ID']==k]['Name'].values[0],str(v[0])+'$GHST')
        graph.edge(wear_id[wear_id['ID']==k]['Name'].values[0],str(v[1])+'$USD')
        graph.edge(wear_id[wear_id['ID']==k]['Name'].values[0],str(v[2]))
        st.graphviz_chart(graph)

except: st.warning('Try another gotchi ID')

