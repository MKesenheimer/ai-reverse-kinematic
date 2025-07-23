import redis

# singleton decorator if needed
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class RobotState():
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.r.set('angle_arm1', 0)

    def set_angle_arm1(self, angle):
        self.r.set('angle_arm1', angle)

    def get_angle_arm1(self):
        return self.r.get('angle_arm1')