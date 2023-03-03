import os
import pygame
pygame.init()
from dpeaDPi.DPiStepper import *
from time import sleep

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.clock import Clock

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.Joystick import Joystick

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'

dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")



class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White



class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """


    def pressMotor(self):
        dpiStepper.enableMotors(True)
        if self.ids.motor.text == 'on':
            self.ids.motor.text = 'off'
            self.ids.motor.color = 1, 0, 0, 1

            steps_per_rotation = 800
            wait_to_finish_moving_flg = False
            dpiStepper.moveToRelativePositionInSteps(0, 100 * -steps_per_rotation, wait_to_finish_moving_flg)



        else:
            self.ids.motor.text = 'on'
            self.ids.motor.color = 0, 1, 0, 1
            dpiStepper.enableMotors(False)


        print("Callback from MainScreen.pressed()")

    def changeDirection(self):
        #put getVlocity into a list, access index 1 of the list
        print(dpiStepper.getCurrentVelocityInRevolutionsPerSecond(0))
        data = tuple(dpiStepper.getCurrentVelocityInRevolutionsPerSecond(0))
        print(data[1])


        steps_per_rotation = 1600
        wait_to_finish_moving_flg = False
        if data[1] > 0:
            dpiStepper.decelerateToAStop(0)
            dpiStepper.moveToRelativePositionInSteps(0, -100*steps_per_rotation, wait_to_finish_moving_flg)
        else:
            dpiStepper.decelerateToAStop(0)
            dpiStepper.moveToRelativePositionInSteps(0, 100*steps_per_rotation, wait_to_finish_moving_flg)

    def slideSpeed(self):
        dpiStepper.enableMotors(True)
        speed_in_mm_per_sec = int(self.ids.slider_label.value)
        accel_in_mm_per_sec_per_sec = int(self.ids.slider_label.value)
        dpiStepper.setSpeedInMillimetersPerSecond(0, speed_in_mm_per_sec)
        dpiStepper.setAccelerationInMillimetersPerSecondPerSecond(0, accel_in_mm_per_sec_per_sec)
        steps_per_rotation = 1600
        wait_to_finish_moving_flg = False
        if self.ids.slider_label.value>0:
            dpiStepper.moveToRelativePositionInSteps(0, 100*steps_per_rotation, wait_to_finish_moving_flg)
        else:
            dpiStepper.enableMotors(False)

    def display(self):
        revolutions = tuple(dpiStepper.getCurrentPositionInRevolutions(0))
        self.ids.position.text = str(revolutions[1])


        print(dpiStepper.getCurrentPositionInRevolutions(0))
        waitToFinishFlg = True
        dpiStepper.enableMotors(True)
        dpiStepper.setSpeedInRevolutionsPerSecond(0,1.0)
        dpiStepper.moveToAbsolutePositionInRevolutions(0, 15, False)


        while revolutions[1]<15:
            revolutions = tuple(dpiStepper.getCurrentPositionInRevolutions(0))
            if revolutions[1]==15:
                self.ids.position.text = str(revolutions[1])


        print("first movement")
        print(dpiStepper.getCurrentPositionInRevolutions(0))
        sleep(10)

        dpiStepper.setSpeedInRevolutionsPerSecond(0,5.0)
        dpiStepper.moveToAbsolutePositionInRevolutions(0, 25, waitToFinishFlg)
        print("second movement")
        print(dpiStepper.getCurrentPositionInRevolutions(0))
        while revolutions[1]<25:
            revolutions = tuple(dpiStepper.getCurrentPositionInRevolutions(0))
            if revolutions[1]==25:
                self.ids.position.text = str(revolutions[1])

        sleep(8)


        directionToMoveTowardHome = 1
        homeSpeedInStepsPerSecond = 1600
        homeMaxDistanceToMoveInSteps = 3200



        dpiStepper.moveToHomeInSteps(0, directionToMoveTowardHome, homeSpeedInStepsPerSecond,homeMaxDistanceToMoveInSteps)
        dpiStepper.setCurrentPositionInSteps(0, 0)
        print("third movement")
        print(dpiStepper.getCurrentPositionInRevolutions(0))
        sleep(30)

        dpiStepper.setSpeedInRevolutionsPerSecond(0,8.0)
        dpiStepper.moveToAbsolutePositionInRevolutions(0, 100, waitToFinishFlg)
        print(dpiStepper.getCurrentPositionInRevolutions(0))
        sleep(10)



        dpiStepper.moveToAbsolutePositionInRevolutions(0, 0, waitToFinishFlg)

        print("last movement")
        print(dpiStepper.getCurrentPositionInRevolutions(0))
        sleep(30)


    def zero(self):
        dpiStepper.enableMotors(True)
        dpiStepper.moveToAbsolutePositionInRevolutions(0,0,True)


















"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()

