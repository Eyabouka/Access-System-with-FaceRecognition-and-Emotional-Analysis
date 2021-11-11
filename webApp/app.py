import streamlit as st
import pandas as pd
import cv2
import datetime

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():


	st.title("ACCESS SYSTEM ")
	run = st.checkbox('Run')
	FRAME_WINDOW = st.image([])
	camera = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './haarcascade_frontalface_default.xml')

	while run:
		_, frame = camera.read()
		# Convert to grayscale
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# Detect the faces
		faces = face_cascade.detectMultiScale(frame, 1.1, 4)
		# Draw the rectangle around each face
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
		FRAME_WINDOW.image(frame)
	else:
		st.write('Stopped')
	st.sidebar.image('./entreprise.jpg')
	tab = st.sidebar.columns(2)
	today = datetime.date.today()
	tab[0].date_input('Today', today)
	tab[1].time_input("time")
	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				#if task == "Add Post":
				#	st.subheader("Add Your Post")

#				elif task == "Analytics":
#					st.subheader("Analytics")
#				elif task == "Profiles":
#					st.subheader("User Profiles")
				user_result = view_all_users()
				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
				st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
			st.button('Back')

if __name__ == '__main__':
	main()