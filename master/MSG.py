class MsgList:
    def __init__(self):
        self.__messages = []

    def add_msg(self, message):
        self.__messages.append(message)

    def get_msg(self):
        return self.__messages
