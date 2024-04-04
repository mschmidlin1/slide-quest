class SqMeta(type):
    """
    SqMeta enforces the draw() and update() methods on whatever classes inherit from it.
    """
    def __new__(cls, name, bases, attrs):
        # Check for the 'draw' method
        if 'draw' not in attrs or not callable(attrs['draw']):
            raise TypeError(f"Class {name} lacks a 'draw' method or it's not callable")
        
        # Check for the 'update' method
        if 'update' not in attrs or not callable(attrs['update']):
            raise TypeError(f"Class {name} lacks an 'update' method or it's not callable")
        
        return super().__new__(cls, name, bases, attrs)



class SqScreenMeta(SqMeta):
    _registry = []

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        cls._registry.append(new_class)
        return new_class

    @classmethod
    def get_registered_classes(cls):
        return cls._registry













class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]












# class TestClass(metaclass=SingletonMeta):
#     def __init__(self):
#         self.x = 1
#         self.name = 'name'