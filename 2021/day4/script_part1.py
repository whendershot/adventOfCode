"""
Find which board wins in bingo first
"""
from io import StringIO
import pandas as pd


class BingoBoard:
    
    def __init__(self, board: pd.DataFrame):
        self.board = board
        self.board_mask = board.isin([" "])
        self.last_number_called: int = None

    def check_is_winner(self) -> bool:
        row_win = self.board_mask.all(axis=0).any()
        col_win = self.board_mask.all(axis=1).any()
        #diagonals do not count in this version, can uncomment to add them back in of course
        # back_cross_win = self.board_mask[0][0] & self.board_mask[1][1] & self.board_mask[2][2] & self.board_mask[3][3] & self.board_mask[4][4]
        # forward_cross_win = self.board_mask[0][4] & self.board_mask[1][3] & self.board_mask[2][2] & self.board_mask[3][1] & self.board_mask[4][0]
        return row_win | col_win #| back_cross_win | forward_cross_win

    def update(self) -> None:
        pass

    def check_number(self, value: int) -> None:
        temp_mask = self.board.isin([value])
        self.board_mask = self.board_mask | temp_mask
        self.last_number_called = value

    def calculate_score(self) -> int:
        # print(test_sim.boards[2].board[test_sim.boards[2].board_mask.isin([False])].sum().sum())
        score = int(self.board[self.board_mask.isin([False])].sum().sum()) * self.last_number_called
        return score


class Simulation:

    def __init__(self, input_path: str):
        self.number_draw = self.generate_number_draw(input_path)
        self.boards = self.generate_boards(input_path)

    def generate_boards(self, input_path: str) -> list[BingoBoard]:
        #example from https://stackoverflow.com/questions/62626392/read-in-txt-file-into-multiple-dataframes-split-by-empty-gaps-between-the-data
        f = open(input_path, "r")
        board_lines = f.readlines()[2:]
        f.close()

        boards = [""]

        for line in board_lines:
            if line.strip():
                boards[-1] += line
            else:
                # single blank line deliminates a board in file
                boards.append("")
                continue 
        # print(boards)
        boards = [BingoBoard(pd.read_table(StringIO(board), header=None, dtype=int, sep="\s+")) for board in boards]
        return boards


    def generate_number_draw(self, input_path: str) -> list[str]:
        f = open(input_path, "r")
        number_draw = f.readline().strip().split(",")
        f.close()
        return number_draw

    def run_simulation(self) -> BingoBoard:
        winning_boards =[]
        for draw in self.number_draw:
            print(f"Checking: {draw}")
            for board in self.boards:
                board.check_number(int(draw))
                if board.check_is_winner():
                    winning_boards.append(board)
            if len(winning_boards) > 0:
                #have at least one winning board
                break

        #for each winning board, calculate its score
        for board in winning_boards:
            print(board.board)
            print(board.board_mask)
            print(f"Score: {board.calculate_score()}")
        #return the board with the highest score and its score
        
test_sim = Simulation("input.txt")
print(test_sim.number_draw)
print("---Running Simulation---")
test_sim.run_simulation()

