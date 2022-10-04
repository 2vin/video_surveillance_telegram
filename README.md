<a href="https://linkedin.com/in/2vin"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></img></a>
<a href="https://connect.vin"><img src="https://img.shields.io/badge/website-FF6A00?style=for-the-badge&logo=About.me&logoColor=white"></img></a>

# video_surveillance_telegram_bot
Image/Video surveillance using OpenCV and Telegram

Using this code, you can build your own video surveillance software which can capture images/videos at regular time interval(s). 
1. It logs the data automatically in "./images" folder
2. It sends the latest image/video to Telegram channel remotely anywhere
3. Type and send "photo" for viewing latest image, "video" for viewing a 5-minute latest video on your "private" Telegram channel

## Demo
<table>
  <tr>
    <td>Image Sample </td>
    <td>Video Sample </td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/38634222/193904621-702be152-5b94-4beb-94d9-bb232c271c3f.jpeg" width=160 height=320></td>
    <td><img src="https://user-images.githubusercontent.com/38634222/193904626-b5a8d03d-db68-426f-85b2-94b68732889c.jpeg" width=160 height=320></td>
  </tr>
 </table>
 

## About the repository
* 'data' : Folder to save image/video
* 'config.ini' : Configuration file for saving important parameters
* 'read_telegram_commant.py' : Main file containing the code

## Usage:

Step 1: Create your TELEGRAM channel and get the relevant TOKEN key.
Step 2: Add this TOKEN key in config.ini
Step 3: Install `telegram_send` using PIP and use following commands to add all subscribers of your telegram channel through their TOKEN(s)
```
telegram-send --configure-channel
```
Step 4: Run the following command in a terminal
```
python read_telegram_commant.py
```

This will open a camera capturing module. It will keep on logging images and send the images/videos when requested by the telegram channel.

