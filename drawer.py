import math

import sdl3
from Box2D import b2Draw

class Drawer(b2Draw):
    def __init__(self, renderer, pixelsPerMeter, thickness=3):
        super().__init__()
        self.renderer = renderer
        self.ppm = pixelsPerMeter
        self.thickness = thickness

    def DrawSolidPolygon(self, vertices, color):
        r = int(color.r * 255)
        g = int(color.g * 255)
        b = int(color.b * 255)
        sdl3.SDL_SetRenderDrawColor(self.renderer, r, g, b, sdl3.SDL_ALPHA_OPAQUE)

        x0 = vertices[0][0] * self.ppm
        y0 = vertices[0][1] * self.ppm
        x1 = vertices[1][0] * self.ppm
        y1 = vertices[1][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x0, y0, x1, y1)

        x1 = vertices[1][0] * self.ppm
        y1 = vertices[1][1] * self.ppm
        x2 = vertices[2][0] * self.ppm
        y2 = vertices[2][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x1, y1, x2, y2)

        x2 = vertices[2][0] * self.ppm
        y2 = vertices[2][1] * self.ppm
        x3 = vertices[3][0] * self.ppm
        y3 = vertices[3][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x2, y2, x3, y3)

        x3 = vertices[3][0] * self.ppm
        y3 = vertices[3][1] * self.ppm
        x0 = vertices[0][0] * self.ppm
        y0 = vertices[0][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x3, y3, x0, y0)

    def DrawSolidCircle(self, center, radius, axis, color):
        numberOfSegments = 100
        angle = 0
        angleStep = 360 / numberOfSegments

        r = int(color.r * 255)
        g = int(color.g * 255)
        b = int(color.b * 255)
        sdl3.SDL_SetRenderDrawColor(self.renderer, r, g, b, sdl3.SDL_ALPHA_OPAQUE)

        centerX = center[0] * self.ppm
        centerY = center[1] * self.ppm
        radius *= self.ppm
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        fromX = centerX + x
        fromY = centerY + y

        for _ in range(numberOfSegments + 1):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            toX = centerX + x
            toY = centerY + y
            sdl3.SDL_RenderLine(self.renderer, fromX, fromY, toX, toY)
            angle += angleStep
            fromX = toX
            fromY = toY

    def DrawPolygon(self, vertices, color):
        pass
    def DrawSegment(self, p1, p2, color):
        pass
    def DrawPoint(self, p, size, color):
        pass
    def DrawCircle(self, center, radius, color, drawwidth=1):
        pass
    def DrawTransform(self, xf):
        pass