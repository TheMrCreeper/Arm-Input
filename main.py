import pygame
import serial
import threading
import time


class JoystickController:
    def __init__(self):
        self.ser = serial.Serial(baudrate=9600, port='COM1')
        self.joystick = None
        self.axis_values = [0] * 6
        self.done = False

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
            time.sleep(0.5)

    def update_axis_values(self):
        for axis in range(6):
            raw_value = self.joystick.get_axis(axis)
            if axis == 4 or axis == 5:
                # Keep axis 4 and 5 values between -100 and 100
                self.axis_values[axis] = int(raw_value * 100)
            else:
                self.axis_values[axis] = int(round(raw_value * 100))

    def send_data(self):
        data_str = ','.join(map(str, self.axis_values))
        self.ser.write(bytearray(data_str + '\n', 'ASCII'))
        print(bytearray(data_str + '\n', 'ASCII'))

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

    def handle_button_down(self, event):
        if event.button == 0:
            print("Button 0 pressed!")


if __name__ == '__main__':
    controller = JoystickController()
    controller.start()


#stable
