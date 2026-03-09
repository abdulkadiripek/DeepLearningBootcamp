# =============================================================================
# SECTION 1: DECORATORS
# =============================================================================
# Decorator'lar, bir fonksiyonun davranışını değiştirmek veya genişletmek için
# kullanılan özel fonksiyonlardır. Wrapper pattern kullanarak mevcut fonksiyona
# yeni özellikler ekleyebiliriz.

print("="*60)
print("SECTION 1: DECORATORS")
print("="*60)

def my_decorator(func):
    """
    Fonksiyonu sarmalayan (wrap) bir decorator.
    Orijinal fonksiyondan önce ve sonra ek işlemler yapar.
    """
    def wrapper():
        print("Wrapper function executed.")
        func()  # Orijinal fonksiyon çağrılıyor
        print("wrapper function executed.")
    
    return wrapper

@my_decorator
def hello_world():
    """Basit bir selamlaşma fonksiyonu."""
    print("Hello World")

# Decorator sayesinde hello_world fonksiyonu artık wrapper ile sarmalanmış durumda
hello_world()



# =============================================================================
# SECTION 2: PROPERTY DECORATORS
# =============================================================================
# @property decorator'ı, class'larda getter, setter ve deleter metodları
# oluşturmak için kullanılır. Bu sayede encapsulation ve data validation
# sağlanabilir.

print("="*60)
print("SECTION 2: PROPERTY DECORATORS")
print("="*60)

# -------------------------------------------------------------------------
# ESKİ YÖNTEM: Getter ve Setter Metodları
# -------------------------------------------------------------------------
# Bu yöntem hala çalışır ama modern Python'da @property kullanımı tercih edilir.

class Person2:
    """Eski yöntem ile encapsulation örneği."""
    
    def __init__(self, name, age):
        self.__name = name  # Private attribute
        self.__age = age    # Private attribute
    
    def get_name(self):
        """Name getter metodu."""
        return self.__name
    
    def set_name(self, new_name):
        """Name setter metodu."""
        self.__name = new_name
        return f"Your new name is {self.__name}"
    
    def get_age(self):
        """Age getter metodu."""
        return self.__age
    
    def set_age(self, new_age):
        """Age setter metodu."""
        self.__age = new_age
        return f"Your new age is {self.__age}"

# Person2 class'ı kullanım örneği
Kadir = Person2("Abdulkadir", 22)
print(Kadir.get_name())
print(Kadir.set_name("Kadir"))
print(Kadir.get_name())
print(Kadir.get_age())
print(Kadir.set_age(23))



# -------------------------------------------------------------------------
# MODERN YÖNTEM: @property Decorator Kullanımı
# -------------------------------------------------------------------------
# @property ile property'lere doğrudan erişim sağlanır, arka planda
# getter/setter metodları çalışır.

class Animal:
    """@property decorator kullanımı örneği."""
    
    def __init__(self, name, age):
        self.__name = name  # Private attribute
        self.__age = age    # Private attribute

    @property  # Getter: cat.name şeklinde erişim sağlar
    def name(self):
        """Name property'sinin getter metodu."""
        return self.__name
    
    @name.setter  # Setter: cat.name = "yeni_isim" şeklinde atama yapar
    def name(self, value):
        """Name property'sinin setter metodu."""
        # Burada artık kuralları biz belirliyoruz
        self.__name = value

    @name.deleter  # Deleter: del cat.name şeklinde silme işlemi yapar
    def name(self):
        """Name property'sinin deleter metodu."""
        self.__name = None

# Animal class'ı kullanım örneği
cat = Animal("Tom", 4)
print(cat.name)  # Getter çalışır

cat.name = "Tom Kedi"  # Setter çalışır
print(cat.name)

del cat.name  # Deleter çalışır
print(cat.name)


# -------------------------------------------------------------------------
# DATA VALIDATION ile @property Kullanımı
# -------------------------------------------------------------------------
# @property decorator'ı ile veri doğrulama (validation) yapabiliriz.
# Bu sayede geçersiz değerlerin atanması engellenir.

class Person:
    """Data validation ile @property kullanımı örneği."""
    
    def __init__(self, name, age):
        self.__name = name  # Private attribute
        self.__age = age    # Private attribute

    @property
    def name(self):
        """Name property'sinin getter metodu."""
        return "Your name is:" + self.__name
    
    @name.setter
    def name(self, value):
        """Name property'sinin setter metodu - validasyon içerir."""
        # Tip kontrolü
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        # Uzunluk kontrolü
        if len(value) <= 2:
            raise ValueError("Name must be longer.")
        self.__name = value

    @property
    def age(self):
        """Age property'sinin getter metodu."""
        return self.__age
    
    @age.setter
    def age(self, value):
        """Age property'sinin setter metodu - validasyon içerir."""
        # Tip kontrolü
        if not isinstance(value, int):
            raise ValueError("Age must be intager.")
        # Değer aralığı kontrolü
        if value < 0 or value > 150:
            raise ValueError("Age is not accepted.")
        self.__age = value

# Person class'ı kullanım örneği - validasyon çalışır
Ozge = Person("Özge", 22)
Ozge.name = "Özge Yalçinkaya"  # Validasyondan geçer
print(Ozge.name)

Ozge.age = 48  # Validasyondan geçer
print(Ozge.age)




# =============================================================================
# SECTION 3: STATIC METHODS
# =============================================================================
# @staticmethod, class'a ait ama self veya cls parametresi gerektirmeyen
# metodlar için kullanılır. Bu metodlar class instance'ı olmadan da çağrılabilir.
# Genellikle utility fonksiyonları için kullanılır.

print("="*60)
print("SECTION 3: STATIC METHODS")
print("="*60)

class MathOperations:
    """Matematiksel işlemler için static metodlar içeren class."""
    
    @staticmethod
    def add(x, y):
        """
        İki sayıyı toplar.
        Static metod olduğu için self veya cls parametresi gerektirmez.
        """
        return x + y

# Static metod iki şekilde çağrılabilir:
# 1. Class adı ile doğrudan
print(MathOperations.add(3, 5))

# 2. Instance oluşturarak
math = MathOperations()
print(math.add(10, 20))



# =============================================================================
# SECTION 4: CLASS METHODS
# =============================================================================
# @classmethod, class'ın kendisi ile çalışan metodlar için kullanılır.
# İlk parametre olarak cls (class) alır. Alternative constructor (fabrika metodu)
# oluşturmak ve class variable'lara erişmek için kullanılır.

print("="*60)
print("SECTION 4: CLASS METHODS")
print("="*60)

class Pizza:
    """Class method kullanımı ve alternative constructor örneği."""
    
    # Class variable - tüm Pizza instance'ları için ortaktır
    total_pizzas = 0

    def __init__(self, ingredients):
        """Pizza constructor'ı."""
        self.ingredients = ingredients
        Pizza.total_pizzas += 1  # Her pizza oluşturulduğunda sayaç artar

    @classmethod
    def margherita(cls):
        """
        Margherita pizza oluşturan alternative constructor.
        cls parametresi Pizza class'ını temsil eder.
        """
        return cls(["peynir", "sucuk", "zeytin"])
    
    @classmethod
    def pepperoni(cls):
        """
        Pepperoni pizza oluşturan alternative constructor.
        """
        return cls(["peynir", "sucuk", "domates"])
    
    @classmethod
    def get_total_pizzas(cls):
        """Oluşturulan toplam pizza sayısını döndürür."""
        return cls.total_pizzas

# Class method'ları kullanarak pizza oluşturma
pizzas = Pizza.margherita()  # Alternative constructor kullanımı
print(Pizza.get_total_pizzas())  # Toplam: 1
print(pizzas.ingredients)

pizzas2 = Pizza.pepperoni()  # Alternative constructor kullanımı
print(Pizza.get_total_pizzas())  # Toplam: 2
print(pizzas2.ingredients)



# =============================================================================
# SECTION 5: ABSTRACT METHODS (SOYUT METODLAR)
# =============================================================================
# Abstract Base Class (ABC) kullanarak soyut class'lar oluşturabiliriz.
# @abstractmethod ile işaretlenen metodlar, alt class'larda mutlaka
# implement edilmek zorundadır. Bu sayede bir arayüz (interface) tanımlanır.

print("=" * 60)
print("SECTION 5: ABSTRACT METHOD")
print("=" * 60)

from abc import ABC, abstractmethod

class Hayvanlar(ABC):
    """
    Soyut (Abstract) Hayvanlar class'ı.
    Bu class'tan direkt instance oluşturulamaz.
    Alt class'lar tüm abstract metodları implement etmek zorundadır.
    """
    
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def sound(self) -> str:
        """Hayvanın çıkardığı ses - alt class'larda implement edilmeli."""
        pass

    @abstractmethod
    def move(self) -> str:
        """Hayvanın hareket şekli - alt class'larda implement edilmeli."""
        pass

    @abstractmethod
    def sleep(self) -> str:
        """Hayvanın uyuma şekli - alt class'larda implement edilmeli."""
        pass

class Dog(Hayvanlar):
    """
    Hayvanlar abstract class'ından türetilen Dog class'ı.
    Tüm abstract metodlar implement edilmek zorundadır.
    """
    
    def sound(self):
        """Köpeğin çıkardığı ses."""
        return "Hav hav"
    
    def move(self):
        """Köpeğin hareket şekli."""
        return "Koş"
    
    def sleep(self):
        """Köpeğin uyuma şekli."""
        return "Uyudu"

# Dog instance'ı oluşturma ve kullanma
barley = Dog("Barley")
print(barley.move())


# =============================================================================
# SECTION 6: OVERLOADING (AŞIRI YÜKLEME)
# =============================================================================
# Python'da gerçek method overloading yoktur, ancak @overload decorator'ı
# ile type hint vererek IDE ve type checker'lar için imza (signature) tanımlayabiliriz.
# Bu sayede farklı parametre kombinasyonları için tip desteği sağlanır.

print("=" * 60)
print("SECTION 6: OVERLOADING")
print("=" * 60)

from typing import overload, Union

def example(x: int):
    """Tip belirtilmiş basit bir fonksiyon."""
    return x * 2

# Böyle de çalışır ama altında bir uyarı verir (tip uyumsuzluğu)
# print(example("Abdulkadir"))

class Calculator:
    """Method overloading örneği içeren hesap makinesi class'ı."""

    # add metodu için overload tanımlamaları (type hint için)
    @overload
    def add(self, a: int, b: int) -> int:
        """İki sayı toplama imzası."""
        ...

    @overload
    def add(self, a: int, b: int, c: int) -> int:
        """Üç sayı toplama imzası."""
        ...

    def add(self, a: int, b: int, c: int | None = None) -> int:
        """
        İki veya üç sayıyı toplayan metod.
        Gerçek implementasyon burada yapılır.
        """
        if c is None:
            return a + b
        else:
            return a + b + c
    
    # process metodu için overload tanımlamaları
    @overload
    def process(self, value: str) -> str:
        """String değer işleme imzası."""
        ...
    
    @overload
    def process(self, value: int) -> int:
        """Integer değer işleme imzası."""
        ...

    def process(self, value: Union[int, str]) -> Union[int, str]:
        """
        Farklı tipleri işleyen metod.
        Integer ise 2 ile çarpar, string ise büyük harfe çevirir.
        """
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
        else:
            raise ValueError("Value must be str or int.")

# Calculator kullanım örnekleri
calculator = Calculator()
print(calculator.add(10, 20, 30))  # Üç sayı toplama
print(calculator.process(10))       # Integer işleme



# =============================================================================
# SECTION 7: FINAL
# =============================================================================
# @final decorator'ı, bir metodun veya class'ın override (üzerine yazma) veya
# inherit (kalıtım) edilmesini engeller. Bu sayede kritik fonksiyonlar korunur.

print("=" * 60)
print("SECTION 7: FINAL")
print("=" * 60)

from typing import final

class BaseGame:
    """Temel oyun class'ı."""

    def start(self) -> None:
        """Oyunu başlatan metod - override edilebilir."""
        print("Game Started")

    @final
    def calculate_score(self, point: int) -> int:
        """
        Puan hesaplama metodu - @final ile işaretlendiği için
        alt class'larda override edilemez.
        """
        bonus = 100
        return point + bonus

# @final ile işaretlenmiş class - inherit edilemez
@final
class SecretAlgorithm:
    """
    Gizli algoritma class'ı.
    @final ile işaretlendiği için bu class'tan türetme yapılamaz.
    """
    
    def process(self):
        """Gizli algoritma işlemini gerçekleştirir."""
        print("Secret algorithm executed")

class MyGame(BaseGame):
    """BaseGame'den türetilmiş özel oyun class'ı."""

    def start(self) -> None:
        """start metodu override edilebilir (@final değil)."""
        print("MyGame started")

    # NOT: calculate_score metodunu override edemeyiz çünkü @final ile işaretli
    # Aşağıdaki kod açılırsa type checker uyarı verir:
    """
    def calculate_score(self, point: int) -> int:
        return point * 2
    """

# MyGame kullanımı
game = MyGame()
game.start()
print(game.calculate_score(100))  # Parent class'taki final metod çalışır

# SecretAlgorithm kullanımı
secret_algorithm = SecretAlgorithm()
secret_algorithm.process()


# =============================================================================
# SECTION 8: OVERRIDE (ÜZERİNE YAZMA)
# =============================================================================
# @override decorator'ı, bir metodun parent class'tan override edildiğini
# açıkça belirtmek için kullanılır. Bu sayede kod daha okunabilir olur ve
# yanlış override durumlarında type checker uyarı verir.

print("=" * 60)
print("SECTION 8: OVERRIDE")
print("=" * 60)

from typing import override

class Shape:
    """Temel şekil class'ı."""

    def area(self) -> float:
        """Şeklin alanını hesaplar - alt class'larda override edilmeli."""
        return 0.0
    
    def perimeter(self) -> float:
        """Şeklin çevresini hesaplar - alt class'larda override edilmeli."""
        return 0.0

class Rectangle(Shape):
    """Dikdörtgen şekli class'ı."""

    def __init__(self, width: float, height: float):
        """Dikdörtgen oluşturur."""
        self.width = width
        self.height = height

    @override
    def area(self) -> float:
        """
        Dikdörtgenin alanını hesaplar.
        @override decorator'ı bu metodun parent class'tan geldiğini belirtir.
        """
        return self.height * self.width

    @override
    def perimeter(self) -> float:
        """
        Dikdörtgenin çevresini hesaplar.
        @override decorator'ı bu metodun parent class'tan geldiğini belirtir.
        """
        return (self.height + self.width) * 2

# Rectangle kullanımı
rectangle = Rectangle(10, 20)
print(rectangle.area())       # Alan: 200
print(rectangle.perimeter())  # Çevre: 60


# =============================================================================
# BONUS SECTION: COMBINING DECORATORS (DECORATOR ZİNCİRLEME)
# =============================================================================
# Birden fazla decorator bir fonksiyona uygulanabilir.
# Decorator'lar alttan üste doğru uygulanır (en alttaki önce, en üstteki son).
# Bu örnekte: calculate -> other_decorator -> multiply_decorator sırasıyla çalışır.

print("=" * 60)
print("BONUS SECTION: COMBINING DECODATORS")
print("=" * 60)

def multiply_decorator(func):
    """
    Fonksiyon sonucunu 2 ile çarpan decorator.
    """
    def wrapper(x: int):
        return func(x) * 2
    return wrapper

def other_decorator(func):
    """
    Fonksiyon sonucunu 4 ile çarpan decorator.
    """
    def wrapper(x: int):
        return func(x) * 4
    return wrapper

# Decorator'lar alttan üste doğru uygulanır:
# 1. calculate(10) çağrılır -> 10 * 2 = 20
# 2. other_decorator uygulanır -> 20 * 4 = 80
# 3. multiply_decorator uygulanır -> 80 * 2 = 160
@multiply_decorator
@other_decorator
def calculate(x: int) -> int:
    """Sayıyı 2 ile çarpan basit fonksiyon."""
    return x * 2

print(calculate(10))  # Sonuç: 160