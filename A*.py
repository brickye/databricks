# Databricks notebook source
import queue
import copy 

def create_tile_puzzle(rows, cols):
    board = [[(j+i*cols) for j in range(1,cols+1)] for i in range(rows)]
    board[rows-1][cols-1]=0
    return TilePuzzle(board)

class TilePuzzle(object):
    def __init__(self, board):
        self.board = board
        self.rowL = len(board)
        self.colL = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        for row in range(self.rowL):
            if 0 in self.board[row]:
                col=self.board[row].index(0)
                break
        
        if row>0 and direction=='up':
            cur = self.board[row-1][col]
            self.board[row-1][col]=0
            self.board[row][col]=cur
            return True
        
        if row<self.rowL-1 and direction=='down':
            cur = self.board[row+1][col]
            self.board[row+1][col]=0
            self.board[row][col]=cur
            return True
        
        if col>0 and direction=='left':
            cur = self.board[row][col-1]
            self.board[row][col-1]=0
            self.board[row][col]=cur
            return True
        
        if col<self.colL-1 and direction=='right':
            cur = self.board[row][col+1]
            self.board[row][col+1]=0
            self.board[row][col]=cur
            return True
        return False
        
    def scramble(self, num_moves):
        for move in range(num_moves): self.perform_move(random.choice(['up', 'down', 'left', 'right']))

    def is_solved(self):
        return self.board==create_tile_puzzle(self.rowL, self.colL).get_board()

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        for direction in ['up', 'down', 'left', 'right']:
            cur = self.copy()
            if cur.perform_move(direction): yield(direction, cur)

    def find_solutions_iddfs(self):
        limit=0; result=[]
        while len(result)==0:
            limit+=1
            result=list(self.iddfs_helper(limit, result, set(tuple(tuple(i) for i in self.board))))
        for result in result: yield result

    def iddfs_helper(self, limit, moves, max_move):
        if self.is_solved(): yield moves
        if len(moves)<limit:
            for (move, cur) in self.successors():
                new_move = tuple(tuple(i) for i in cur.board)
                if new_move not in max_move:
                    next_move = copy.deepcopy(max_move)
                    next_move.add(new_move)
                    for result in cur.iddfs_helper(limit, moves+[move], next_move):
                        yield result

    # f(n) = g(n) + h(n)
    # g(n) = distance from current node to root node (sum of edge costs from start to n)
    # h(n) = number od misplaced tiles by comparing current state to goal state (estimate of lowest cost path from n to goal)

    def find_solution_a_star(self):
        result = queue.PriorityQueue()
        reached = set()
        result.put((self.heuristic(), 0, [], self))

        while (not result.empty()): 
            startition = result.get(); size = 3 
            if tuple(tuple(i) for i in startition[size].board) in reached: continue
            else: reached.add(tuple(tuple(i) for i in startition[size].board))
            if startition[size].is_solved(): return startition[size-1]
            for (move, cur) in startition[size].successors():
                if tuple(tuple(i) for i in cur.board) not in reached:
                    result.put((startition[size-2]+cur.heuristic()+1, startition[size-2]+1, startition[size-1]+[move], cur))

    def heuristic(self):
        manhattan_distance = 0
        for x in range(self.rowL):
            for y in range(self.colL):
                if self.board[x][y]!=0:
                    v=self.adjust(x,y)
                    dx, dy=self.iterate(v)
                    manhattan_distance+=abs(x-dx) + abs(y-dy)
        return manhattan_distance
    
    def adjust(self, row, col):
        if row==self.rowL-1 and col==self.colL-1: return 0
        return row*self.rowL+col+1

    def iterate(self, value):
        for dx in range(self.rowL):
            for dy in range(self.colL):
                if self.board[dx][dy]==value:
                    return dx, dy
                  

# b = [[4,1,2], [0,5,3], [7,8,6]]
# p = TilePuzzle(b)
# print(p.find_solution_a_star())

b = [[1,3,2], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
print(p.find_solution_a_star())

# COMMAND ----------


