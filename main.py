import streamlit as st
from web3 import Web3
import base64
from ABI import *
import json

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

user_address = st.text_input('Input Address', placeholder='0x...')
try:
    IDS = (contract3.caller.tokenIdsOfOwner(user_address))
    col1, col2 = st.columns(2)
    with col1:
        for gotchis in IDS[:5]:
            st.write(contract.caller.getAavegotchiSvg(gotchis),unsafe_allow_html=True)
    with col2:
        for gotchis in IDS[5:]:
            st.write(contract.caller.getAavegotchiSvg(gotchis),unsafe_allow_html=True)


except:
    st.warning('Insert valid address')

