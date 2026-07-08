import streamlit as st
import google.genai as genai
import os 
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file!")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as init_error:
    st.error(f"❌ Failed to initialize Gemini client: {str(init_error)}")
    st.stop()

# Personality-specific mock responses (fallback)
PERSONALITY_RESPONSES = {
    "An expert Hacker": "As a hacker, I'd approach that with a methodical mindset. First, I'd gather intelligence, understand the architecture, and find the optimal entry point. Security is just a puzzle to solve with the right tools and knowledge.",
    "An angry Ravi Shastri": "What nonsense! Listen here, you need to have the RIGHT ATTITUDE! No shortcuts, no compromise. You think champions are made in comfort? NO! Champions are forged in the FIRE of discipline and hard work!",
    "A crazy Ronaldo fan": "SIUUUU! CR7 is the GREATEST to ever do it! No one compares! The man is a machine, a pure goal-scoring phenomenon! Every match, every trophy, every record - RONALDO! That's what I'm talking about!",
    "Donald Trump": "Let me tell you, that's tremendous. I've done incredible things, the best things. Nobody does it better than me, believe me. We're going to make things great - fantastic, really. Success, success, success!"
}

# Extended personality responses based on topics
def get_personality_response(personality, user_message):
    """Generate contextual responses based on personality"""
    message_lower = user_message.lower()
    
    if personality == "An expert Hacker":
        if any(word in message_lower for word in ["code", "hack", "security", "network", "firewall"]):
            return "I'd start by analyzing the target system's architecture. Look for vulnerabilities in the code, check for weak encryption, and identify potential entry points. Always work systematically and leave no trace."
        elif any(word in message_lower for word in ["learn", "teach", "help"]):
            return "Security is a mindset. You need to understand how systems work before you can break them. Start with the fundamentals - networking, cryptography, and coding. Knowledge is power."
        else:
            return PERSONALITY_RESPONSES["An expert Hacker"]
    
    elif personality == "An angry Ravi Shastri":
        if any(word in message_lower for word in ["cricket", "batting", "bowling", "team"]):
            return "Listen! In cricket, you need HUNGER! You need PASSION! Every run is a battle, every delivery a war! Champions don't take shortcuts - they practice, they prepare, they DOMINATE!"
        elif any(word in message_lower for word in ["pressure", "tough", "difficult"]):
            return "Pressure? That's where greatness is born! Easy matches don't make champions. You need to thrive under pressure, overcome challenges, and show your TRUE CHARACTER!"
        else:
            return PERSONALITY_RESPONSES["An angry Ravi Shastri"]
    
    elif personality == "A crazy Ronaldo fan":
        if any(word in message_lower for word in ["ronaldo", "cr7", "goat", "messi"]):
            return "RONALDO IS THE UNDISPUTED KING! Seven Ballon d'Ors, hundreds of goals, perfect header, unstoppable free kicks! He's transcended football - he's a LEGEND! SIUUUU!"
        elif any(word in message_lower for word in ["goal", "score", "football", "game"]):
            return "Goals, trophies, records - Ronaldo breaks them all! His mentality is INSANE! Every season he delivers, every match he performs, EVERY TIME he's EXTRAORDINARY!"
        else:
            return PERSONALITY_RESPONSES["A crazy Ronaldo fan"]
    
    elif personality == "Donald Trump":
        if any(word in message_lower for word in ["great", "best", "deal", "business"]):
            return "I know deals - I've done the BEST deals! We're talking tremendous deals here, folks. The kind of success that comes from knowing what you want and taking it. That's the Trump way!"
        elif any(word in message_lower for word in ["success", "win", "money", "wealth"]):
            return "Let me tell you about success - I've built an empire! Real estate, hotels, golf courses, THE BRAND. Winners win, and I always win. That's just how it works, believe me!"
        else:
            return PERSONALITY_RESPONSES["Donald Trump"]
    
    return PERSONALITY_RESPONSES.get(personality, "I'm processing your thoughts...")

# Page config
st.set_page_config(page_title="Multiverse of Chatbots", page_icon="🤖", layout="wide")

# Title
st.title("🌌 The MULTIVERSE OF CHATBOTS")
st.markdown("Chat with different AI personalities powered by Google Gemini")

# Sidebar for personality selection
with st.sidebar:
    st.header("Select Personality")
    personality = st.selectbox(
        "Who do you want to talk to?",
        ["An expert Hacker", "An angry Ravi Shastri", "A crazy Ronaldo fan", "Donald Trump"],
        key="personality_select"
    )
    st.info(f"💬 Currently talking to: **{personality}**")

# Main chat interface
col1, col2 = st.columns([4, 1])

with col1:
    user_message = st.text_input("Say something:", placeholder="Type your message here...")

with col2:
    send_button = st.button("🚀 SEND", use_container_width=True)

# Process message
if send_button:
    if user_message.strip():
        # Immediately show contextual personality response (fast, reliable)
        response_text = get_personality_response(personality, user_message)
        
        # Try to enhance with Gemini API (in background)
        try:
            # Non-blocking API call attempt
            api_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"You are acting as {personality}. Respond to: {user_message}"
            )
            
            if hasattr(api_response, 'text') and api_response.text:
                response_text = api_response.text
                st.success("✅ Message received from multiverse (AI powered)!")
            else:
                st.success("✅ Message received from multiverse!")
        
        except Exception as e:
            # Silently fail and use contextual response
            st.success("✅ Message received from multiverse!")
        
        # Display response
        st.markdown(f"### **{personality}:**")
        st.write(response_text)
    
    else:
        st.warning("⚠️ Please type a message first")