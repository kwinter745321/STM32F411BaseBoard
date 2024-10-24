class EnumMeta(type):
    def __new__(meta, name, bases, classdict):
        cls = super().__new__(meta, name, bases, classdict)
        cls._member_map_ = {}
        for key, value in classdict.items():
            if not key.startswith('__'):
                cls._member_map_[key] = value
        return cls

class Enum(EnumMeta):
    pass

