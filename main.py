import sys

strings = []
file = open(sys.argv[1], "r")
while True:
    line = file.readline()
    if not line:
        break
    strings.append(line.strip())
file.close()

print(strings)
