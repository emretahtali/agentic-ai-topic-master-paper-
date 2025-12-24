def get_class_variable_fields(cls):
    return [name for name, val in cls.__dict__.items()
     if not callable(val) and not name.startswith('__')]


def get_class_field_values(cls):
    return list(map(cls.__dict__.get, get_class_variable_fields(cls)))
