"""
Main code that runs all parts of the game.

Two modes:
1. Training: trains the AI to play the game
2. Playing: play the game against the AI

Training Pipeline:
1. Generate abstractions for the holdem game
2. Use Monte-Carlo CFR to generate a blueprint strategy for the abstracted game

Playing Pipeline:
1. Use the blueprint strategy + real-time search (depth-limited solving) to play the game
2. Integrate with pygame
"""

import random
from aiplayer import AIPlayer
from player import Player
from table import TABLE

def main():
    print("\nBenvenuto al gioco di Poker con AI!")
    
    # Configurazione del tavolo
    table = TABLE()

    # Creazione dei giocatori
    human_player = Player(balance=1000)  # Giocatore umano
    ai_player = AIPlayer(balance=1000)   # AI Player

    # Aggiunta dei giocatori al tavolo
    table.add_player(human_player)
    table.add_player(ai_player)

    # Inizio partita
    while True:
        print("\nNuova mano!\n")
        table.start_hand()

        # Mostra le carte iniziali del giocatore umano
        print(f"Le tue carte: {human_player.hand}")

        # Fase di puntata (simulazione semplice)
        while not table.hand_over:
            print("\nTocca a te!")
            print("1. Fold 2. Check/Call 3. Bet/Raise")
            action = input("Scegli la tua azione: ")

            if action == "1":
                print("Hai scelto di fare Fold.")
                table.fold(human_player)
                break
            elif action == "2":
                print("Hai scelto Check/Call.")
                table.call(human_player)
            elif action == "3":
                bet = int(input("Inserisci l'importo del tuo Bet/Raise: "))
                table.bet(human_player, bet)
            else:
                print("Azione non valida.")
                continue

            # Azione dell'AI
            print("\nTocca all'AI...")
            ai_action = ai_player.getAction()
            print(f"L'AI ha scelto: {ai_action}")
            table.apply_action(ai_player, ai_action)

        if input("Vuoi giocare un'altra mano? (s/n): ") != "s":
            break

    print("Grazie per aver giocato! Alla prossima!")

if __name__ == "__main__":
    main()

	