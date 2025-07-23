import ctypes
import math
import os

from Box2D import (b2_dynamicBody, b2BodyDef, b2CircleShape, b2FixtureDef, b2PolygonShape, b2Vec2, b2World)

os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3
from drawer import Drawer
from state import RobotState

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

    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    windowTitle = "Draw Box2D colliders using line segments, PySDL3".encode()
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

    # Create a arm body
    robotArm1Def = b2BodyDef()
    robotArm1Def.allowSleep = False
    robotArm1Def.position = b2Vec2(200 / ppm, 210 / ppm)
    #robotArm1Def.type = b2_dynamicBody
    robotArm1 = world.CreateBody(robotArm1Def)
    robotArm1Shape = b2PolygonShape()
    robotArm1Shape.SetAsBox(10 / 2 / ppm, 60 / 2 / ppm)
    robotArm1FixtureDef = b2FixtureDef()
    robotArm1FixtureDef.shape = robotArm1Shape
    robotArm1FixtureDef.density = 0
    robotArm1.CreateFixture(robotArm1FixtureDef)

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
    
    robotArm1.angle = float(robotState.get_angle_arm1())

    world.Step(0.016, 3, 2)
    world.DrawDebugData()

    sdl3.SDL_RenderPresent(renderer)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):
    ... # SDL will clean up the window/renderer for us