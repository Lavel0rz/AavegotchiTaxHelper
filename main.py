import streamlit as st
from web3 import Web3
import base64
from ABI import *
import json
import pandas as pd
import numpy as np
wear_df = pd.read_csv('TestingWEAR.csv')
df_merged = pd.read_csv('TestingGOTCHIS.csv')
df_ghst = pd.read_csv('GHST.csv')
web3 = Web3(Web3.HTTPProvider(st.secrets['api']))
address = '0x86935F11C86623deC8a25696E1C19a8659CbF95d'

contract = web3.eth.contract(address=address, abi=abi)


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


contract2 = web3.eth.contract(address=address, abi=abi2)
contract3 = web3.eth.contract(address=address, abi=abi3)

user_address = st.text_input('Input Address', placeholder='0x...').lower()
ls_IDS = list(df_merged[df_merged['Buyer']==user_address.lower()]['ID'].values)



Gotchid = st.selectbox('Select a Gotcher ID',(ls_IDS))



Cost = df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['precio'].values[0]*(df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['Price'].values[0])
date = df_merged[df_merged['Buyer']==user_address][df_merged[df_merged['Buyer']==user_address]['ID']==Gotchid]['Date'].values[0]

st.markdown(f'BUY PRICE {round(Cost, 2)}$   \n Date of purchase: {date}')
try:
    sell = df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['precio'].values[0]*(df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['Price'].values[0])
    sell_date = df_merged[df_merged['Seller']==user_address][df_merged[df_merged['Seller']==user_address]['ID']==Gotchid]['Date'].values[0]

    st.markdown(f'SELL PRICE {round(sell, 2)}$   \n Date of purchase: {sell_date}')
except:st.warning('No sells found for this GotchiID!')
