import functions as Function


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WHITE = '\033[39m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class log_type:
    PING = "[\033[39m" + "P\033[39m]"
    READ = "[\033[92m" + "R\033[39m]"
    INFO = "[\033[95m" + "I\033[39m]"
    ONLINE = "[\033[93m" + "O\033[39m]"


class log:
    def __init__(self, name):
        self.name = name

    def log_prefix_r(self):
        return "[" + bcolors.OKCYAN + " " * int(14 - len(self.name)) + self.name + bcolors.WHITE + "]"

    def log_prefix_addr(self):
        return "[" + bcolors.OKCYAN + " " * int(2 - len(self.name)) + self.name + bcolors.WHITE + "]"
