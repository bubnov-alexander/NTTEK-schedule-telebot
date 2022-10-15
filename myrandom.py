import random

def randomman():
    file = open('data/Student.txt', 'r', encoding='UTF-8')
    file2 = open('data/random.txt', 'w', encoding='UTF-8')
    lines = []
    for line in file:
        lines.append(line)
    random_line = random.choice(lines)
    file2.write (" ".join(random_line))
    file.close()
