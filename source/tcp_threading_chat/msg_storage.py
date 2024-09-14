from threading import Lock


class Storage:

    def __init__(self):
        self.all_messages = []
        self.list_lock = Lock()


    def put(self, msg):
        with self.list_lock:
            self.all_messages.append(msg)

    

    

