import threading


class ThreadSafeDict:
    def __init__(self):
        self.dictionary = {}
        self.lock = threading.Lock()


    def del_item(self, key):
        with self.lock:
            if key in self.dictionary:
                del self.dictionary[key]


    def set_item(self, key, value):
        with self.lock:
            self.dictionary[key] = value


    def get_item(self, key):
        with self.lock:
            return self.dictionary[key]

    
    def is_contains(self, key):
        with self.lock:
            return True if key in self.dictionary else False
    
    def copy_values(self):
        with self.lock:
            return list(self.dictionary.values())
        

    def copy_keys(self):
        with self.lock:
            return list(self.dictionary.keys())
        

    def add_if_not_exist(self, key, value):
        with self.lock:
            if key not in self.dictionary:
                self.dictionary[key] = value
                return True
            return False