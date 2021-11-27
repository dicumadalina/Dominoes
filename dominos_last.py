import random


class Domino:

    def __init__(self):
        self.full_domino_set = []
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = None
        self.player_input = None

    def generate_full_domino_set(self):
        self.full_domino_set = [[x, y] for x in range(7) for y in range(x + 1)]

    def shuffle_domino_set(self):
        random.shuffle(self.full_domino_set)

    def allocate_domino_pieces(self):
        self.player_pieces = self.full_domino_set[:7]
        self.computer_pieces = self.full_domino_set[7:14]
        self.stock_pieces = self.full_domino_set[14:]

    def determine_starting_player(self):
        player_pieces_max = max(self.player_pieces)
        computer_pieces_max = max(self.computer_pieces)

        if computer_pieces_max > player_pieces_max:
            self.status = 'player'

            max_index = self.computer_pieces.index(computer_pieces_max)
            self.domino_snake.append(self.computer_pieces[max_index])
            self.computer_pieces.remove(self.computer_pieces[max_index])
        else:
            self.status = 'computer'

            max_index = self.player_pieces.index(player_pieces_max)
            self.domino_snake.append(self.player_pieces[max_index])
            self.player_pieces.remove(self.player_pieces[max_index])

    def check_player_input(self):
        while True:
            if self.player_input.lstrip('-').isdigit():
                if abs(int(self.player_input)) > len(self.player_pieces):
                    print("Invalid input. Please try again.")
                    self.player_input = input()
                else:
                    break
            else:
                print("Invalid input. Please try again.")
                self.player_input = input()

    def player_move(self):
        while True:
            self.player_input = input()
            self.check_player_input()
            player_input = int(self.player_input)
            player_piece = self.player_pieces[abs(player_input) - 1]

            if player_input > 0:
                if player_piece[0] in self.domino_snake[-1]:
                    self.domino_snake.append(self.player_pieces[player_input - 1])
                    self.player_pieces.remove(self.player_pieces[player_input - 1])
                elif player_piece[1] in self.domino_snake[-1]:
                    self.domino_snake.append(self.player_pieces[abs(player_input) - 1][::-1])
                    self.player_pieces.remove(self.player_pieces[abs(player_input) - 1])
                else:
                    print('Illegal move. Please try again.')
                    continue
                break
            elif player_input < 0:
                self.domino_snake.insert(0, self.player_pieces[abs(player_input) - 1])
                self.player_pieces.remove(self.player_pieces[abs(player_input) - 1])
                break
            else:
                if len(self.stock_pieces) != 0:
                    new_player_piece = self.stock_pieces.pop()
                    self.player_pieces.append(new_player_piece)
                    break
                else:
                    print("Invalid input. Please try again.")

    def computer_move(self):
        while True:
            computer_input = random.randint(-len(self.computer_pieces), len(self.computer_pieces))

            if computer_input > 0:
                self.domino_snake.append(self.computer_pieces[computer_input - 1])
                self.computer_pieces.remove(self.computer_pieces[computer_input - 1])
                break
            elif computer_input < 0:
                self.domino_snake.insert(0, self.computer_pieces[abs(computer_input) - 1])
                self.computer_pieces.remove(self.computer_pieces[abs(computer_input) - 1])
                break
            else:
                if len(self.stock_pieces) != 0:
                    new_computer_piece = self.stock_pieces.pop()
                    self.computer_pieces.append(new_computer_piece)
                    break
                else:
                    continue

    def check_for_win_condition(self):
        if len(self.player_pieces) == 0:
            self.status = 'player_wins'
            return True
        elif len(self.computer_pieces) == 0:
            self.status = 'computer_wins'
            return True
        elif self.domino_snake[0][0] == self.domino_snake[len(self.domino_snake) - 1][1]:
            if self.domino_snake.count(self.domino_snake[0][0]) >= 8:
                self.status = 'game_over_draw'
                return True
            else:
                return False
        else:
            return False

    def display_game_status(self):
        if self.status == 'player':
            print("\nStatus: It's your turn to make a move. Enter your command.")
        elif self.status == 'computer':
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        elif self.status == 'player_wins':
            print("\nStatus: The game is over. You won!")
        elif self.status == 'computer_wins':
            print("\nStatus: The game is over. The computer won!")
        elif self.status == 'game_over_draw':
            print("\nStatus: The game is over. It's a draw!")

    def change_player(self):
        if self.status == 'player':
            self.status = 'computer'
        else:
            self.status = 'player'

    def print_domino_snake(self):
        if len(self.domino_snake) > 6:
            first_domino_snake_half = self.domino_snake[0:3]
            second_domino_snake_half = self.domino_snake[(len(self.domino_snake) - 3):]

            first_half_string_list = []
            for _ in first_domino_snake_half:
                first_half_string_list.append(str(_))
            first_half = ''.join(first_half_string_list)

            second_half_string_list = []
            for _ in second_domino_snake_half:
                second_half_string_list.append(str(_))
            second_half = ''.join(second_half_string_list)

            print(first_half + '...' + second_half)
            print()

        else:
            domino_snake_string_list = []
            for _ in self.domino_snake:
                domino_snake_string_list.append(str(_))

            print(''.join(domino_snake_string_list))
            print()

    def game_interface(self):
        print("=" * 70)
        print(f"Stock size:", len(self.stock_pieces))
        print(f"Computer pieces:", len(self.computer_pieces))
        print()

        self.print_domino_snake()

        print("Your pieces:")
        for i, domino in enumerate(self.player_pieces, 1):
            print(i, domino, sep=':')

    def main(self):
        self.generate_full_domino_set()
        self.shuffle_domino_set()
        self.allocate_domino_pieces()
        self.determine_starting_player()

        while not self.check_for_win_condition():
            self.game_interface()
            self.display_game_status()
            if self.status == 'player':
                self.player_move()
                self.change_player()
            else:
                self.player_input = input()
                self.computer_move()
                self.change_player()

        self.game_interface()
        self.display_game_status()


Domino().main()