import pytest
from opto_analysis.scratch import triple, Person

def test_triple():
    input = 99.0
    output = triple(input)
    assert output==297
    assert type(output)==int

def test_Person(capsys):
    person = Person("John", 36.5)
    person.report() 
    printed_text = capsys.readouterr()
    assert printed_text.out=="John\n36\n"