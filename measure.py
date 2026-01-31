from robot import RobotState
import functions
import math
import json
from gcodeSender import GCodeSender
import time

##########################################################################################
# Roboterarm initialisieren                                                              #
##########################################################################################
# TODO: Parameter des physikalischen Modells hier eintragen
robotState = RobotState()
robotState.set_length_arm1(24.0)
robotState.set_base_position_arm1((200, 0))
robotState.set_angle_in_grad_arm1(180)

robotState.set_length_arm2(19.3)
robotState.set_angle_in_grad_arm2(180)

robotState.set_length_arm3(0.0)
robotState.set_angle_in_grad_arm3(180)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

##########################################################################################
# GCodeSender initialisieren                                                              #
##########################################################################################
sender = GCodeSender("/dev/tty.usbserial-1120")
time.sleep(1)

##########################################################################################
# Messung durchführen                                                                    #
##########################################################################################
list_alpha = []
list_coord = []
while True:
    # TODO:
    # An der Stelle Kommunikation mit dem "echten" Roboterarm einfügen
    # -> MCodes an den Roboterarm senden
    # bspw.:
    # M0 Z<beta_grad>
    # M0 A<angle1_grad>
    # M0 B<angle2_grad>
    #print(input())
    try:
        beta_grad = float(sender.sendGcode("M0 Z"))
        angle1_grad = float(sender.sendGcode("M0 A"))
        angle2_grad = float(sender.sendGcode("M0 B"))
    except Exception as e:
        print(f"Fehler bei der Konvertierung: {e}")

    beta = functions.scale_grad_to_rad(beta_grad)

    robotState.set_angle_in_grad_arm1(angle1_grad)
    robotState.set_angle_in_grad_arm2(angle2_grad)
    Xs3_top, Zs3_top = robotState.get_relative_top_arm3()

    # rücktransformation in das raumfeste KS: Xs, Ys -> X, Y
    # Ys ist im mitrotierenden Koordinatensystem 0
    Ys = 0
    X3_top = Xs3_top * math.cos(beta) - Ys * math.sin(beta)
    Y3_top = Xs3_top * math.sin(beta) + Ys * math.cos(beta)
    Z3_top = Zs3_top

    print(f"\nWinkel: beta = {beta_grad}, alpha1 = {angle1_grad}, alpha2 = {angle2_grad}")
    print(f"Koordinaten im raumfesten KS: X{X3_top} Y{Y3_top} Z{Z3_top}\n")

    alpha_values = [angle1_grad, angle2_grad]
    list_alpha.append(alpha_values)
    #print(list_alpha)

    coord_values = [Xs3_top, Zs3_top]
    list_coord.append(coord_values)
    #print(list_coord)

    try:
        input("Drücke Enter für neue Messung.")
    except:
        break

# Combine into a dictionary
data = {
    "list_alpha": list_alpha,
    "list_coord": list_coord,
    "max_length": max_length
}
#print(data)

# Write to JSON file
with open("model_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("\nKoordinaten nach model_data.json gespeichert.\nEnde.")