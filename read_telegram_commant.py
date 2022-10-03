from urllib.request import urlopen
import json
import cv2
import os
import time 
import datetime

# Check if there is new msg_id found
last_msg_id = -1


import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')

CAM_ID = int(parser['Settings']['cam_id'])
TELE_TOKEN = parser['Settings']['tele_token']
FRAME_RATE = int(parser['Settings']['frame_rate'])
FRAME_HISTORY = int(parser['Settings']['frame_history'])
VIDEO_LENGTH = int(parser['Settings']['video_length'])

# Open camera 
video_capture = cv2.VideoCapture(CAM_ID) # Edit the cam ID here

url = "https://api.telegram.org/bot"+TELE_TOKEN+"/getUpdates"

SAMPLE_TIME = float(1.0/FRAME_RATE)

FRAME_LIST = []
MAX_FRAME_LIST = int(60*FRAME_RATE*FRAME_HISTORY)


# FLUSH all data before starting again ## CAUTION
try:
	os.system('rm ./data/images/*')
	os.system('rm ./data/videos/*')
except:
	print("Folder not flused")

# if "stop" is not sent to terminate
while last_msg_id != "stop":

	try:
		response = urlopen(url)
		data_json = json.loads(response.read())
		 
		msg_id = data_json["result"][-1]['channel_post']["message_id"]
		msg_txt = data_json["result"][-1]['channel_post']["text"]


		# taking a frame to save 
		ret, frame = video_capture.read()

		#write that to disk
		PATH = './data/images/'+str(datetime.datetime.now().strftime("%Y:%m:%d_%H:%M:%S"))+'.png'
		FRAME_LIST.append(PATH)

		cv2.imwrite(PATH,frame)

		# Delete older frames from data folder
		if(len(FRAME_LIST) > MAX_FRAME_LIST):
			while (len(FRAME_LIST) > MAX_FRAME_LIST):
				if os.path.exists(FRAME_LIST[0]):
				  os.remove(FRAME_LIST[0])
				else:
				  print("The file does not exist: ", FRAME_LIST[0])
				FRAME_LIST.pop(0)



		# If new msg_id is found from telegram
		if msg_id != last_msg_id:
			last_msg_id = msg_id

			# If "photo" or "Photo" or "P" is sent
			if msg_txt == "photo" or msg_txt == "Photo" or msg_txt == "P":
				print("Taking a photo to send!")
				
				os.system("telegram-send --image "+str(FRAME_LIST[-1])+"  --caption '"+str(datetime.datetime.now().strftime("%Y:%m:%d_%H:%M:%S"))+"'")

				print("Sent successfully!")

			# If "video" or "Video" or "V" is sent
			elif msg_txt == "video" or msg_txt == "Video" or msg_txt == "V":
				print("Preparing video to send!")

				try:
					os.system('rm ./data/videos/*')
				except:
					print("Videos not flushed!")

				if len(FRAME_LIST) > VIDEO_LENGTH*FRAME_RATE:
					for i in range(len(FRAME_LIST)):
						if i >= len(FRAME_LIST) - VIDEO_LENGTH*FRAME_RATE:
							os.system("cp "+str(FRAME_LIST[i])+" ./data/videos/")
				else:
					os.system("cp ./data/images/* ./data/videos/")


				video_name = str(datetime.datetime.now().strftime("%Y:%m:%d_%H:%M:%S"))+".mp4"
				os.system("ffmpeg -framerate "+str(FRAME_RATE)+" -pattern_type glob -i './data/videos/*.png'  -pix_fmt yuv420p ./data/videos/"+video_name)
				os.system("telegram-send --video ./data/videos/"+video_name+"  --caption '"+video_name+"'")
				
				print("Sent successfully!")

			elif msg_txt == "stop":
				break
			else:
				print("Not a valid command!")

		# Wait will the frame rate is matched
		time.sleep(SAMPLE_TIME)
	except Exception as e:
		print("Waiting fix!", e)

video_capture.release()