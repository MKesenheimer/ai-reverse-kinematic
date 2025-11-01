import redis
import math
import functions

# singleton decorator if needed
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

class data_class():
    def __init__(self):
        self.vars = {}
        self.redis_available = False
        try:
            # start redis via docker:
            # docker run --rm --name redis -p 6379:6379 -v "$(pwd)/redis:/data" -d redis redis-server --save 60 1 --loglevel warning
            self.r = redis.Redis(host='localhost', port=6379, db=0)
            self.r.set('redis', 'init')
            self.redis_available = True
        except Exception as _:
            print("Warning: Redis not available. Using local data class. Communication with other processes will not work.")

    def set(self, key:str, value):
        self.vars[key] = value
        if self.redis_available:
            self.r.set(key, value)

    def get(self, key:str, type=float):
        if self.redis_available:
            if self.r.get(key) is None:
                self.r.set(key, 0)
            return type(self.r.get(key))
        else:
            try:
                return type(self.vars[key])
            except KeyError:
                self.vars[key] = 0
                return type(self.vars[key])

@singleton
class RobotState():
    def __init__(self):
        self.data = data_class()

    # Arm1 definitions
    def set_base_position_arm1(self, position:tuple):
        self.data.set('base_x_arm1', position[0])
        self.data.set('base_y_arm1', position[1])

    def get_base_position_arm1(self):
        return (self.data.get('base_x_arm1'), self.data.get('base_y_arm1'))

    def set_length_arm1(self, length:float):
        self.data.set('length_arm1', length)

    def set_angle_in_grad_arm1(self, angle1:float):
        angle1 = functions.scale_grad_to_rad(angle1)
        self.set_angle_arm1(angle1)

    def set_angle_arm1(self, angle1:float):
        self.data.set('angle_arm1', angle1)
        self.data.set('absolute_angle_arm1', angle1)
        x1 = self.data.get('base_x_arm1')
        y1 = self.data.get('base_y_arm1')
        r = self.data.get('length_arm1') / 2
        x = x1 + r * math.cos(angle1)
        y = y1 + r * math.sin(angle1)
        x2 = x1 + 2 * r * math.cos(angle1)
        y2 = y1 + 2 * r * math.sin(angle1)
        self.data.set('mid_x_arm1', x)
        self.data.set('mid_y_arm1', y)
        self.data.set('top_x_arm1', x2)
        self.data.set('top_y_arm1', y2)
        # update arm 2
        self.data.set('base_x_arm2', x2)
        self.data.set('base_y_arm2', y2)
        angle2 = self.get_angle_arm2()
        self.set_angle_arm2(angle2)

    def get_angle_arm1(self):
        return self.data.get('angle_arm1')

    def get_absolute_angle_arm1(self):
        return self.data.get('absolute_angle_arm1')

    def get_x_base_arm1(self):
        return self.data.get('base_x_arm1')

    def get_y_base_arm1(self):
        return self.data.get('base_y_arm1')

    def get_x_arm1(self):
        return self.data.get('mid_x_arm1')

    def get_y_arm1(self):
        return self.data.get('mid_y_arm1')

    def get_length_arm1(self):
        return self.data.get('length_arm1')

    def get_x_top_arm1(self):
        return self.data.get('top_x_arm1')

    def get_y_top_arm1(self):
        return self.data.get('top_y_arm1')

    def get_top_arm1(self):
        return (self.data.get('top_x_arm1'), self.data.get('top_y_arm1'))

    def get_relative_top_arm1(self):
        t = tuple(x - y for x, y in zip(self.get_top_arm1(), self.get_base_position_arm1()))
        return t

    # Arm2 definitions
    def set_base_position_arm2(self, position:tuple):
        self.data.set('base_x_arm2', position[0])
        self.data.set('base_y_arm2', position[1])

    def set_length_arm2(self, length:float):
        self.data.set('length_arm2', length)

    def set_angle_in_grad_arm2(self, angle2:float):
        angle2 = functions.scale_grad_to_rad(angle2)
        self.set_angle_arm2(angle2)

    def set_angle_arm2(self, angle2:float):
        angle1 = self.get_angle_arm1()
        abs_angle2 = angle1 + angle2 - math.pi
        self.data.set('absolute_angle_arm2', abs_angle2)
        self.data.set('angle_arm2', angle2)
        x1 = self.data.get('base_x_arm2')
        y1 = self.data.get('base_y_arm2')
        #print(x1, y1)
        #print(angle1, angle2)
        r = self.data.get('length_arm2') / 2
        x = x1 + r * math.cos(abs_angle2)
        y = y1 + r * math.sin(abs_angle2)
        x2 = x1 + 2 * r * math.cos(abs_angle2)
        y2 = y1 + 2 * r * math.sin(abs_angle2)
        self.data.set('mid_x_arm2', x)
        self.data.set('mid_y_arm2', y)
        self.data.set('top_x_arm2', x2)
        self.data.set('top_y_arm2', y2)
        # update arm 3
        self.data.set('base_x_arm3', x2)
        self.data.set('base_y_arm3', y2)
        angle3 = self.get_angle_arm3()
        self.set_angle_arm3(angle3)

    def get_angle_arm2(self):
        return self.data.get('angle_arm2')

    def get_absolute_angle_arm2(self):
        return self.data.get('absolute_angle_arm2')

    def get_x_arm2(self):
        return self.data.get('mid_x_arm2')

    def get_y_arm2(self):
        return self.data.get('mid_y_arm2')

    def get_length_arm2(self):
        return self.data.get('length_arm2')

    def get_x_top_arm2(self):
        return self.data.get('top_x_arm2')

    def get_y_top_arm2(self):
        return self.data.get('top_y_arm2')

    def get_top_arm2(self):
        return (self.data.get('top_x_arm2'), self.data.get('top_y_arm2'))

    def get_relative_top_arm2(self):
        t = tuple(x - y for x, y in zip(self.get_top_arm2(), self.get_base_position_arm1()))
        return t

    # Arm3 definitions
    def set_base_position_arm3(self, position:tuple):
        self.data.set('base_x_arm3', position[0])
        self.data.set('base_y_arm3', position[1])

    def set_length_arm3(self, length:float):
        self.data.set('length_arm3', length)

    def set_angle_in_grad_arm3(self, angle3:float):
        angle3 = functions.scale_grad_to_rad(angle3)
        self.set_angle_arm3(angle3)

    def set_angle_arm3(self, angle3:float):
        angle1 = self.get_angle_arm1()
        angle2 = self.get_angle_arm2()
        abs_angle3 = angle1 + angle2 + angle3
        self.data.set('absolute_angle_arm3', abs_angle3)
        self.data.set('angle_arm3', angle3)
        x1 = self.data.get('base_x_arm3')
        y1 = self.data.get('base_y_arm3')
        r = self.data.get('length_arm3') / 2
        x = x1 + r * math.cos(abs_angle3)
        y = y1 + r * math.sin(abs_angle3)
        x2 = x1 + 2 * r * math.cos(abs_angle3)
        y2 = y1 + 2 * r * math.sin(abs_angle3)
        self.data.set('mid_x_arm3', x)
        self.data.set('mid_y_arm3', y)
        self.data.set('top_x_arm3', x2)
        self.data.set('top_y_arm3', y2)

    def get_angle_arm3(self):
        return self.data.get('angle_arm3')

    def get_absolute_angle_arm3(self):
        return self.data.get('absolute_angle_arm3')

    def get_x_arm3(self):
        return self.data.get('mid_x_arm3')

    def get_y_arm3(self):
        return self.data.get('mid_y_arm3')

    def get_length_arm3(self):
        return self.data.get('length_arm3')

    def get_x_top_arm3(self):
        return self.data.get('top_x_arm3')

    def get_y_top_arm3(self):
        return self.data.get('top_y_arm3')

    def get_top_arm3(self):
        return (self.data.get('top_x_arm3'), self.data.get('top_y_arm3'))

    def get_relative_top_arm3(self):
        t = tuple(x - y for x, y in zip(self.get_top_arm3(), self.get_base_position_arm1()))
        return t