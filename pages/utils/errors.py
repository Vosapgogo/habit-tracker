class ValidationError(Exception):
    pass

class UserNotFoundError(Exception):
    def __init__(self, message="There is no such user"):
        self.message = message
        super().__init__(self.message)

class DataStorageError(Exception):
    def __init__(self, message="There was a problem with the data storage files"):
        self.message = message
        super().__init__(self.message)