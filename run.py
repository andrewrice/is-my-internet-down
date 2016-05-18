import os, sys
import simpleaudio
import argparse
from time import sleep
from contextlib import contextmanager

# Parse Script Arguments
parser = argparse.ArgumentParser(description='Check if your internet connection is down, and if so, panic.')
parser.add_argument('--hostname', help='Hostname to attempt to resolve', default='google.com')
parser.add_argument('--timeout', help='Amount of time in milliseconds to wait before panicking', default="10000")
parser.add_argument('--delay', help='Amount of time in seconds to wait before successively checking host resolution', default=3)

# Add arguments to global namespace
hostname = parser.parse_args().hostname
wait_time = str(parser.parse_args().timeout) # Must be a string because its being concatenated into os.system command
seconds_between_checks = int(parser.parse_args().delay) # Must be an integer since sleep() requires integer as argument

# Configure sounds
sounds_dir = os.path.abspath('./') + '/sounds/'
connected_sound = "ta-da.wav"
disconnected_sound = "flatline.wav"

# Initialize internet_status flag
internet_status = "Offline"

# Check internet status
def internet_is_down():
	
	# Ping server, hide output
	response = os.system('ping -c 1 -W ' + wait_time + ' ' + hostname + " > /dev/null 2>&1 ")

	# Check response for non-zero values
	# (anything > 0 represents an error code)
	if response == 0:
		return False
	else:
		return True

# Execute script
def run_internet_check():

	global seconds_between_checks
	global internet_status

	# Delay checks as desired
	sleep(seconds_between_checks)

	# Check if the connection is currently down
	if internet_is_down():

		# If the connection was not previously down, 
		# play a sound and set the `internet_status` flag to offline
		if not internet_status is 'offline':
			
			print("Connection possibly lost.")

			if confirming_disconnect():
				internet_status = 'offline'
				print("You are now offline.")
			else:
				print("Whew! Crisis averted")

		# ... and repeat
		run_internet_check()

	# Check if the internet is currently online
	else: 

		# If the connection was not previously online,
		# play a sound and set the `internet_status` flag to online
		if not internet_status is 'online': 
			
			print("Congrats! You're online.")
			internet_status = 'online'
			play_success_sound()

		# ... and repeat 	
		run_internet_check()

# Utility function to play sound on success
def play_success_sound():

	global connected_sound;

	# Build a simpleaudio object from the sound file
	# then play the sound and wait for it to finish
	wave_obj = simpleaudio.WaveObject.from_wave_file(sounds_dir + connected_sound)
	play_obj = wave_obj.play()
	play_obj.wait_done()

def confirming_disconnect():

	# Build a simpleaudio object from the sound file
	# then play the sound and wait for it to finish
	wave_obj = simpleaudio.WaveObject.from_wave_file(sounds_dir + disconnected_sound)
	play_obj = wave_obj.play()

	# While the countdown alarm is playing, try to re-establish connection
	while play_obj.is_playing():

		# Ping server with minimal timeout (100ms)
		response = os.system('ping -c 1 -W 100 ' + hostname + " > /dev/null 2>&1 ")

		# If connected, abort countown
		if response == 0:
			play_obj.stop()
			return False

	# Countdown completed without re-establishing connection
	return True

# Initialize the internet check
run_internet_check()