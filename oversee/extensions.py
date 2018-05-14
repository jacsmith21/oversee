def validate(required, unless):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not kwargs[required] and not kwargs[unless]:
                raise ValueError('{} required if {} is not given!'.format(required, unless))
            func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
