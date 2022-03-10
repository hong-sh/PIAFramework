import platform
import os

class BlackBoard:
    def __init__(self):
        self.run_redis_server()

    def run_redis_server(self):
        running_os = platform.system()
        if running_os == "Windows":
            os.system("C:\\Program Files\\Redis\\redis-server --service-start")
        elif running_os == "Darwin" or running_os == "Linux":
            os.system("sudo systemctl restart redis.service")

    