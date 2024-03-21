import pygame
import serial
import time

joysticks = {}
last_axis_check_time=time.time()

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM15'
ser.open()



def main():
    pygame.init()

    done = False
    while not done:

        done = Controller_Input(done)  # Aktualisiere done


def Controller_Input(done):
    global last_axis_check_time

    axis0_value = 0
    axis1_value = 0
    axis2_value = 0
    axis3_value = 0
    axis4_value = 0
    axis5_value = 0


    for event in pygame.event.get():
        current_time = time.time()

        if event.type == pygame.QUIT:
            done = True  #

        elif event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} verbunden")

        elif event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} getrennt")

        elif event.type == pygame.JOYBUTTONDOWN:
            joystick = joysticks[event.instance_id]
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if i == 0 and button == 1:
                    print("Knopf 0 wurde gedrückt!")

        # Alle 0,1 Sekunden überprüfen
        if event.type == pygame.JOYAXISMOTION and (current_time - last_axis_check_time) >= 100:
            joystick = joysticks[event.instance_id]
            # Überprüfe die Achsen
            if event.axis == 0:
                axis0_value = round(joystick.get_axis(0), 1)
                print(f"Achse 0 Wert: {axis0_value}")
            elif event.axis == 1:
                axis1_value = round(joystick.get_axis(1), 1)
                print(f"Achse 1 Wert: {axis1_value}")
            elif event.axis == 2:
                axis2_value = round(joystick.get_axis(2), 1)
                print(f"Achse 2 Wert: {axis2_value}")
            elif event.axis == 3:
                axis3_value = round(joystick.get_axis(3), 1)
                print(f"Achse 3 Wert: {axis3_value}")
            elif event.axis == 4:
                axis4_value = joystick.get_axis(4)
                axis4_value += 1
                axis4_value *= 0.5
                print(f"Achse 4 Wert: {round(axis4_value, 1)}")
            elif event.axis == 5:
                axis5_value = joystick.get_axis(5)
                axis5_value += 1
                axis5_value *= 0.5
                print(f"Achse 5 Wert: {round(axis5_value, 1)}")

            Startup = False
            last_axis_check_time = current_time  # Aktualisiert last_axis_check_time
            Arm_Calc(axis0_value, axis1_value, axis2_value, axis3_value, axis4_value, axis5_value)

    return done


def Arm_Calc(axis0_value, axis1_value, axis2_value, axis3_value, axis4_value, axis5_value):
    axis0_value_send = int(axis0_value * 100+0.5)
    axis1_value_send = int(axis1_value * 100+0.5)
    axis2_value_send = int(axis2_value * 100+0.5)
    axis3_value_send = int(axis3_value * 100+0.5)
    axis4_value_send = int(axis4_value * 100+0.5)
    axis5_value_send = int(axis5_value * 100+0.5)
    send(axis0_value_send, axis1_value_send, axis2_value_send, axis3_value_send, axis4_value_send, axis5_value_send)

def send(axis0_value_send, axis1_value_send, axis2_value_send, axis3_value_send, axis4_value_send, axis5_value_send):
    str = f"{axis0_value_send},{axis1_value_send},{axis2_value_send},{axis3_value_send},{axis4_value_send},{axis5_value_send}"
    ser.write(bytearray(str,'ASCII') + bytearray([10]))  # Korrigierte Zeile

if __name__ == '__main__':
    main()
