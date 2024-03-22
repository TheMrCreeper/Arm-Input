import pygame
import serial
import threading
import time

class JoystickController:
    def __init__(self):
        self.ser = serial.Serial(baudrate=9600, port='COM15')
        self.joystick = None
        self.axis_values = [0] * 6
        self.done = False
        self.button_output = 0

    def initialize_pygame(self):
        pygame.init()
        pygame.joystick.init()

    def connect_joystick(self):
        pygame.event.set_allowed([pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED])
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick {self.joystick.get_instance_id()} connected")
        else:
            print("No joystick detected")
            # Set all axis values to 0 when no joystick is detected
            self.axis_values = [0] * 6

    def send_data_thread(self):
        while not self.done:
            self.update_axis_values()
            self.send_data()
            time.sleep(0.1)

    def update_axis_values(self):
        for axis in range(6):
            raw_value = self.joystick.get_axis(axis)
            if axis == 4 or axis == 5:
                self.axis_values[axis] = int((raw_value + 1) * 50)  # Achse 4 und 5 werdencon 0-100 skaliert
            else:
                if -0.15 <= raw_value <= 0.15:
                    self.axis_values[axis] = 0
                else:
                    self.axis_values[axis] = int(round(raw_value * 100))

        if self.joystick.get_button(0):
            button_0_pressed = 1
        else:
            button_0_pressed = 0

        if self.joystick.get_button(1):
            button_1_pressed = 1
        else:
            button_1_pressed = 0

        self.button_output = button_0_pressed - button_1_pressed



    def send_data(self):
        data_str = ','.join(map(str, self.axis_values))
        data_str = f'{data_str},{self.button_output}\n'
        self.ser.write(data_str.encode('ASCII'))
        print(data_str)

    def start(self):
        self.initialize_pygame()
        self.connect_joystick()
        threading.Thread(target=self.send_data_thread, daemon=True).start()

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.connect_joystick()
                elif event.type == pygame.JOYDEVICEREMOVED:
                    print(f"Joystick {event.instance_id} disconnected")
            time.sleep(0.01)  # Short sleep to prevent busy waiting



if __name__ == '__main__':
    controller = JoystickController()
    controller.start()
