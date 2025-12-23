def get_class_variable_fields(cls):
    return [name for name, val in cls.__dict__.items()
     if not callable(val) and not name.startswith('__')]
