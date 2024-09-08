import streamlit as st

def main():
    st.title("Simple Addition App")

    # Input fields for two numbers
    num1 = st.number_input("Enter the first number:", value=0.0)
    num2 = st.number_input("Enter the second number:", value=0.0)

    # Button to perform addition
    if st.button("Add"):
        result = num1 + num2
        st.success(f"The sum of {num1} and {num2} is: {result}")

if __name__ == "__main__":
    main()
