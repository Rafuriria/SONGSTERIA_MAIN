import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av 
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import webbrowser

model  = load_model("model.h5")
label = np.load("labels.npy")
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
				webbrowser.open(f"https://open.spotify.com/search/{lang}{emotion}{artist}")
			elif btn_youtube:  # Check if the YouTube button is clicked
				webbrowser.open(f"https://music.youtube.com/search?q={artist}+{lang}+{emotion}")
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
	#https://music.youtube.com/search?q=taylor+swift+neutral+song+english

