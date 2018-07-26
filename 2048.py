import numpy
import random

class My_2048:
    def __init__(self, size=4):
        self.size = size
        self.matrix = numpy.zeros((self.size, self.size))
        # random_add a number in inital process
        self.random_add(self.matrix)
        self.game_start('Input "w, a, s, d" to control your action, Input "stop" to quit')

    def random_add(self, matrix):
        # generate a random number in (2,4)
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

        if not self.matrix_equal(new_matrix, self.matrix):
            # if we can't find similar number to sum, we should return the origin matrix
            if not self.random_add(new_matrix):
                self.game_over('game over')
        return self.matrix
    
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
    
    def game_start(self, message):
        print(message)

    def game_over(self, message):
        print(message)
    
    def sum_similar(self, col):
        if len(col) < 2:
            return col
        else:
            for index in range(len(col)-1):
                # we should sum the similar number from tail to head, and only sum once a time.
                if col[-(index+1)] == col[-(index+1)-1]:
                    col[-(index+1)-1] = col[-(index+1)] + col[-(index+1)-1]
                    col.pop(-(index+1))
                    break
            return col

    def matrix_equal(self, matrix_x, matrix_y):
        '''
        this method used to judge if matrix_x equel to matrix_y
        '''
        flat_x = matrix_x.flat
        flat_y = matrix_y.flat

        for index in range(self.size*self.size):
            if flat_x[index] != flat_y[index]:
                return False
        return True


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
    
