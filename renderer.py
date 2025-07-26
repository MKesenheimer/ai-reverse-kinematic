import ctypes
import os

from Box2D import (b2_dynamicBody, b2BodyDef, b2CircleShape, b2FixtureDef, b2PolygonShape, b2Vec2, b2World)

os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3
from drawer import Drawer
from robot import RobotState

renderer = ctypes.POINTER(sdl3.SDL_Renderer)()
window = ctypes.POINTER(sdl3.SDL_Window)()
world = b2World(gravity=b2Vec2(0, 9.8))
# pixels per meter
ppm = 30
# state of the robot
robotState = RobotState()

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):
    global robotArm1
    global robotArm2
    global robotArm3

    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    windowTitle = "Robot Arm Renderer".encode()
    if not sdl3.SDL_CreateWindowAndRenderer(windowTitle, 500, 300, 0, window, renderer):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    sdl3.SDL_SetRenderVSync(renderer, 1) # Turn on vertical sync

    drawer = Drawer(renderer, ppm)
    drawer.flags = { "drawShapes": True }
    world.renderer = drawer

    # Create a ground body
    groundBodyDef = b2BodyDef()
    groundBodyDef.position = b2Vec2(250 / ppm, 270 / ppm)
    groundBody = world.CreateBody(groundBodyDef)
    groundShape = b2PolygonShape()
    groundShape.SetAsBox(400 / 2 / ppm, 40 / 2 / ppm)
    groundFixtureDef = b2FixtureDef()
    groundFixtureDef.shape = groundShape
    groundFixtureDef.density = 0
    groundBody.CreateFixture(groundFixtureDef)

    # Create a arm1 body
    robotArm1_length = float(robotState.get_length_arm1())
    robotArm1_x = float(robotState.get_x_arm1())
    robotArm1_y = float(robotState.get_y_arm1())
    robotArm1_angle = float(robotState.get_angle_arm1())
    robotArm1Def = b2BodyDef()
    robotArm1Def.allowSleep = False
    robotArm1Def.position = b2Vec2(robotArm1_x / ppm, robotArm1_y / ppm)
    robotArm1Def.angle = robotArm1_angle
    robotArm1Def.type = b2_dynamicBody
    robotArm1 = world.CreateBody(robotArm1Def)
    robotArm1Shape = b2PolygonShape()
    robotArm1Shape.SetAsBox(10 / 2 / ppm, robotArm1_length / 2 / ppm)
    robotArm1FixtureDef = b2FixtureDef()
    robotArm1FixtureDef.shape = robotArm1Shape
    robotArm1FixtureDef.density = 0
    robotArm1.CreateFixture(robotArm1FixtureDef)

    # Create a arm2 body
    robotArm2_length = float(robotState.get_length_arm2())
    robotArm2_x = float(robotState.get_x_arm2())
    robotArm2_y = float(robotState.get_y_arm2())
    robotArm2_angle = float(robotState.get_angle_arm2())
    robotArm2Def = b2BodyDef()
    robotArm2Def.allowSleep = False
    robotArm2Def.position = b2Vec2(robotArm2_x / ppm, robotArm2_y / ppm)
    robotArm2Def.angle = robotArm2_angle
    robotArm2Def.type = b2_dynamicBody
    robotArm2 = world.CreateBody(robotArm2Def)
    robotArm2Shape = b2PolygonShape()
    robotArm2Shape.SetAsBox(10 / 2 / ppm, robotArm2_length / 2 / ppm)
    robotArm2FixtureDef = b2FixtureDef()
    robotArm2FixtureDef.shape = robotArm2Shape
    robotArm2FixtureDef.density = 0
    robotArm2.CreateFixture(robotArm2FixtureDef)

    # Create a arm3 body
    robotArm3_length = float(robotState.get_length_arm3())
    robotArm3_x = float(robotState.get_x_arm3())
    robotArm3_y = float(robotState.get_y_arm3())
    robotArm3_angle = float(robotState.get_angle_arm3())
    robotArm3Def = b2BodyDef()
    robotArm3Def.allowSleep = False
    robotArm3Def.position = b2Vec2(robotArm3_x / ppm, robotArm3_y / ppm)
    robotArm3Def.angle = robotArm3_angle
    robotArm3Def.type = b2_dynamicBody
    robotArm3 = world.CreateBody(robotArm3Def)
    robotArm3Shape = b2PolygonShape()
    robotArm3Shape.SetAsBox(10 / 2 / ppm, robotArm3_length / 2 / ppm)
    robotArm3FixtureDef = b2FixtureDef()
    robotArm3FixtureDef.shape = robotArm3Shape
    robotArm3FixtureDef.density = 0
    robotArm3.CreateFixture(robotArm3FixtureDef)

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS
    elif sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_MOUSE_BUTTON_DOWN:
        print("click")

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):
    sdl3.SDL_SetRenderDrawColor(renderer, 33, 33, 33, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(renderer) # Start with a blank canvas
    
    robotArm1.angle = robotState.get_absolute_angle_arm1()
    robotArm1.position = b2Vec2(robotState.get_x_arm1() / ppm, robotState.get_y_arm1() / ppm)

    robotArm2.angle = robotState.get_absolute_angle_arm2()
    robotArm2.position = b2Vec2(robotState.get_x_arm2() / ppm, robotState.get_y_arm2() / ppm)

    robotArm3.angle = robotState.get_absolute_angle_arm3()
    robotArm3.position = b2Vec2(robotState.get_x_arm3() / ppm, robotState.get_y_arm3() / ppm)

    world.Step(0.016, 3, 2)
    world.DrawDebugData()

    sdl3.SDL_RenderPresent(renderer)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):
    ... # SDL will clean up the window/renderer for us