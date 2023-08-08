registered_functions = []


def register_plugin(func):
    registered_functions.append(func)
    return func
