import streamlit as st
import requests

# Page title for the Streamlit app
st.title("MY AI IMAGE GENERATOR")

# Sidebar settings section for the app
st.sidebar.header("SETTINGS")
art_style = st.sidebar.selectbox(
    "Select desired Art Style",
    ["Photorealistic", "Anime", "Vintage Victorian", "Sketch", "3D Render"]
)

# Width and height sliders for the generated image
width = st.sidebar.slider("Image width", min_value=256, max_value=1024, value=768)
height = st.sidebar.slider("Image height", min_value=256, max_value=1024, value=768)

# User prompt input field
user_prompt = st.text_input("Describe the image you want to generate")

# Generate button triggers API call and image display
if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Rendering the image"):
            # Build the prompt with the selected art style
            full_prompt = f"{user_prompt}, make the art style: {art_style}"
            url = f"https://image.pollinations.ai/prompt/{full_prompt}"

            # Request the generated image from the external API
            response = requests.get(url)

            if response.status_code == 200:
                st.success("Image Generated")
                # Display the fetched image in the Streamlit app
                st.image(response.content, caption=full_prompt)

                # Provide a download button for the generated image
                st.download_button(
                    "Download image",
                    data=response.content,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                # Show an error if the API request failed
                st.error("API is not working")
    else:
        # Prompt the user to enter a description before generating
        st.warning("Please provide a prompt to generate an image")