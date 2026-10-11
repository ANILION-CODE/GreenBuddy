import streamlit as st
import os
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="GreenBuddy",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 GreenBuddy")
st.subheader("Your AI gardening companion")
st.write("Plan less on your screen. Grow more in the real world.")

with st.form("garden_form"):
    city = st.text_input("Your city", placeholder="e.g. Kolkata")

    space = st.selectbox(
        "Where will you grow plants?",
        ["Balcony", "Terrace", "Garden", "Windowsill"]
    )

    sunlight = st.selectbox(
        "How much sunlight does the space get?",
        ["Low sunlight", "Partial sunlight", "Direct sunlight"]
    )

    plants = st.text_input(
        "What would you like to grow?",
        placeholder="e.g. Mint, coriander, tomatoes"
    )

    submitted = st.form_submit_button("🌿 Create my garden plan")

if submitted:
    if not city.strip() or not plants.strip():
        st.warning("Please enter your city and the plants you want to grow.")
    else:
        token = os.getenv("HF_TOKEN")

        if not token:
            st.error(
                "Hugging Face token not found. "
                "Set the HF_TOKEN environment variable first."
            )
        else:
            try:
                client = InferenceClient(
                    provider="auto",
                    api_key=token
                )

                with st.spinner("Growing your garden plan..."):
                    response = client.chat.completions.create(
                        model="Qwen/Qwen3-4B",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are GreenBuddy, a careful gardening "
                                    "assistant. Give practical, beginner-friendly "
                                    "advice. Do not invent local weather or "
                                    "seasonal facts. If information is uncertain, "
                                    "say so. End with one simple outdoor task."
                                )
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"City: {city}\n"
                                    f"Growing space: {space}\n"
                                    f"Sunlight: {sunlight}\n"
                                    f"Desired plants: {plants}\n\n"
                                    "Create a practical gardening plan with "
                                    "planting considerations, care tips, and "
                                    "one outdoor mission for today."
                                )
                            }
                        ],
                        max_tokens=600
                    )

                st.markdown("## 🌱 Your garden plan")
                st.write(response.choices[0].message.content)

                st.success(
                    "Now step outside and try your gardening mission!"
                )

            except Exception as error:
                st.error(
                    "The AI request failed. Check your token, model access, "
                    "internet connection, and available inference quota."
                )
                st.caption(str(error))
