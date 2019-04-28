# https://www.ploggingdev.com/2016/11/n-queens-solver-in-python-3/
"""
Solve N-Queen problem by using BFS in python3
2019. 04. 28. Hyeongon Simon Kim
Kookmin Univ. Computer Science, Seoul, Republic of Korea
"""

import queue
import copy

def take_input():
    """Accepts the size of the chess board"""

    while True:
        try:
            size = int(input('What is the size of the chessboard? n = \n'))
            if size == 1:
                print("Trivial solution, choose a board size of at least 4")
            if size <= 3:
                print("Enter a value such that size>=4")
                continue
            return size
        except ValueError:
            print("Invalid value entered. Enter again")


def get_board(size):
    """Returns an n by n board"""
    board = [0] * size
    for ix in range(size):
        board[ix] = [0] * size
    return board


def print_solutions(solutions, size):
    """Prints all the solutions in user friendly way"""
    for sol in solutions:
        for row in sol:
            print(row)
        print()


def is_safe_dfs(board, row, col, size):
    """Check if it's safe to place a queen at board[x][y]"""

    """같은 행에 놓인 퀸이 있는지 검사"""
    for iy in range(col):
        if board[row][iy] == 1:
            return False

    """좌측하단 대각선으로 내려가며 퀸이 있는지 검사"""
    ix, iy = row, col
    while ix >= 0 and iy >= 0:
        if board[ix][iy] == 1:
            return False
        ix -= 1
        iy -= 1

    """우측하단 대각선으로 내려가며 퀸이 있는지 검사"""
    jx, jy = row, col
    while jx < size and jy >= 0:
        if board[jx][jy] == 1:
            return False
        jx += 1
        jy -= 1

    return True


def is_safe_bfs(locationQueen):
    """
    locationQueen에 같은 숫자가 존재하면 같은 열에 존재
    너비우선으로 접근 중이므로 같은 행에는 존재할 수 없음
    list의 index숫자의 차와 값의 차가 동일하다면 대각선상에 존재
    """

    """같은 열에 놓인 퀸이 있는지 검사"""
    if len(locationQueen) > len(set(locationQueen)):
        return False

    """대각선에 놓인 퀸이 있는지 검사"""
    for i in range(len(locationQueen)):
        for j in range(i + 1, len(locationQueen)):
            if (j - i) == (locationQueen[j] - locationQueen[i]) or (j - i) == (locationQueen[i] - locationQueen[j]):
                return False

    return True


def print_solutions_bfs(solutions, size):
    """BFS를 위해 정답이 되는 해당 행의 열만 담긴 1차원 배열이 담긴 solutions를 완전한 형태로 출력하는 함수"""
    queen = [1]
    noneQueen = [0]
    for sol in solutions:
        for i in sol:
            print((noneQueen * i) + queen + (noneQueen * (size - i - 1)))
        print()


def solve_dfs(board, col, size):
    """Use backtracking to find all solutions"""

    """재귀를 수행하며 유망성검사를 통해 답이 될 가능성이 있는지 확인한다. 없다면 즉각 직전단계로 돌아가 복잡도를 줄인다."""
    # base case
    if col >= size:
        return

    for i in range(size):
        
        """만약 현재 지점이 퀸을 놓을 수 있는 위치라면"""
        if is_safe_dfs(board, i, col, size):
            
            """일단 퀸을 놓는다"""
            board[i][col] = 1
            
            """끝까지 탐색하는데 성공했다면 해당 board를 솔루션으로 추가한다"""
            if col == size - 1:
                add_solution(board)
                board[i][col] = 0
                return
            
            """DFS재귀구조를 통해 다음 열에 퀸을 놓을 수 있는지 확인한다"""
            solve_dfs(board, col + 1, size)
            
            # backtrack
            """DFS재귀구조를 수행하다가 실패했거나 성공적으로 솔루션을 찾았다면, 직전의 위치로 옮겨가서 다음 for loop로 진입한다(백트래킹)"""
            board[i][col] = 0


def solve_bfs(size):
    """출력함수를 별도로 사용해야한다."""

    """
    너비우선탐색을 위해 FIFO의 큐를 사용한다.
    큐에는 크기가 최대 size인 1차원 배열들이 담기고, index가 보드에서의 행, 해당 index의 데이터값이 열을 의미한다.
    """
    q = queue.Queue()
    
    """빈 보드의 1행에는 자유롭게 퀸을 배치할 수 있으므로, 초기 시작 퀸들을 배치한다."""
    for i in range(size):
        start_board = [i]
        saved_board = copy.deepcopy(start_board)
        q.put(saved_board)

    """큐가 비어있지 않다면 무한 반복한다."""
    while not q.empty():

        """큐에서 배열을 하나 꺼낸다."""
        queue_board = q.get()

        """만약 꺼낸 배열의 길이가 size라면, 정답 배열이므로 solution으로 추가한다."""
        if len(queue_board) == size:
            add_solution(queue_board)

        """그게 아니라면 새로운 행에 좌측 열부터 퀸을 배치하며 유망성검사를 진행하고, 통과한 배열은 큐에 추가한다"""
        else:
            for k in range(size):
                new_board = queue_board + [k]
                if is_safe_bfs(new_board):
                    saved_new_board = copy.deepcopy(new_board)
                    q.put(saved_new_board)


def add_solution(board):
    """Saves the board state to the global variable 'solutions'"""
    global solutions
    saved_board = copy.deepcopy(board)
    solutions.append(saved_board)


size = take_input()

board = get_board(size)

solutions = []

solve_bfs(size)

print_solutions_bfs(solutions, size)

"""

solve_dfs(board, 0, size)

print_solutions(solutions, size)

"""

print("Total solutions = {}".format(len(solutions)))
