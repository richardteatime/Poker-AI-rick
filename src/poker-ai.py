import streamlit as st
from aiplayer import AIPlayer
from evaluator import Evaluator
from abstraction import calculate_equity
from table import Table

# Inizializza il giocatore AI e il tavolo
ai_player = AIPlayer(balance=1000)
evaluator = Evaluator()

def validate_and_format_card(card):
    """Valida e formatta una carta nel formato corretto."""
    valid_values = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}
    valid_suits = {"h", "d", "s", "c"}
    if len(card) < 2 or len(card) > 3:
        raise ValueError(f"Formato della carta non valido: {card}")
    value = card[:-1]
    suit = card[-1]
    if value not in valid_values or suit not in valid_suits:
        raise ValueError(f"Carta non valida: {card}")
    # Ritorna la carta nel formato corretto (es. "10s" -> "Ts")
    return ("T" if value == "10" else value) + suit

def ai_suggestion(player_hand, community_cards):
    """Genera suggerimenti dell'AI sulla base delle carte fornite."""
    # Validazione e formattazione delle carte
    player_hand = [validate_and_format_card(card) for card in player_hand]
    community_cards = [validate_and_format_card(card) for card in community_cards]

    equity = calculate_equity(player_hand, community_cards)
    if equity > 0.7:
        return "Suggerimento AI: Punta o Rilancia (Bet/Raise). Equity alta!"
    elif 0.4 < equity <= 0.7:
        return "Suggerimento AI: Check o Call. Equity moderata."
    else:
        return "Suggerimento AI: Fold. Equity bassa."

# Configurazione di Streamlit
st.title("Poker AI Chat")
st.write("Inserisci le tue carte e le carte sul tavolo per ricevere suggerimenti dall'AI.")

# Input dell'utente per le carte
player_hand = st.text_input("Le tue carte (es. 'As Kd'): ")
community_cards = st.text_input("Carte sul tavolo (es. '2h 7d 9c'): ")

if st.button("Ottieni suggerimento dall'AI"):
    try:
        # Dividi le carte in liste
        player_hand_list = player_hand.split()
        community_cards_list = community_cards.split()

        # Controlla se i formati delle carte sono validi
        if len(player_hand_list) != 2:
            st.error("Devi inserire esattamente due carte per la tua mano.")
        elif len(community_cards_list) not in [0, 3, 4, 5]:
            st.error("Le carte sul tavolo devono essere 0, 3, 4 o 5.")
        else:
            # Genera suggerimento dall'AI
            suggestion = ai_suggestion(player_hand_list, community_cards_list)
            st.success(suggestion)

    except Exception as e:
        st.error(f"Si è verificato un errore: {str(e)}")
