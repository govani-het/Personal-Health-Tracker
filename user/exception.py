class ValueError(ValueError):
    """This Will Raise a Value Error"""
    pass

class AuthenticationError(ValueError):
    """This Will Raise a Username Error"""
    pass

class UserBlocked(ValueError):
    """This Will Raise a Username Error"""
    pass

class ProfileSetUpAlreadyExists(ValueError):
    pass