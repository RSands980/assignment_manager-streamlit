
class Counter:
    def __init__(self, start: int = 0, step: int = 1) -> None:
        self.value = start
    
    def increment(self):
        self.value += 1
    
    def current(self) -> int:
        return self.value
    
    def increment_2(self):
        self.value += 2



c = Counter( start = 5) # creating an object from the Counter class

c1 = Counter( start = 10) # creating an object from the Counter class

c1.increment()


print(f"{c1.current()}")
print(f'{c.current()}')

c.increment_2()

print(f'{c.current()}')
print(f'{c1.current()}')
