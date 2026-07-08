import streamlit as st

#initializing 
st.title("The Identity Echo Interface")
st.write("Enter your name and a message, then click 'Transmit'.")

#taking input
user_name = st.text_input("Name")
user_message = st.text_input("Message")

#submiting
if st.button("Transmit"):

   
    if user_name.strip() == "":
        st.error("Please provide your name.")

    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")

    
    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        #token cost estimater
        total_characters = len(user_message)
        token_count = total_characters / 4

        st.info(
            f"System Check: Your message will consume approximately {token_count:.2f} tokens from our context window."
        )