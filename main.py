import pygame
from playsound import playsound

import concurrent.futures
import asyncio

def play(file):
	playsound(file)

if __name__ == "__main__":
	pygame.init()
	joysticks = []
	clock = pygame.time.Clock()
	executor = concurrent.futures.ThreadPoolExecutor(50)
	loop = asyncio.get_event_loop()

	# for al the connected joysticks
	for i in range(0, pygame.joystick.get_count()):
		# create an Joystick object in our list
		joysticks.append(pygame.joystick.Joystick(i))

		# initialize them all (-1 means loop forever)
		joysticks[-1].init()

		# print a statement telling what the name of the controller is
		print ("Detected joystick "),joysticks[-1].get_name(),"'"

	baseDir = "./samples/"
	buttonMap = {
		0: {
			"name": "green",
			"sample": "stand.wav"
		},
		1: {
			"name": "red",
			"sample": "snare.wav"
		},
		2: {
			"name": "blue",
			"sample": "tom.wav"
		},
		3: {
			"name": "yellow",
			"sample": "hat.wav"
		},
		5: {
			"name": "orange",
			"sample": "crash.wav"
		},
	}
  
	while True:
		clock.tick(1000)
		
		event = pygame.event.get()

		if (len(event) != 0 and event[0].type == 1539):
			button = vars(event[0])

			if ("button" in button.keys()):
				print(buttonMap[button["button"]])

				file = baseDir + buttonMap[button["button"]]["sample"]
				loop.run_in_executor(executor, play, file)