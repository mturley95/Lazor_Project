import random


class Grid3x3:
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return str(self.values)


# Create an example 9x9 grid
grid9x9 = [[random.randint(1, 9) for _ in range(9)] for _ in range(9)]

# Iterate through each 3x3 space and replace it with an instance of the Grid3x3 class
for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        if i == 0 and j == 0:
            values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        elif i == 3 and j == 0:
            values = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        else:
            values = [[random.randint(1, 9) for _ in range(3)]
                      for _ in range(3)]
        for r in range(3):
            for c in range(3):
                grid9x9[i+r][j+c] = values[r][c]

# Print the modified 9x9 grid
for row in grid9x9:
    print(row)
