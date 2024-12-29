import sys

sys.path.append("../src")

from environment import *
from helper import *
import pygame
import argparse
import time
import joblib

pygame.font.init()  # For fonts
pygame.mixer.init()  # For sounds

SCALE = 1
WIDTH, HEIGHT = 1280, 720  # you can resize this dynamically afterwards

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Poker By Steven Gong")

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 60

INVERSE_RANK_KEY = {
    14: "A",
    2: "02",
    3: "03",
    4: "04",
    5: "05",
    6: "06",
    7: "07",
    8: "08",
    9: "09",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
}

# INITIALIZE GLOBAL VARIABLES
FLOP_1_CARD_POSITION = None
FLOP_2_CARD_POSITION = None
FLOP_3_CARD_POSITION = None
TURN_CARD_POSITION = None
RIVER_CARD_POSITION = None
PLAYER_CARD_1 = None
PLAYER_CARD_2 = None
OPPONENT_CARD_1 = None
OPPONENT_CARD_2 = None
DEALER_BUTTON = None
DEALER_BUTTON_POSITION_1 = None
DEALER_BUTTON_POSITION_2 = None
CARD_BACK = None
POT_FONT = None
BET_BUTTON_FONT = None
BET_FONT = None
PLAYERS_FONT = None
START_NEW_ROUND_BUTTON = None
fold_rect = None
check_rect = None
custom_rect = None
start_new_round_rect = None
buttons = None
input_box = None
POKER_BACKGROUND = None

scale_factor = 1
color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color = color_inactive
active = False
input_bet_text = ""
warning_text = ""
done = False

cursor_counter = 0


def resize(width, height):
    global scale_factor, WIN
    scale_factor = width / WIDTH
    WIN = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    update_asset_positions()


def scale_tuple(tup, factor):
    return tuple([x * factor for x in tup])


def update_asset_positions():
    global FLOP_1_CARD_POSITION, FLOP_2_CARD_POSITION, FLOP_3_CARD_POSITION, TURN_CARD_POSITION, RIVER_CARD_POSITION, PLAYER_CARD_1, PLAYER_CARD_2, OPPONENT_CARD_1, OPPONENT_CARD_2
    global DEALER_BUTTON, DEALER_BUTTON_POSITION_1, DEALER_BUTTON_POSITION_2, CARD_BACK, POT_FONT, BET_BUTTON_FONT, BET_FONT, PLAYERS_FONT, fold_rect, check_rect, custom_rect, start_new_round_rect, buttons, input_box, POKER_BACKGROUND

    FLOP_1_CARD_POSITION = scale_tuple((400, HEIGHT / 2 - 65), scale_factor)
    FLOP_2_CARD_POSITION = scale_tuple((490, HEIGHT / 2 - 65), scale_factor)
    FLOP_3_CARD_POSITION = scale_tuple((580, HEIGHT / 2 - 65), scale_factor)
    TURN_CARD_POSITION = scale_tuple((670, HEIGHT / 2 - 65), scale_factor)
    RIVER_CARD_POSITION = scale_tuple((760, HEIGHT / 2 - 65), scale_factor)
    PLAYER_CARD_1 = scale_tuple((WIDTH / 2 - 70, HEIGHT - 220), scale_factor)
    PLAYER_CARD_2 = scale_tuple((WIDTH / 2, HEIGHT - 220), scale_factor)
    OPPONENT_CARD_1 = scale_tuple((WIDTH / 2 - 70, 35), scale_factor)
    OPPONENT_CARD_2 = scale_tuple((WIDTH / 2, 35), scale_factor)
    DEALER_BUTTON = pygame.transform.scale(
        pygame.image.load("assets/dealer_button.png"), scale_tuple((30, 30), scale_factor)
    )
    DEALER_BUTTON_POSITION_1 = scale_tuple((500, HEIGHT - 200), scale_factor)
    DEALER_BUTTON_POSITION_2 = scale_tuple((515, 120), scale_factor)

    CARD_BACK = pygame.transform.scale(
        pygame.image.load("../assets/back.png"), scale_tuple((263 / 3, 376 / 3), scale_factor)
    )
    POT_FONT = pygame.font.SysFont("Roboto", int(scale_factor * 30), bold=True)
    BET_BUTTON_FONT = pygame.font.SysFont("Roboto", int(scale_factor * 24), bold=True)
    BET_FONT = pygame.font.SysFont("Roboto", int(scale_factor * 26), bold=True)
    PLAYERS_FONT = pygame.font.SysFont("Roboto", int(scale_factor * 30), bold=True)

    fold_rect = pygame.Rect(*scale_tuple((800, HEIGHT - 80, 80, 45), scale_factor))
    check_rect = pygame.Rect(
        *scale_tuple((887, HEIGHT - 80, 100, 45), scale_factor)
    )  # Can also be call button
    custom_rect = pygame.Rect(*scale_tuple((995, HEIGHT - 80, 80, 45), scale_factor))
    start_new_round_rect = pygame.Rect(
        *scale_tuple((WIDTH - 300, HEIGHT - 80, 250, 45), scale_factor)
    )
    buttons = [fold_rect, check_rect, custom_rect, start_new_round_rect]

    input_box = pygame.Rect(*scale_tuple((1060, HEIGHT - 80, 140, 45), scale_factor))

    POKER_BACKGROUND = pygame.transform.scale(
        pygame.image.load("assets/poker-table.png"), scale_tuple((WIDTH, HEIGHT), scale_factor)
    )


update_asset_positions()


def load_card_image(card: Card):
    # 263 × 376
    return pygame.transform.scale(
        pygame.image.load("../assets/" + str(card) + ".png"),
        scale_tuple((263 / 3, 376 / 3), scale_factor),
    )


def display_total_pot_balance(env: PokerEnvironment):
    pot_information = POT_FONT.render(
        "Total Pot: $" + str(env.total_pot_balance + env.stage_pot_balance), 1, WHITE
    )
    WIN.blit(pot_information, scale_tuple((875, HEIGHT / 2 - 15), scale_factor))


def display_user_balance(env: PokerEnvironment):
    player_balance = PLAYERS_FONT.render(
        "$" + str((env.players[0].player_balance - env.players[0].current_bet)), 1, GREEN
    )
    WIN.blit(player_balance, scale_tuple((WIDTH / 2 + 130, HEIGHT - 200), scale_factor))


def display_opponent_balance(env: PokerEnvironment):
    opponent_balance = PLAYERS_FONT.render(
        "$" + str((env.players[1].player_balance - env.players[1].current_bet)), 1, GREEN
    )
    WIN.blit(opponent_balance, scale_tuple((WIDTH / 2 + 130, 100), scale_factor))


def display_user_bet(env: PokerEnvironment):
    pot_information = BET_FONT.render("Bet: $" + str(env.players[0].current_bet), 1, WHITE)
    WIN.blit(pot_information, scale_tuple((WIDTH / 2 - 30, HEIGHT - 280), scale_factor))


def display_opponent_bet(env: PokerEnvironment):
    pot_information = BET_FONT.render("Bet: $" + str(env.players[1].current_bet), 1, WHITE)
    WIN.blit(pot_information, (WIDTH / 2 - 30, 190))


def display_sessions_winnings(env: PokerEnvironment):
    if env.players[0].is_AI: # don't show if AI
        return

    winnings = 0
    if len(env.players_balance_history) != 0:
        winnings = sum(env.players_balance_history[0])
    if winnings < 0:
        text = POT_FONT.render("Session Winnings: -$" + str(-winnings), 1, WHITE)
    else:
        text = POT_FONT.render("Session Winnings: $" + str(winnings), 1, WHITE)

    WIN.blit(text, scale_tuple((WIDTH - 400, 40), scale_factor))


def display_turn(env: PokerEnvironment):
    if env.position_in_play == 0:  # AI
        text = POT_FONT.render("YOUR TURN", 1, WHITE)
    else:
        text = POT_FONT.render("OPPONENT TURN", 1, RED)
    WIN.blit(text, scale_tuple((70, 40), scale_factor))


def display_user_cards(env: PokerEnvironment):
    WIN.blit(CARD_BACK, PLAYER_CARD_1)
    WIN.blit(CARD_BACK, PLAYER_CARD_2)

def reveal_user_cards(env: PokerEnvironment):
    WIN.blit(load_card_image(env.players[0].hand[0]), PLAYER_CARD_1)
    WIN.blit(load_card_image(env.players[0].hand[1]), PLAYER_CARD_2)

def display_opponent_cards(env: PokerEnvironment):
    WIN.blit(CARD_BACK, OPPONENT_CARD_1)
    WIN.blit(CARD_BACK, OPPONENT_CARD_2)


def reveal_opponent_cards(env: PokerEnvironment):
    WIN.blit(load_card_image(env.players[1].hand[0]), OPPONENT_CARD_1)
    WIN.blit(load_card_image(env.players[1].hand[1]), OPPONENT_CARD_2)


def display_community_cards(env: PokerEnvironment):
    # Draw the CARDS
    for idx, card in enumerate(env.community_cards):
        if idx == 0:
            WIN.blit(load_card_image(card), FLOP_1_CARD_POSITION)
        elif idx == 1:
            WIN.blit(load_card_image(card), FLOP_2_CARD_POSITION)
        elif idx == 2:
            WIN.blit(load_card_image(card), FLOP_3_CARD_POSITION)
        elif idx == 3:
            WIN.blit(load_card_image(card), TURN_CARD_POSITION)
        else:
            WIN.blit(load_card_image(card), RIVER_CARD_POSITION)


def display_dealer_button(env: PokerEnvironment):
    if env.dealer_button_position == 0:  # User is the dealer
        WIN.blit(DEALER_BUTTON, DEALER_BUTTON_POSITION_1)
    else:  # Opponent is the dealer
        WIN.blit(DEALER_BUTTON, DEALER_BUTTON_POSITION_2)


def draw_window(env: PokerEnvironment, god_mode=False, user_input=False):
    WIN.blit(POKER_BACKGROUND, (0, 0))

    if env.showdown and env.end_of_round():  # Reveal opponent's cards at showdown
        god_mode = True

    # Display the cards
    if god_mode:
        reveal_user_cards(env)
        reveal_opponent_cards(env)
    else:
        display_user_cards(env)
        display_opponent_cards(env)

    # Display Community Cards
    display_community_cards(env)

    # Display Pot Information
    display_total_pot_balance(env)
    display_dealer_button(env)

    # TODO: Display Current bet information
    display_user_bet(env)
    display_opponent_bet(env)

    # Display Player Balance Information
    display_user_balance(env)
    display_opponent_balance(env)

    # Display Session Winnings
    display_sessions_winnings(env)

    # Display turn
    display_turn(env)

    if env.end_of_round():
        winning_players = env.get_winning_players_idx()
        if len(winning_players) == 2:  # Split the pot
            text = BET_FONT.render("This is a tie", 1, WHITE)
        elif winning_players[0] == 0:
            text = BET_FONT.render("You won!", 1, WHITE)
        else:
            text = BET_FONT.render("You lost.", 1, WHITE)

        WIN.blit(text, scale_tuple((250, 350), scale_factor))

        start_new_round = BET_BUTTON_FONT.render("Start New Round", 1, WHITE)

        AAfilledRoundedRect(WIN, RED, start_new_round_rect, radius=0.4)
        WIN.blit(
            start_new_round,
            (start_new_round_rect.x + 28 * scale_factor, start_new_round_rect.y + 7 * scale_factor),
        )

    # Pressable Buttons for Check / Fold / Raise. Only display buttons if it is your turn
    warning_text_rendered = BET_FONT.render(warning_text, 1, RED)
    WIN.blit(warning_text_rendered, scale_tuple((WIDTH - 250, HEIGHT - 120), scale_factor))

    if user_input:
        # AAfilledRoundedRect(WIN, RED, pygame.Rect(392,400, 120,50), radius=0.4)
        if not env.end_of_round() and not env.players[env.position_in_play].is_AI:
            AAfilledRoundedRect(WIN, RED, check_rect, radius=0.4)
            AAfilledRoundedRect(WIN, RED, custom_rect, radius=0.4)
            AAfilledRoundedRect(WIN, WHITE, input_box, radius=0.4)
            AAfilledRoundedRect(WIN, RED, fold_rect, radius=0.4)

            if "f" in env.valid_actions():
                fold_bet = BET_BUTTON_FONT.render("Fold", 1, WHITE)
                WIN.blit(
                    fold_bet, (fold_rect.x + 15 * scale_factor, fold_rect.y + 9 * scale_factor)
                )

            if "k" in env.valid_actions():
                check_bet = BET_BUTTON_FONT.render("Check", 1, WHITE)
                WIN.blit(
                    check_bet, (check_rect.x + 15 * scale_factor, check_rect.y + 9 * scale_factor)
                )
            else:
                call_bet = BET_BUTTON_FONT.render("Call", 1, WHITE)
                WIN.blit(
                    call_bet, (check_rect.x + 28 * scale_factor, check_rect.y + 9 * scale_factor)
                )

            # TODO: Handle edges cases where these buttons are impossible, in which case you need to grey it out
            custom_bet = BET_BUTTON_FONT.render("Bet", 1, WHITE)
            WIN.blit(
                custom_bet, (custom_rect.x + 15 * scale_factor, custom_rect.y + 9 * scale_factor)
            )
            custom_input_bet_text = BET_BUTTON_FONT.render(input_bet_text, 1, BLACK)
            WIN.blit(
                custom_input_bet_text,
                (input_box.x + 7 * scale_factor, input_box.y + 9 * scale_factor),
            )

            if cursor_counter < 15 and active:
                pygame.draw.rect(
                    WIN,
                    (0, 0, 0),
                    scale_tuple(
                        (WIDTH - 210 + 13 * len(input_bet_text), HEIGHT - 70, 1, 20), scale_factor
                    ),
                    1,
                )

    pygame.display.update()


def main():
    score = [0, 0]  # [PLAYER_SCORE, AI_SCORE]
    # Load the nodeMap
    parser = argparse.ArgumentParser(description="Play Hold'Em Poker against the best AI possible.")
    parser.add_argument(
        "-p",
        "--play",
        action="store_true",
        dest="user_input",
        default=True,
        help="Manually play against the AI through a PyGame interface.",
    )
    parser.add_argument(
        "-r",
        "--replay",
        action="store_true",
        dest="replay",
        default=False,
        help="replay a history of games",
    )
    parser.add_argument(
        "-g",
        "--god",
        action="store_true",
        dest="god_mode",
        default=False,
        help="God mode (see the opponent's cards)",
    )

    args = parser.parse_args()
    user_input = args.user_input
    replay = args.replay
    god_mode = args.god_mode

    if replay:  # TODO: Load a history of games, and visualize those
        history = joblib.load("HoldemTrainingHistory.joblib")
        game = 0
        game_i = 0

    INPUT_CARDS = False # Set to true if you want to input your own cards
    env: PokerEnvironment = PokerEnvironment(input_cards=INPUT_CARDS)

    env.add_player() # You
    env.add_AI_player() # Oponent
    env.start_new_round()

    clock = pygame.time.Clock()
    run = True

    def place_custom_bet():
        global input_bet_text, warning_text
        if input_bet_text != "" and input_bet_text.isdigit():
            bet = "b" + str(int(input_bet_text))
            if int(input_bet_text) == env.get_highest_current_bet():
                warning_text = "Cannot bet the same amount"
                return

            env.handle_game_stage(bet)
            if int(input_bet_text) != env.get_highest_current_bet():
                warning_text = "Invalid bet size"

    while run:
        global input_bet_text, active, cursor_counter, warning_text
        cursor_counter = (cursor_counter + 1) % 30

        clock.tick(FPS)

        if env.players[env.position_in_play].is_AI:
            env.handle_game_stage()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:  # For resizing of the window
                resize(event.w, event.h)

            # Check if the buttons are clicked, only process if it is our turn
            if user_input:
                # and env.position_in_play == 0, we can make decisions as the opponent too
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(buttons)):
                        if buttons[i].collidepoint(pygame.mouse.get_pos()):
                            warning_text = ""
                            if i == 0:
                                env.handle_game_stage("f")  # Fold
                            elif i == 1:
                                if "k" in env.valid_actions():
                                    env.handle_game_stage("k")  # Check
                                else:
                                    env.handle_game_stage("c")  # Call
                            elif i == 2:
                                place_custom_bet()
                            elif i == 3 and env.end_of_round():
                                env.start_new_round()
                            else:
                                continue

                            input_bet_text = ""
                            break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            place_custom_bet()

                        elif event.key == pygame.K_BACKSPACE:
                            input_bet_text = input_bet_text[:-1]
                        else:
                            input_bet_text += event.unicode

        if replay:
            if game_i == 0:  # New game, update player's hands
                # TODO: Show the appropriate community cards. Right now it shows the right player cards, but the board is still the old way.
                # TODO: This is a little buggy right now too. It doesn't show the right cards.
                env.players[0].hand = [
                    Card(rank_suit=history[game]["player_cards"][0]),
                    Card(rank_suit=history[game]["player_cards"][1]),
                ]
                env.players[1].hand = [
                    Card(rank_suit=history[game]["opponent_cards"][0]),
                    Card(rank_suit=history[game]["opponent_cards"][1]),
                ]

            env.handle_game_stage(history[game]["history"][game_i])
            game_i += 1
            if game_i >= len(history[game]["history"]):  # Move onto the next game
                print(
                    "Finished game with history: {}. Player: {} Opponent: {} Board: {}".format(
                        history[game]["history"],
                        history[game]["player_cards"],
                        history[game]["opponent_cards"],
                        history[game]["community_cards"],
                    )
                )
                game += 1
                game_i = 0
                if game == len(history):
                    print("Finished replay of all games")
                    return

        # At Showdown, reveal opponent's cards and add a delay
        if replay or user_input:
            draw_window(env, god_mode, user_input)

    pygame.quit()


if __name__ == "__main__":
    main()
