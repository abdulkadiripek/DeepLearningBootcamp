# Section - 1: Decorators

print("="*60)
print("SECTION 1: DECORATORS")
print("="*60)

def my_decorator(func):

    def wrapper():
        print("Wrapper function executed.")
        func()
        print("wrapper function executed.")

    return wrapper

@my_decorator
def hello_world():
    print("Hello World")

hello_world()


print("="*60)
print("SECTION 2: PROPERTY DECORATORS")
print("="*60)

#data validation için kullanılabilir. (encapsulation)

# BUNLAR ESKİ ALIŞKANLIKLAR DAHA MODERNİ VAR.
class Person:
    def __init__(self,name,age):
        self.__name = name
        self.__age  = age
    
    def get_name(self):
        return self.__name
    
    def set_name(self,new_name):
        self.__name = new_name
        return f"Your new name is {self.__name}"
    
    def get_age(self):
        return self.__age
    
    def set_age(self,new_age):
        self.__age = new_age
        return f"Your new age is {self.__age}"

Kadir = Person("Abdulkadir", 22)
print(Kadir.get_name())
print(Kadir.set_name("Kadir"))
print(Kadir.get_name())
print(Kadir.get_age())
print(Kadir.set_age(23))

print

class Animal:
    def __init__(self,name,age):
        self.__name = name
        self.__age = age

    @property            # GETTER
    def name(self):
        return self.__name
    
    # Burada artık kuralları biz belirliyoruz.
    @name.setter         # SETTER
    def name(self,value):
        self.__name = value

cat = Animal("Tom",4)
print(cat.name)

cat.name = "Tom Kedi"
print(cat.name)
