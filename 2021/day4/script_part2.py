"""
Play a game of bingo from a file. For all boards, calculate their scores and finishing positions
"""
from io import StringIO
import pandas as pd


class BingoBoard:
    
    def __init__(self, board: pd.DataFrame):
        self.board = board
        self.board_mask = board.isin([" "])
        self.last_number_called: int = None
        self.has_won = False

    def check_is_winner(self) -> bool:
        row_win = self.board_mask.all(axis=0).any()
        col_win = self.board_mask.all(axis=1).any()
        #diagonals do not count in this version, can uncomment to add them back in of course
        # back_cross_win = self.board_mask[0][0] & self.board_mask[1][1] & self.board_mask[2][2] & self.board_mask[3][3] & self.board_mask[4][4]
        # forward_cross_win = self.board_mask[0][4] & self.board_mask[1][3] & self.board_mask[2][2] & self.board_mask[3][1] & self.board_mask[4][0]
        return row_win | col_win #| back_cross_win | forward_cross_win


    def check_number(self, value: int) -> None:
        if not self.has_won:
            temp_mask = self.board.isin([value])
            self.board_mask = self.board_mask | temp_mask
            self.last_number_called = value
            self.has_won = self.check_is_winner()

    def calculate_score(self) -> int:
        score = int(self.board[self.board_mask.isin([False])].sum().sum()) * self.last_number_called
        return score


class Simulation:

    def __init__(self, input_path: str):
        self.number_draw = self.generate_number_draw(input_path)
        self.playing_boards = self.generate_boards(input_path)

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
        boards = [BingoBoard(pd.read_table(StringIO(board), header=None, dtype=int, sep="\s+")) for board in boards]
        return boards


    def generate_number_draw(self, input_path: str) -> list[str]:
        f = open(input_path, "r")
        number_draw = f.readline().strip().split(",")
        f.close()
        return number_draw

    def run_simulation(self) -> pd.DataFrame:
        winning_boards = []
        for draw in self.number_draw:
            print(f"Checking: {draw}")
            for board in list(self.playing_boards):
                board.check_number(int(draw))
                if board.has_won:
                    winning_boards.append(board)
                    self.playing_boards.remove(board)

        #for each winning board; calculate its score, then generate the DataFrame
        d = {"finish_position": [], "score": [], "board" : []}
        for i, board in enumerate(winning_boards):
            d["finish_position"].append(i + 1)
            d["score"].append(board.calculate_score())
            d["board"].append(board)
        
        df = pd.DataFrame(d)
        return df

test_sim = Simulation("input.txt")
print(test_sim.number_draw)
print("---Running Simulation---")
df = test_sim.run_simulation()

print(df.describe())
print("---Highest Score---")
highest_score = df[df["score"] == df["score"].max()]
print(highest_score)
print(highest_score["board"].values[0].board)
print(highest_score["board"].values[0].board_mask)
print("---First Winner---")
first_winner = df.head(1)
print(first_winner)
print(first_winner["board"].values[0].board)
print(first_winner["board"].values[0].board_mask)
print("---Lowest Score---")
lowest_score = df[df["score"] == df["score"].min()]
print(lowest_score)
print(lowest_score["board"].values[0].board)
print(lowest_score["board"].values[0].board_mask)
print("---Last Winner---")
last_winner = df.tail(1)
print(last_winner)
print(last_winner["board"].values[0].board)
print(last_winner["board"].values[0].board_mask)