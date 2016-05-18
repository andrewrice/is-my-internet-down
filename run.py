import os, sys
import simpleaudio
import argparse
from time import sleep
from contextlib import contextmanager

# Parse Script Arguments
parser = argparse.ArgumentParser(description='Check if your internet connection is down, and if so, panic.')
parser.add_argument('--hostname', help='Hostname to attempt to resolve', default='google.com')
parser.add_argument('--timeout', help='Amount of time in milliseconds to wait before panicking', default='3000')
hostname = parser.parse_args().hostname
wait_time = parser.parse_args().timeout

# Set sound directory
sounds_dir = os.path.abspath('./') + '/sounds/'

# Initialize internet_status flag
internet_status = "Offline"

# Utility function to suppress console output
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

# Utility function to play sound
def play_sound(sound_file):

	# Build a simpleaudio object from the sound file
	# then play the sound and wait for it to finish
	sound_obj = simpleaudio.WaveObject.from_wave_file(sounds_dir + sound_file)
	sound_obj.play().wait_done()

# Check internet status
def internet_is_down():
	
	# with suppress_stdout():
	response = os.system('ping -c 1 -W ' + wait_time + ' ' + hostname + " > /dev/null 2>&1 ")

	if response == 0:
		return False
	else:
		return True

# Execute script
def run_internet_check():

	sleep(1)
	global internet_status

	# Check if the connection is currently down
	if internet_is_down():

		# If the connection was not previously down, 
		# play a sound and set the `internet_status` flag to oflfine
		if not internet_status is 'offline':
			
			print("OH MY GOD WE'RE LOSING IT!")
			print("NOOOOO!");
			internet_status = 'offline'
			play_sound('flatline.wav') 
			print("You are now offline.")

		# ... and repeat
		run_internet_check()

	# Check if the internet is currently online
	else: 

		# If the connection was not previously online,
		# play a sound and set the `internet_status` flag to online
		if not internet_status is 'online': 
			
			print("You're online!")
			internet_status = 'online'
			play_sound('ta-da.wav')

		# ... and repeat 	
		run_internet_check()

# Initialize the internet check
run_internet_check()