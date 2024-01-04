import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av  #for video retrieved emotion from np
import cv2 #for video
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import webbrowser
from io import BytesIO
import requests
import tensorflow as tf
import tempfile
#import os

#PORT = int(os.environ.get('PORT', 8501)) # Use the PORT environment variable or default to 8501 if running locally

def music_rec_main():
    st.header("Music Recommendation Based on User Emotion")

# Function to load model from URL
def load_model_from_url(url):
    response = requests.get(url)
    model_content = BytesIO(response.content)
    
    # Save the model to a temporary local file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".h5") as temp_model_file:
        temp_model_file.write(model_content.getvalue())
        temp_model_path = temp_model_file.name
    
    # Load the model from the temporary local file
    loaded_model = load_model(temp_model_path)
    
    return loaded_model

# Load the labels.npy file
# labels_url = "https://drive.google.com/uc?id=1PoL_B8sPR8CqvRJbG1Mi1Xy_QPeIwc1Y"
model  = load_model("model.h5")
label = np.load("labels.npy")

# labels_url = 'labels.npy'
# label = np.load(BytesIO(requests.get(labels_url).content))

# # Load the model
# model_url = "https://drive.google.com/uc?id=1rzB_G6hqOiVZgJ4OABzw606g-ArKlqtM"
# model = load_model_from_url(model_url)

# # Load the emotion from Google Drive
# emotion_url = "https://drive.google.com/uc?id=1d0rBSvaqgfy-6Yf5nCALx01WuTMQQ27f"
# emotion = np.load(BytesIO(requests.get(emotion_url).content))[0]

holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils
#col1, col2 = st.columns(2)
st.header("Music Recommendation Based on User Emotion")

if "run" not in st.session_state:
	st.session_state["run"] = "true"

try:
	emotion = np.load("emotion.npy")[0]
except:
	emotion=""

if not(emotion):
	st.session_state["run"] = "true"
else:
	st.session_state["run"] = "true"

class EmotionProcessor:
	def recv(self, frame):
		frm = frame.to_ndarray(format="bgr24")

		##############################
		frm = cv2.flip(frm, 1)

		res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

		lst = []

		if res.face_landmarks:
			for i in res.face_landmarks.landmark:
				lst.append(i.x - res.face_landmarks.landmark[1].x)
				lst.append(i.y - res.face_landmarks.landmark[1].y)

			if res.left_hand_landmarks:
				for i in res.left_hand_landmarks.landmark:
					lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
					lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
			else:
				for i in range(42):
					lst.append(0.0)

			if res.right_hand_landmarks:
				for i in res.right_hand_landmarks.landmark:
					lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
					lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
			else:
				for i in range(42):
					lst.append(0.0)

			lst = np.array(lst).reshape(1,-1)

			pred = label[np.argmax(model.predict(lst))]

			print(pred)
			cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)

			np.save("emotion.npy", np.array([pred]))

			
		drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
								landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), thickness=-1, circle_radius=1),
								connection_drawing_spec=drawing.DrawingSpec(thickness=1))
		drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
		drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)


		##############################

		return av.VideoFrame.from_ndarray(frm, format="bgr24")
lang = ""
lang = st.selectbox(
   "Language:",
   ('English', 'Malay', 'Korean', 'Japan','Chinese', 'Others'),
   placeholder="Song Language",
)
artist = st.text_input("Artist Name")

# if lang and artist and st.session_state["run"] != "false":
# 	webrtc_streamer(key="key", desired_playing_state=True,
# 				video_processor_factory=EmotionProcessor)

webrtc_streamer(key="key", desired_playing_state=True,video_processor_factory=EmotionProcessor)

col1, col2 = st.columns(2)

# Button for Spotify recommendation
btn_spotify = col1.button("Recommend on Spotify")
# Button for YouTube recommendation
btn_youtube = col2.button("Recommend on YouTube")

def my_function():
	if not emotion:
		st.warning("Please let me capture your emotion first")
		st.session_state["run"] = "true"
	elif artist == "":
		st.warning("Please fil the artist")
		st.session_state["run"] = "true"
	elif lang == "":
		st.warning("Please Select the language")
		st.session_state["run"] = "true"
	elif st.session_state["run"] == "true":
			if btn_spotify:  # Check if the Spotify button is clicked
				webbrowser.open(f"https://open.spotify.com/search/{artist}{emotion}{lang}")
			elif btn_youtube:  # Check if the YouTube button is clicked
				webbrowser.open(f"https://music.youtube.com/search?q={artist}+{emotion}+song+{lang}")
	np.save("emotion.npy", np.array([""]))
	st.session_state["run"] = "false"
if btn_spotify or btn_youtube:
	my_function()
# 	if (emotion == "" and st.session_state["run"] == "false"):
# 		st.warning("Please let me capture your emotion first")
# 		st.session_state["run"] = "true"
# 	else:
# 		# webbrowser.open(f"https://www.youtube.com/results?search_query={lang}+{emotion}+song+{artist}")
# 		webbrowser.open(f"https://open.spotify.com/search/{lang}+{emotion}+song+{artist}")
# 		np.save("emotion.npy", np.array([""]))
# 		st.session_state["run"] = "false"

#if __name__ == '__main__':
#    st.run(port=PORT)
	
