from board import *

high_score = 0

print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
print("Welcome to the Game 2048")
print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
print("To play use the 'w', 'a', 's', and 'd' keys!")
print("Objective: Reach the 2048 tile! Good Luck!")

play_again = True

while play_again:
    grid = Grid()

    score = 0

    print("Score: " + str(score) + "    High Score: " + str(high_score))
    grid.print_grid()
    continue_game = True
    while continue_game:
        move = str(input())
        move = move.lower()
        if move == 'w':
            score += grid.up_press()
        elif move == 'a':
            score += grid.left_press()
        elif move == 's':
            score += grid.down_press()
        elif move == 'd':
            score += grid.right_press()
        else:
            print("Please press 'w', 'a', 's', or 'd'.")

        print()
        print()
        print()

        if score > high_score:
            high_score = score

        print("Score: " + str(score) + "    High Score: " + str(high_score))
        grid.print_grid()

        if grid.game_over():
            continue_game = False

    print()
    print("****GAME OVER****")
    print()
    print("Would you like to play again? (y/n)   ")
    invalid_answer = True
    while invalid_answer:
        ans = input()
        ans = ans.lower()
        if ans == 'y':
            invalid_answer = False
        elif ans == 'n':
            invalid_answer = False
            play_again = False
        else:
            print("Please respond with 'y' or 'n'.")