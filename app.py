import streamlit as st
import json
import py_nillion_client as nillion
import os
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
import asyncio
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

import nada_numpy as na
import nada_numpy.client as na_client
from common.utils import compute, store_program, store_secrets
mlseed = "my_seed"
userkey = UserKey.from_seed((mlseed))
nodekey = NodeKey.from_seed((mlseed))
client = create_nillion_client(userkey, nodekey)
home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

async def addition():
    st.header("Addition")
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    num1 = st.number_input("Enter the first number:", value=0, key="add_num1")
    num2 = st.number_input("Enter the second number:", value=0, key="add_num2")
    program_name = "addition_simple"
    program_mir_path = f"../nadaprograms/{program_name}.nada.bin"
    print(program_mir_path)
    if st.button("Add", key="add_button"):
        # result=num1+num2
        # st.success(f"The sum of {num1} and {num2} is: {result}")
        payments_config = create_payments_config(chain_id, grpc_endpoint)
        payments_client = LedgerClient(payments_config)
        payments_wallet = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )
        receipt_store_program = await get_quote_and_pay(
            client,
            nillion.Operation.store_program(program_mir_path),
            payments_wallet,
            payments_client,
            cluster_id,
        )

        print(f"Storing program in the network: {program_name}")
        program_id = await client.store_program(
            cluster_id, program_name, program_mir_path, receipt_store_program
        )
        print("Stored program_id:", program_id)

        # 4. Create the 1st secret, add permissions, pay for and store it in the network
        # Create a secret named "my_int1" with any value, ex: 500
        new_secret = nillion.NadaValues(
            {
                "my_int1": nillion.SecretInteger(int(num1)),
            }
        )

        # Set the input party for the secret
        # The party name needs to match the party name that is storing "my_int1" in the program
        party_name = "Party1"
        party_id = client.party_id
        # Set permissions for the client to compute on the program
        permissions = nillion.Permissions.default_for_user(client.user_id)
        permissions.add_compute_permissions({client.user_id: {program_id}})

        # Pay for and store the secret in the network and print the returned store_id
        receipt_store = await get_quote_and_pay(
            client,
            nillion.Operation.store_values(new_secret, ttl_days=5),
            payments_wallet,
            payments_client,
            cluster_id,
        )
        # Store a secret
        store_id = await client.store_values(
            cluster_id, new_secret, permissions, receipt_store
        )
        print(f"Computing using program {program_id}")
        print(f"Use secret store_id: {store_id}")

        # 5. Create compute bindings to set input and output parties, add a computation time secret and pay for & run the computation
        compute_bindings = nillion.ProgramBindings(program_id)
        compute_bindings.add_input_party(party_name, party_id)
        compute_bindings.add_output_party(party_name, party_id)

        # Add my_int2, the 2nd secret at computation time
        computation_time_secrets = nillion.NadaValues({"my_int2": nillion.SecretInteger(int(num2))})

        # Pay for the compute
        receipt_compute = await get_quote_and_pay(
            client,
            nillion.Operation.compute(program_id, computation_time_secrets),
            payments_wallet,
            payments_client,
            cluster_id,
        )

        # Compute on the secret
        compute_id = await client.compute(
            cluster_id,
            compute_bindings,
            [store_id],
            computation_time_secrets,
            receipt_compute,
        )

        # 8. Return the computation result
        print(f"The computation was sent to the network. compute_id: {compute_id}")
        while True:
            compute_event = await client.next_compute_event()
            if isinstance(compute_event, nillion.ComputeFinishedEvent):
                print(f"✅  Compute complete for compute_id {compute_event.uuid}")
                print(f"🖥️  The result is {compute_event.result.value}")
                st.success(f"The sum of {num1} and {num2} is: {compute_event.result.value}")
                break

async def subtraction():
    st.header("Subtraction")
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    num1 = st.number_input("Enter the first number:", value=0, key="sub_num1")
    num2 = st.number_input("Enter the second number:", value=0, key="sub_num2")
    program_name = "subtraction_simple"
    program_mir_path = f"../nadaprograms/{program_name}.nada.bin"
    print(program_mir_path)
    if st.button("Subtract", key="sub_button"):
        # result=num1-num2
        # st.success(f"The difference between {num1} and {num2} is: {result}")
        payments_config = create_payments_config(chain_id, grpc_endpoint)
        payments_client = LedgerClient(payments_config)
        payments_wallet = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )
        receipt_store_program = await get_quote_and_pay(
            client,
            nillion.Operation.store_program(program_mir_path),
            payments_wallet,
            payments_client,
            cluster_id,
        )

        print(f"Storing program in the network: {program_name}")
        program_id = await client.store_program(
            cluster_id, program_name, program_mir_path, receipt_store_program
        )
        print("Stored program_id:", program_id)

        # 4. Create the 1st secret, add permissions, pay for and store it in the network
        # Create a secret named "my_int1" with any value, ex: 500
        new_secret = nillion.NadaValues(
            {
                "my_int1": nillion.SecretInteger(int(num1)),
            }
        )

        # Set the input party for the secret
        # The party name needs to match the party name that is storing "my_int1" in the program
        party_name = "Party1"
        party_id = client.party_id
        # Set permissions for the client to compute on the program
        permissions = nillion.Permissions.default_for_user(client.user_id)
        permissions.add_compute_permissions({client.user_id: {program_id}})

        # Pay for and store the secret in the network and print the returned store_id
        receipt_store = await get_quote_and_pay(
            client,
            nillion.Operation.store_values(new_secret, ttl_days=5),
            payments_wallet,
            payments_client,
            cluster_id,
        )
        # Store a secret
        store_id = await client.store_values(
            cluster_id, new_secret, permissions, receipt_store
        )
        print(f"Computing using program {program_id}")
        print(f"Use secret store_id: {store_id}")

        # 5. Create compute bindings to set input and output parties, add a computation time secret and pay for & run the computation
        compute_bindings = nillion.ProgramBindings(program_id)
        compute_bindings.add_input_party(party_name, party_id)
        compute_bindings.add_output_party(party_name, party_id)

        # Add my_int2, the 2nd secret at computation time
        computation_time_secrets = nillion.NadaValues({"my_int2": nillion.SecretInteger(int(num2))})

        # Pay for the compute
        receipt_compute = await get_quote_and_pay(
            client,
            nillion.Operation.compute(program_id, computation_time_secrets),
            payments_wallet,
            payments_client,
            cluster_id,
        )

        # Compute on the secret
        compute_id = await client.compute(
            cluster_id,
            compute_bindings,
            [store_id],
            computation_time_secrets,
            receipt_compute,
        )

        # 8. Return the computation result
        print(f"The computation was sent to the network. compute_id: {compute_id}")
        while True:
            compute_event = await client.next_compute_event()
            if isinstance(compute_event, nillion.ComputeFinishedEvent):
                print(f"✅  Compute complete for compute_id {compute_event.uuid}")
                print(f"🖥️  The result is {compute_event.result.value}")
                st.success(f"The difference between {num1} and {num2} is: {compute_event.result.value}")
                break

def main():
    st.title("Simple Math Operations App")

    tab1, tab2 = st.tabs(["Addition", "Subtraction"])
    
    with tab1:
        asyncio.run(addition())
    
    with tab2:
        asyncio.run(subtraction())

if __name__ == "__main__":
    main()
