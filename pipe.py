# pipe.py: Projeto de Inteligência Artificial 2023/2024.

# Grupo 71:
# 106324 - Cristiano Pantea
# 106074 - Rodrigo Perestrelo

import sys
import numpy as np
from search import (
    Problem,
    Node,
    breadth_first_tree_search,
)

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, cells):
        self.cells = cells
        self.rows = len(cells)
        self.cols = len(cells[0])
        self.cutBranch = False
        rotated = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.rotated = np.array(rotated)

    def isOnBoard(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return True
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (self.isOnBoard(row, col)):
            return  self.cells[row][col]
        return None
    
    def compatiblePipes(self, mainTube: str, comparingPipe: str, position: str):

        if (comparingPipe == None):
            return False
        
        direction_connections = {
            'C': ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'],
            'B': ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'],
            'E': ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'],
            'D': ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']
        }
        
        connections = {
            'FC': {'C': direction_connections['C']},
            'FB': {'B': direction_connections['B']},
            'FE': {'E': direction_connections['E']},
            'FD': {'D': direction_connections['D']},
            'BC': {'C': direction_connections['C'], 'E': direction_connections['E'], 'D': direction_connections['D']},
            'BB': {'B': direction_connections['B'], 'E': direction_connections['E'], 'D': direction_connections['D']},
            'BE': {'E': direction_connections['E'], 'C': direction_connections['C'], 'B': direction_connections['B']},
            'BD': {'C': direction_connections['C'], 'D': direction_connections['D'], 'B': direction_connections['B']},
            'VC': {'E': direction_connections['E'], 'C': direction_connections['C']},
            'VB': {'D': direction_connections['D'], 'B': direction_connections['B']},
            'VE': {'E': direction_connections['E'], 'B': direction_connections['B']},
            'VD': {'D': direction_connections['D'], 'C': direction_connections['C']},
            'LH': {'E': direction_connections['E'], 'D': direction_connections['D']},
            'LV': {'C': direction_connections['C'], 'B': direction_connections['B']}
        }

        # check if the position of the second pipe is compatible with the first pipe
        if position not in connections[mainTube]:
            return False
        
        # check if the comparing pipe is compatible with the first pipe at the specified position
        if comparingPipe not in connections[mainTube][position]:
            return False
        
        return True

    def get_upperValue(self, row: int, col: int):
        return [row - 1, col, 'C']
    
    def get_lowerValue(self, row: int, col: int):
        return [row + 1, col, 'B']
    
    def get_rightValue(self, row: int, col: int):
        return [row, col + 1, 'D']
    
    def get_leftValue(self, row: int, col: int):
        return [row, col - 1, 'E']
    
    def getAdjacentPipes(self, row: int, col: int):
        piece = self.get_value(row, col)
        first_letter = piece[0]
        second_letter = piece[1]

        if first_letter == "F":
            if second_letter == "C":
                return [self.get_upperValue(row, col), ]
            elif second_letter == "B":
                return [self.get_lowerValue(row, col), ]
            elif second_letter == "E":
                return [self.get_leftValue(row, col), ]
            elif second_letter == "D":
                return [self.get_rightValue(row, col), ]
        elif first_letter == "B":
            if second_letter == "C":
                return [self.get_leftValue(row, col), self.get_upperValue(row, col), self.get_rightValue(row, col)]
            elif second_letter == "B":
                return [self.get_leftValue(row, col), self.get_lowerValue(row, col), self.get_rightValue(row, col)]
            elif second_letter == "E":
                return [self.get_upperValue(row, col), self.get_leftValue(row, col), self.get_lowerValue(row, col)]
            elif second_letter == "D":
                return [self.get_upperValue(row, col), self.get_rightValue(row, col), self.get_lowerValue(row, col)]
        elif first_letter == "V":
            if second_letter == "C":
                return [self.get_leftValue(row, col), self.get_upperValue(row, col)]
            elif second_letter == "B":
                return [self.get_lowerValue(row, col), self.get_rightValue(row, col)]
            elif second_letter == "E":
                return [self.get_leftValue(row, col), self.get_lowerValue(row, col)]
            elif second_letter == "D":
                return [self.get_upperValue(row, col), self.get_rightValue(row, col)]
        elif first_letter == "L":
            if second_letter == "H":
                return [self.get_leftValue(row, col), self.get_rightValue(row, col)]
            elif second_letter == "V":
                return [self.get_upperValue(row, col), self.get_lowerValue(row, col)]
            
    def getSurroundingCoords(self, row, col):
        return [(row - 1, col, 'C'), (row, col + 1, 'D'), (row + 1, col, 'B'), (row, col - 1, 'E')]

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        cells = [line.strip().split() for line in sys.stdin]
        cells_np = np.array(cells)
        board = Board(cells_np)
        board.board_first_approach()
        return board
    
    def __str__(self):
        """Devolve uma representação do tabuleiro em forma de string."""
        result = ""
        numRows = self.rows
        numCols = self.cols

        for i in range(numRows):
            for j in range(numCols):
                if(j == (numCols-1)):
                    result += self.cells[i][j]
                else:
                    result += self.cells[i][j] + "\t"
            if(i == (numRows-1)):
                return result
            else:
                result += '\n'
    
    def verifyBorder(self, row, col):

        board = self

        piece = board.get_value(row, col)
        board_rows = board.rows
        board_columns = board.cols

        if piece[0] == 'B':

            #Peca B na linha superior (sem ser nos cantos)
            if row == 0:
                board.cells[row][col] = 'BB'
                board.rotated[row][col] = True
            #Peca B na linha inferiorc (sem ser nos cantos)
            elif row == board_rows - 1:
                board.cells[row][col] = 'BC'
                board.rotated[row][col] = True
            #Peca B na coluna esquerda (sem ser nos cantos)
            elif col == 0:
                board.cells[row][col] = 'BD'
                board.rotated[row][col] = True
            #Peca B na coluna direita (sem ser nos cantos)
            elif col == board_columns - 1:
                board.cells[row][col] = 'BE'
                board.rotated[row][col] = True

        #Peca V
        elif piece[0] == 'V':

            #Peca V no canto superior esquerdo
            if row == 0 and col == 0:
                board.cells[row][col] = 'VB'
                board.rotated[row][col] = True
            #Peca V no canto superior direito
            elif row == 0 and col == board_columns - 1:
                board.cells[row][col] = 'VE'
                board.rotated[row][col] = True
            #Peca V no canto inferior esquerdo
            elif row == board_rows - 1 and col == 0:
                board.cells[row][col] = 'VD'
                board.rotated[row][col] = True
            #Peca V no canto inferior direito
            elif row == board_rows - 1 and col == board_columns - 1:
                board.cells[row][col] = 'VC'
                board.rotated[row][col] = True
                
        #Peca L
        elif piece[0] == 'L':

            #Peca L na linha superior ou na linha inferior
            if row == 0 or row == board_rows - 1:
                board.cells[row][col] = 'LH'
                board.rotated[row][col] = True
            #Peca L na coluna esquerda ou na coluna direita
            elif col == 0 or col == board_columns - 1:
                board.cells[row][col] = 'LV'
                board.rotated[row][col] = True

        return
    
    def board_first_approach(self):
    
        board = self
        board_rows = board.rows
        board_columns = board.cols


        firstRow = 0
        lastRow = board_rows - 1
        
        for i in range(board_columns):
            board.verifyBorder(firstRow, i)
            board.verifyBorder(lastRow, i)

        firstCol = 0
        lastCol = board_columns - 1

        for i in range(board_rows):
            board.verifyBorder(i, firstCol)
            board.verifyBorder(i, lastCol)

        return

    def inferencedPossibleRotations(self, row, col):

        board = self

        targetingUs = {
            'C': ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'],
            'B': ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'],
            'E': ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'],
            'D': ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']
        }

        connectsWithPosition = {
            'FC': ['C'],
            'FB': ['B'],
            'FE': ['E'],
            'FD': ['D'],

            'BC': ['E', 'C', 'D'],
            'BB': ['E', 'B', 'D'],
            'BE': ['E', 'C', 'B'],
            'BD': ['C', 'D', 'B'],

            'VC': ['E', 'C'],
            'VB': ['B', 'D'],
            'VE': ['E', 'B'],
            'VD': ['C', 'D'],

            'LH': ['E', 'D'],
            'LV': ['C', 'B']
        }


        hasToConnect = []
        doesntHaveToConnect = []
        res = []

        # Pega nas coordenadas das peças adjacentes
        adjacentCoords = board.getSurroundingCoords(row, col)
        for each in adjacentCoords:

            # Se está na board
            if(board.isOnBoard(each[0], each[1])):

                # Se foi rodada (é como se estivesse no sitio certo, pode não estar)
                if(board.rotated[each[0], each[1]]):
                    # Se a peça está a apontar para nós, temos de apontar para ela, logo adiciona na hasToConnect
                    if (board.get_value(each[0], each[1]) in targetingUs[each[2]]):

                        hasToConnect += each[2]

                    # Caso não esteja a apontar para nós mas esteja rodada, não podemos apontar para ela
                    else:
                        doesntHaveToConnect += each[2]

            # Se não estiver na board, a peça não pode conectar com essa posição
            else:
                doesntHaveToConnect += each[2]

        # Depois de ter a lista de para onde tem de apontar e para onde não tem,
        # ver se alguma rotação da peça se encaixa nessas restrições
        possibleRotations = board.possibleRotations(row, col)

        # Para cada rotação verifica as restrições
        for each2 in possibleRotations:

            # Pega na peça
            piece = board.applyRotaion(each2[0], each2[1], each2[2])
            connectsWith = connectsWithPosition[piece]
            acceptablePiece = True
            for position in hasToConnect:
                if(position not in connectsWith):
                    acceptablePiece = False
            for position in doesntHaveToConnect:
                if(position in connectsWith):
                    acceptablePiece = False
            if(acceptablePiece):
                res.append((each2[0], each2[1], each2[2]))
            
        return res
            
    def testInference(self):

        board = self
        board_columns = board.cols
        board_rows = board.rows

        targetingUs = {
            'C': ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'],
            'B': ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'],
            'E': ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'],
            'D': ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']
        }

        connectsWithPosition = {
            'FC': ['C'],
            'FB': ['B'],
            'FE': ['E'],
            'FD': ['D'],

            'BC': ['E', 'C', 'D'],
            'BB': ['E', 'B', 'D'],
            'BE': ['E', 'C', 'B'],
            'BD': ['C', 'D', 'B'],

            'VC': ['E', 'C'],
            'VB': ['B', 'D'],
            'VE': ['E', 'B'],
            'VD': ['C', 'D'],

            'LH': ['E', 'D'],
            'LV': ['C', 'B']
        }


        hasToConnect = []
        doesntHaveToConnect = []
        pieceCount = 0
        changed = True
        i = 0

        while(changed):
            changed = False
            for row in range(board_rows):
                for col in range(board_columns):

                    # Verificar se está a false, caso esteja, ver se só tem 1 possibilidade de rotação
                    if(not board.rotated[row][col]):

                        # Pega nas coordenadas das peças adjacentes
                        adjacentCoords = board.getSurroundingCoords(row, col)
                        for each in adjacentCoords:

                            # Se está na board
                            if(board.isOnBoard(each[0], each[1])):

                                # Se foi rodada (é como se estivesse no sitio certo, pode não estar)
                                if(board.rotated[each[0], each[1]]):
                                    # Se a peça está a apontar para nós, temos de apontar para ela, logo adiciona na hasToConnect
                                    if (board.get_value(each[0], each[1]) in targetingUs[each[2]]):

                                        hasToConnect += each[2]

                                    # Caso não esteja a apontar para nós mas esteja rodada, não podemos apontar para ela
                                    else:
                                        doesntHaveToConnect += each[2]

                            # Se não estiver na board, a peça não pode conectar com essa posição
                            else:
                                doesntHaveToConnect += each[2]

                        # Depois de ter a lista de para onde tem de apontar e para onde não tem,
                        # ver se alguma rotação da peça se encaixa nessas restrições
                        possibleRotations = board.possibleRotations(row, col)

                        # Para cada rotação verifica as restrições
                        for each2 in possibleRotations:

                            # Pega na peça
                            piece = board.applyRotaion(each2[0], each2[1], each2[2])
                            connectsWith = connectsWithPosition[piece]
                            acceptablePiece = True
                            for position in hasToConnect:
                                if(position not in connectsWith):
                                    acceptablePiece = False
                            for position in doesntHaveToConnect:
                                if(position in connectsWith):
                                    acceptablePiece = False
                            # Modificar este if para verificar se mais de uma peça dá fit-in
                            # se sim não altera, caso seja 0, mata branch
                            # em caso de ser igual a 1, altera
                            if(acceptablePiece):
                                rightPiece = piece
                                pieceCount += 1
                        if(pieceCount == 1):
                            board.cells[row][col] = rightPiece
                            board.rotated[row][col] = True
                            changed = True
                        elif(pieceCount == 0):
                            board.cutBranch = True
                            return
                        pieceCount = 0
                        hasToConnect = []
                        doesntHaveToConnect = []
                                
        return

    def possibleRotations(self, row, column):

        board = self
        piece = board.get_value(row, column)

        board_rows = board.rows
        board_columns = board.cols

        actions_FBV = ('C','B','E','D')
        actions_L = ('H','V')

        actions_F_canto_superior_direito = ('B','E')
        actions_F_canto_superior_esquerdo = ('B','D')
        actions_F_canto_inferior_direito = ('C','E')
        actions_F_canto_inferior_esquerdo = ('C','D')

        actions_F_linha_superior = ('B','E','D')
        actions_F_linha_inferior = ('C','E','D')
        actions_F_coluna_esquerda = ('C','B','D')
        actions_F_coluna_direita = ('C','B','E')

        actions_V_primeira_linha = ('B','E')
        actions_V_ultima_linha = ('C','D')
        actions_V_primeira_coluna = ('B','D')
        actions_V_ultima_coluna = ('C','E')
        
        actions = []

        if ((row != 0 and row != board_rows-1) and (column != 0 and column != board_columns-1)):
            if (piece[0] == 'L'):
                for position in actions_L:
                    actions.append((row,column,position),)
            else:
                for position in actions_FBV:
                    actions.append((row,column,position),)

        #Peca F
        elif piece[0] == 'F':

            #Peca F no canto superior esquerdo
            if row == 0 and column == 0:
                for position in actions_F_canto_superior_esquerdo:
                    actions.append((row,column,position),)
            #Peca F no canto superior direito
            elif row == 0 and column == board_columns - 1:
                for position in actions_F_canto_superior_direito:
                    actions.append((row,column,position),)
            #Peca F no canto inferior esquerdo
            elif row == board_rows - 1 and column == 0:
                for position in actions_F_canto_inferior_esquerdo:
                    actions.append((row,column,position),)
            #Peca F no canto inferior direito
            elif row == board_rows - 1 and column == board_columns - 1:
                for position in actions_F_canto_inferior_direito:
                    actions.append((row,column,position),)

            #Peca F na linha superior (sem ser nos cantos)
            elif row == 0:
                for position in actions_F_linha_superior:
                    actions.append((row,column,position),)
            #Peca F na linha inferior (sem ser nos cantos)
            elif row == board_rows - 1:
                for position in actions_F_linha_inferior:
                    actions.append((row,column,position),)
            #Peca F na coluna esquerda (sem ser nos cantos)
            elif column == 0:
                for position in actions_F_coluna_esquerda:
                    actions.append((row,column,position),)
            #Peca F na coluna direita (sem ser nos cantos)
            elif column == board_columns - 1:
                for position in actions_F_coluna_direita:
                    actions.append((row,column,position),)

        #Peca V
        elif piece[0] == 'V':
            
            #Peca V na linha superior (sem ser nos cantos)
            if row == 0:
                for position in actions_V_primeira_linha:
                    actions.append((row,column,position),)
            #Peca V na linha inferior (sem ser nos cantos)
            elif row == board_rows - 1:
                for position in actions_V_ultima_linha:
                    actions.append((row,column,position),)
            #Peca V na coluna esquerda (sem ser nos cantos)
            elif column == 0:
                for position in actions_V_primeira_coluna:
                    actions.append((row,column,position),)
            #Peca V na coluna direita (sem ser nos cantos)
            elif column == board_columns - 1:
                for position in actions_V_ultima_coluna:
                    actions.append((row,column,position),)
            
        return actions

    def applyRotaion(self, row, column, rotation):
        board = self

        piece = board.get_value(row, column)

        firstLetter = piece[0]
        newPiece = firstLetter + rotation

        return newPiece


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.initial = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        board = state.board
        board_cols = board.cols
        board_rows = board.rows

        board.testInference()
        if (board.cutBranch):
            return []
        
        rotated_pieces = state.board.rotated

        row = 0
        col = 0

        while(rotated_pieces[row][col]):
            col+=1
            if col == board_cols:
                col = 0
                row+=1
            if row == board_rows:
                return [(0, 0, board.cells[0][0][1])]
        
        state.board.rotated[row][col] = True
        return board.inferencedPossibleRotations(row, col)
    
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        newCells = np.copy(state.board.cells)
        newRotated = np.copy(state.board.rotated)

        row = action[0]
        col = action[1]
        rotation = action[2]

        newBoard = Board(newCells)
        newBoard.rotated = newRotated

        newPiece = newBoard.applyRotaion(row, col, rotation)
        newBoard.cells[row][col] = newPiece

        newState = PipeManiaState(newBoard)

        return newState

    # Starts at the initial piece and goes through the paths of the tubes, only 
    # returns true if all pieces have been traversed and all connections are correct.
    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        visited = [[False for _ in range(board.cols)] for _ in range(board.rows)]
        stack = []
        first_piece = [0, 0]
        stack.append(first_piece)

        totalPieces = board.rows * board.cols
        countPieces = 0

        stillCompatible = 1
        while(stack != []):
            piece = stack.pop()
            piece_row = piece[0]
            piece_col = piece[1]
            piece_str = board.get_value(piece_row, piece_col)

            if (not visited[piece_row][piece_col]):
                visited[piece_row][piece_col] = True
                countPieces += 1
                # [row, col, position relative to the main piece]
                adjacentPipesList = board.getAdjacentPipes(piece_row, piece_col)

                # if all pipes are compatible at a certain moment
                if (stillCompatible):
                    for coord_sec_piece in adjacentPipesList:
                        str_sec_piece = board.get_value(coord_sec_piece[0], coord_sec_piece[1])
                        position = coord_sec_piece[2]
                        # adds the pipes do the stack do continue visiting pipes
                        if (board.compatiblePipes(piece_str, str_sec_piece, position)):
                            stack += [[coord_sec_piece[0], coord_sec_piece[1]], ]

                        # incompatible pipes
                        else:
                            stillCompatible = 0
                # found incompatible pipes, end
                else:
                    break

        # verifies if every pipe was visited, if not it means that there were found
        # incompatible pipes or there are two or more different pipe structures.
        return totalPieces == countPieces

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass

if __name__ == "__main__":
    board = Board.parse_instance()
    problem = PipeMania(board)

    goal_node = breadth_first_tree_search(problem)

    if goal_node:
        print(goal_node.state.board.__str__())
    else:
        print("No solution found.")