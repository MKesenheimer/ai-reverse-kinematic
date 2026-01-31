from robot import RobotState

##########################################################################################
# Roboterarm initialisieren                                                              #
##########################################################################################
robotState = RobotState()
robotState.set_length_arm1(24.0)
robotState.set_base_position_arm1((80, 0))
robotState.set_angle_in_grad_arm1(90)

robotState.set_length_arm2(19.3)
robotState.set_angle_in_grad_arm2(180)

robotState.set_length_arm3(0.0)
robotState.set_angle_in_grad_arm3(180)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

##########################################################################################
# Simulation des Roboterarms                                                             #
##########################################################################################
while True:
    try:
        # Benutzereingabe der Koordinaten im raumfesten Koordinatensystem
        angle1_grad = float(input("alpha1 eingeben: "))
        angle2_grad = float(input("alpha2 eingeben: "))
        angle3_grad = float(input("alpha3 eingeben: "))
        robotState.set_angle_in_grad_arm1(angle1_grad)
        robotState.set_angle_in_grad_arm2(angle2_grad)
        robotState.set_angle_in_grad_arm3(angle3_grad)

        #print(f"Koordinaten im raumfesten KS: X{X3_top} Y{Y3_top} Z{Z3_top}\n")
    except ValueError as e:
        print("Kein gültiger Winkel. Erneut versuchen.")
        print(e)
