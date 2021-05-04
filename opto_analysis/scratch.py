from dataclasses import dataclass

def triple(input: int) -> int:
    """
    Triples a number
    Args:
        input: select any number
    Returns:
        output (int): the number multiplied by 3
    
    """
    output = int(input * 3) 
    return output

@dataclass
class Person:
    name: str = "John Doe"
    age: int = 0

    def __post_init__(self): 
        self.age = round(self.age)

    def report(self):
        print(self.name)
        print(self.age)