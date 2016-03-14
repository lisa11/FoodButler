# Exception class for FoodButler Program

class MyError(Exception):
    '''
    Exception class mainly for insufficient recipes supplied
    This class is modified from:
    https://docs.python.org/2/tutorial/errors.html#user-defined-exceptions
    '''

    def __init__(self, message="insufficient qualified recipes returned by yummly"):
        self.message = message
    
    def __str__(self):
        return repr(self.message)