# plugins/__init__.py
PLUGINS = {}

def register_plugin(name):
    def decorator(cls):
        PLUGINS[name] = cls
        return cls
    return decorator
