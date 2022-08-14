from random import random

notes = ["do", "re", "mi", "fa", "sol", "la", "ti"]

practice = [notes[int(random()*len(notes))] for _ in range(20)]

print(practice)
