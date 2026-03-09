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
class Person2:
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

Kadir = Person2("Abdulkadir", 22)
print(Kadir.get_name())
print(Kadir.set_name("Kadir"))
print(Kadir.get_name())
print(Kadir.get_age())
print(Kadir.set_age(23))


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

    @name.deleter        # DELETER
    def name(self):
        self.__name = None    

cat = Animal("Tom",4)
print(cat.name)

cat.name = "Tom Kedi"
print(cat.name)

del cat.name
print(cat.name)

class Person:
    def __init__(self,name,age):
        self.__name = name
        self.__age  = age

    @property
    def name(self):
        return "Your name is:" + self.__name
    
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise ValueError("Name must be a string.")
        if len(value)<=2:
            raise ValueError("Name must be longer.")
        self.__name = value

    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self,value):
        if not isinstance(value,int):
            raise ValueError("Age must be intager.")
        if value < 0 or value > 150 :
            raise ValueError("Age is not accepted.")
        self.__age=value
    
Ozge = Person("Özge",22)
Ozge.name = "Özge Yalçinkaya"
print(Ozge.name)

Ozge.age = 48
print(Ozge.age)



print("="*60)
print("SECTION 3: STATIC METHODS")
print("="*60)


class MathOperations:
    
    @staticmethod
    def add(x,y):
        return x+y
    
print(MathOperations.add(3,5))
math = MathOperations()
print(math.add(10,20))


print("="*60)
print("SECTION 4: CLASS METHODS")
print("="*60)

#@classmethod

# alternative constructor

class Pizza:
    total_pizzas = 0

    def __init__(self,ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    @classmethod    
    def margherita(cls):
        return cls(["peynir", "sucuk", "zeytin"])
    
    @classmethod    
    def pepperoni(cls):
        return cls(["peynir", "sucuk", "domates"])
    
    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas

pizzas = Pizza.margherita()
print(Pizza.get_total_pizzas())
print(pizzas.ingredients)

pizzas2 = Pizza.pepperoni()
print(Pizza.get_total_pizzas())
print(pizzas2.ingredients)


print("=" * 60)
print("SECTION 5: ABSTRACT METHOD")
print("=" * 60)

from abc import ABC, abstractmethod

class Hayvanlar(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def sound(self) -> str:
        pass

    @abstractmethod
    def move(self) -> str:
        pass

    @abstractmethod
    def sleep(self) -> str:
        pass

class Dog(Hayvanlar):
    def sound(self):
        return "Hav hav"
    
    def move(self):
        return "Koş"
    
    def sleep(self):
        return "Uyudu"

barley = Dog("Barley")
print(barley.move())

# overloading, overriding, final

print("=" * 60)
print("SECTION 6: OVERLOADING")
print("=" * 60)

from typing import overload, Union

def example(x:int):
    return x * 2

# Böyle de çalışır ama altında bir uyarı verir.
# print(example("Abdulkadir"))

class Calculator:

    @overload
    def add(self,a:int,b:int) -> int:
        ...

    @overload
    def add(self,a:int,b:int,c:int) -> int:
        ...

    def add(self, a:int, b:int, c:int | None=None) -> int:
        if c is None:
            return a+b
        else:
            return a+b+c
        
    @overload
    def process(self,value:str) -> str:
        ...
    
    @overload
    def process(self,value:int) -> int:
        ...

    def process(self,value:Union[int,str]) -> Union[int,str]:
        if isinstance(value,int):
            return value * 2
        elif isinstance(value,str):
            return value.upper()
        else:
            raise ValueError("Value must be str or int.")
        

calculator = Calculator()
print(calculator.add(10,20,30))
print(calculator.process(10))