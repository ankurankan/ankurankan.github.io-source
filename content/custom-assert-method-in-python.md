---
layout: post
title: Custom Exceptions in python
date: 2014-06-03 08:19
comments: true
categories: python testing unittest assert exceptions
---
While writing tests we often need to compare objects defined by
us and we then have to compare each attribute of the object one
by one.

Let's take an example of a simple `Car` class. The Car object has
two attributes `speed` and `color`.

```python
class Car:
    def __init__(self, speed, color):
        self.speed = speed
        self.color = color
```

So if you try writing test for it using `unittest.TestCase.AssertEqual`
method.

```python
import unittest

class TestCar(unittest.TestCase):
    def test_car_equal(self):
       car1 = Car(40, 'red')
       car2 = Car(40, 'red')
       self.assertEqual(car1, car2) 
```
If you now try to run this test, the test case will fail.
```python
    self.assertEqual(Car(40, 'red'), Car(40, 'red'))
AssertionError: <assert.Car object at 0x7f8edbc078d0> != <assert.Car object at 0x7f8edbc07908>
```
This is because unittest doesn't know how to compare two `Car` objects.

So, we have a two options to make this work:  
1. We can define a `__eq__` method in `Car` class.  
2. We can create a custom assertion class.  

### 1. `__eq__` method

`__eq__` is one of the rich comparison methods. Whenever `==` is used on any object
its `__eq__` method is called. For example `car1 == car2` internally calls `car1.__eq__(car2)`.

Our new car class:
```python
class Car:
   def __init__(self, speed, color):
      self.speed = speed
      self.color = color
  
   def __eq__(self, another_car):
       if type(self)==type(another_car) and self.speed==another_car.speed and
               self.color==another_car.color:
           return True
        else:
           return False
```
And now the same test passes. But when `car1` is not equal to `car2`, the test fails
and the output is not at all informative about why the test failed. It simply prints:
```
    self.assertEqual(car1, car2)
AssertionError: <Car object at 0x7f1f86af6a20> != <Car object at 0x7f1f86af6a58>
```

So, one drawback of this approach is that we can't show some message about why the 
equality failed. Showing an error message by printing it wouldn't be a good design
because when the user does a simple `car1 == car2` and if they are not equal, `__eq__`
would still print the details of why they are not equal.

Now, we see the second approach in which we can give a detailed message about why 
the equality failed.

### 2. Custom assertion class
We can write a custom assertion class for out `car` class.
```python
class AssertCarEqual:
    def assert_car_equal(self, car1, car2):
        if type(car1) != type(car2):
            raise AssertionError("car1 is of type: ", type(car1), " and car2 is of type: ", type(car2))
        elif car1.speed != car2.speed:
            raise AssertionError("speed of car1: ", car1.speed, " and speed of car2: ", car2.speed)
        elif car1.color != car2.color:
            raise AssertionError("color of car1: ", car1.color, " and color of car2: ", car2.color)
```
And modifying the test like this:
```python
class TestCar(unittest.TestCase, AssertCarEqual):
    def test_car_equal(self):
        car1 = car.Car(40, 'blue')
        car2 = car.Car(40, 'red')
        self.assert_car_equal(car1,car2)
```
Now when we run the test, the test fails and gives a message about
why the test failed.
```
    raise AssertionError("color of car1: ", car1.color, " and color of car2: ", car2.color)
AssertionError: ('color of car1: ', 'blue', ' and color of car2: ', 'red')
```
