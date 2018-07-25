import numpy
import random

class My_2048:
    def __init__(self, size=4):
        self.size = size
        self.matrix = numpy.zeros((self.size, self.size))
        # self.matrix = numpy.array([[0,1,0],
        #                         [1,0,3],
        #                         [0,1,2]])

    def random_add(self, matrix):
        index_list = []
        for index, ele in enumerate(matrix.flat):
            if ele == 2048:
                return self.game_over('success')
            if ele == 0:
                index_list.append(index)

        if len(index_list) > 0:
            index = random.sample(index_list, 1)[0]
            matrix[index//self.size, index%self.size] = random.randrange(2, 4, 2)
            self.matrix = matrix
            return True
        else:
            return False

    def down_sum(self):
        new_matrix = numpy.zeros((self.size, self.size))
        for col in range(self.size):
            new_col = []
            for num in self.matrix[..., col]:
                if num != 0:
                    new_col.append(num)

            new_col = self.sum_similar(new_col)
            new_col = [0] * (self.size - len(new_col)) + new_col
            new_matrix[..., col] = new_col
            
        if self.random_add(new_matrix):
            return self.matrix
        else:
            self.game_over('game over')
    
    def up_sum(self):   
        self.matrix = numpy.vstack([row for row in self.matrix[::-1, ...]])
        self.down_sum()
        self.matrix = numpy.vstack([row for row in self.matrix[::-1, ...]])
        return self.matrix

    def right_sum(self):
        self.matrix = self.matrix.T
        self.down_sum()
        self.matrix = self.matrix.T
        return self.matrix

    def left_sum(self):
        self.matrix = self.matrix.T
        self.up_sum()
        self.matrix = self.matrix.T
        return self.matrix
    
    def game_over(self, message):
        print(message)
    
    def sum_similar(self, col):
        if len(col) < 2:
            return col
        else:
            if col[0] == col[1]:
                col[1] = col[0] + col[1]
                col.pop(0)
            return col


my2048 = My_2048()
while True:
    action = input('Chose you action\n>>>')
    map_action = {
        'w': 'up_sum',
        'a': 'left_sum',
        's': 'down_sum',
        'd': 'right_sum'
    }
    if action == 'stop':
        break
    if map_action.get(action, None):
        f = getattr(my2048, map_action.get(action))
        print(f())
    else:
        print('Wrong action')
    
