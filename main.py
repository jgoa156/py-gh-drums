from charset_normalizer import detect
import pygame
from playsound import playsound
import concurrent.futures
import asyncio

# CONSTS
TICKRATE = 100000
MAX_SAMPLE_THREADS = 50

# GLOBALS
controllers = []
baseDir = "./samples/"
defaultMap = {
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


def play(file):
    playsound(file)


class Controller:
    def __init__(self, joystick, name, map={}):
        print(f"New joystick detected - {name}")

        self.joystick = joystick
        self.name = name
        self.map = map

        self.executor = concurrent.futures.ThreadPoolExecutor(
            MAX_SAMPLE_THREADS)
        self.loop = asyncio.get_event_loop()
        self.joystick.init()

    def executeCommand(self, button):
        if (button in self.map.keys()):
            print(self.map[button])

            file = baseDir + self.map[button]["sample"]
            self.loop.run_in_executor(self.executor, play, file)


def detectControllers():
    joystickCount = 0

    # while(True):
    newCount = pygame.joystick.get_count()

    if (joystickCount != newCount):
        for index in range(joystickCount, newCount):
            joystick = pygame.joystick.Joystick(index)

            controllers.append(Controller(
                joystick, joystick.get_name(), defaultMap))

        joystickCount = newCount


def listen():
    clock = pygame.time.Clock()
    clock.tick(TICKRATE)

    while True:
        event = pygame.event.get()

        if (len(event) != 0 and event[0].type == pygame.JOYBUTTONDOWN):
            controllers[event[0].joy].executeCommand(event[0].button)


if __name__ == "__main__":
    pygame.init()

    """
    executor = concurrent.futures.ThreadPoolExecutor(2)
    loop = asyncio.get_event_loop()

    loop.run_in_executor(executor, detectControllers)
    loop.run_in_executor(executor, listen)
    """

    detectControllers()
    listen()
