import streamlit as st
import json
import py_nillion_client as nillion
import os
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

import nada_numpy as na
import nada_numpy.client as na_client
from common.utils import compute, store_program, store_secrets

def addition():
    st.header("Addition")
    num1 = st.number_input("Enter the first number:", value=0.0, key="add_num1")
    num2 = st.number_input("Enter the second number:", value=0.0, key="add_num2")
    
    if st.button("Add", key="add_button"):
        result = num1 + num2
        st.success(f"The sum of {num1} and {num2} is: {result}")

def subtraction():
    st.header("Subtraction")
    num1 = st.number_input("Enter the first number:", value=0, key="sub_num1")
    num2 = st.number_input("Enter the second number:", value=0, key="sub_num2")
    
    if st.button("Subtract", key="sub_button"):
        result = num1 - num2
        st.success(f"The difference between {num1} and {num2} is: {result}")

def main():
    st.title("Simple Math Operations App")

    tab1, tab2 = st.tabs(["Addition", "Subtraction"])
    
    with tab1:
        addition()
    
    with tab2:
        subtraction()

if __name__ == "__main__":
    main()
