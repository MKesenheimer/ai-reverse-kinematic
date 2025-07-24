import redis

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
        try:
            self.r = redis.Redis(host='localhost', port=6379, db=0)
            self.r.set('redis', 'init')
        except Exception as _:
            print("Warning: Redis not available. Using local data class. Communication with other processes will not work.")

    def set(self, key:str, value):
        self.vars[key] = value
        try:
            self.r.set(key, value)
        except Exception as _:
            print("Warning: Redis not available. Using local data class. Communication with other processes will not work.")

    def get(self, key:str):
        try:
            return self.r.get(key)
        except Exception as _:
            try:
                return self.vars[key]
            except Exception as _:
                self.vars[key] = 0
                return self.vars[key]

@singleton
class RobotState():
    def __init__(self):
        self.data = data_class()

    def set_angle_arm1(self, angle):
        self.data.set('angle_arm1', angle)

    def get_angle_arm1(self):
        return self.data.get('angle_arm1')