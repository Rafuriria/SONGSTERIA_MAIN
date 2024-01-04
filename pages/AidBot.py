import streamlit as st
import random
import collections.abc
collections.Hashable = collections.abc.Hashable
import yaml
import requests


def AidBot():
    st.header("AidBot Page")

# Specify the Google Drive file ID for your YAML file
file_id = "18qOjzodU4rt-Jn8p2f4EouLrBP5OCDyc"

def fetch_yaml_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"

    # Make an HTTP request to fetch the YAML content
    response = requests.get(url)

    # Load the YAML content into a dictionary
    dataset = yaml.safe_load(response.text)

    return dataset.get("conversations", [])

# Fetch the YAML content directly from Google Drive
dataset = fetch_yaml_from_drive(file_id)

def get_chatbot_response(user_input, dataset, conversation_history):
    for conversation in dataset:
        if user_input in conversation:
            responses = conversation[conversation.index(user_input) + 1]

            # Randomly select one response
            selected_response = random.choice(responses)

            # Include the entire conversation in the responses
            conversation_history.append({"user": user_input, "bot": selected_response})

            return conversation_history

def main():
    st.title("AidBot")

    # Initialize or get the conversation history
    conversation_history = st.session_state.get("conversation_history", [])

    # Display the entire conversation as a chatbox
    chat_container = st.empty()

    for entry in conversation_history:
        if entry['user']:
            chat_container.markdown(f'<div style="display: flex; justify-content: flex-end; padding: 5px;">'
                                    f'<div style="background-color: #DA70D6; color: #fff; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["user"]}</div></div>',
                                    unsafe_allow_html=True)
        if entry['bot']:
            chat_container.markdown(f'<div style="display: flex; padding: 5px;">'
                                    f'<div style="background-color: #a2d5f2; color: #1f1f1f; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["bot"]}</div></div>',
                                    unsafe_allow_html=True)

    # User input field under the chat history
    user_input = st.text_input("You:")
    response_button = st.button("Get Response")

    if user_input and response_button:
        # Get and update the conversation history
        conversation_history = get_chatbot_response(user_input, dataset, conversation_history)

        # Save conversation history to session state
        st.session_state.conversation_history = conversation_history

        # Update the chat container with the new messages
        chat_container.empty()
        for entry in conversation_history:
            if entry['user']:
                chat_container.markdown(f'<div style="display: flex; justify-content: flex-end; padding: 5px;">'
                                        f'<div style="background-color: #DA70D6; color: #fff; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["user"]}</div></div>',
                                        unsafe_allow_html=True)
            if entry['bot']:
                chat_container.markdown(f'<div style="display: flex; padding: 5px;">'
                                        f'<div style="background-color: #a2d5f2; color: #1f1f1f; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["bot"]}</div></div>',
                                        unsafe_allow_html=True)

    # Display the full conversation history with adjusted padding
    st.subheader("Chat History")
    for entry in conversation_history:
        if entry['user']:
            st.markdown(f'<div style="text-align: right; margin-bottom: 20px;">'
                        f'<span style="background-color: #DA70D6; color: #fff; padding: 8px; border-radius: 10px; max-width: 70%;">You: {entry["user"]}</span></div>',
                        unsafe_allow_html=True)
        if entry['bot']:
            st.markdown(f'<div style="margin-bottom: 20px;">'
                        f'<span style="background-color: #a2d5f2; color: #1f1f1f; padding: 8px; border-radius: 10px; max-width: 70%;">Aid: {entry["bot"]}</span></div>',
                        unsafe_allow_html=True)

if __name__ == "__main__":
    main()
