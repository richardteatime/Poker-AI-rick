import streamlit as st
from aiplayer import AIPlayer
from evaluator import Evaluator
from abstraction import calculate_equity
from table import Table

# Configurazione iniziale nella barra laterale
st.sidebar.title("Configurazione del gioco")
default_balance = st.sidebar.number_input("💰 Inserisci il saldo iniziale per il giocatore AI:", min_value=100, max_value=10000, value=1000, step=100)
default_bet_cost = st.sidebar.number_input("🎲 Costo per chiamare o rilanciare (Bet/Raise):", min_value=1, max_value=500, value=50, step=1)

# Configurazione dei giocatori
num_players = st.sidebar.number_input("👥 Numero di giocatori al tavolo:", min_value=2, max_value=10, value=4, step=1)
st.sidebar.write("**Stato dei giocatori:**")
players_status = {
    f"Giocatore {i+1}": st.sidebar.checkbox(f"Giocatore {i+1} attivo", value=True)
    for i in range(num_players)
}



#def update_balance(player, amount):
  #  """Aggiorna il saldo del giocatore."""
 #   if hasattr(player, 'balance') and player.balance >= amount:
  #      player.balance -= amount
  #      return f"✅ {amount} chips puntate. Saldo rimanente: {player.balance}"
  #  elif hasattr(player, 'balance'):
  #      return "⚠️ Saldo insufficiente per puntare."
 #   else:
  #      return "❌ Errore: Attributo 'balance' non trovato nel giocatore."
# Firma personalizzata nella barra laterale
st.sidebar.markdown("---")
st.sidebar.markdown("**Created by Rick** 🚀")


# Inizializza il giocatore AI e il tavolo
try:
    class CustomAIPlayer(AIPlayer):
        def __init__(self, balance):
            super().__init__(balance)
            self.balance = balance  # Forza l'attributo balance

    ai_player = CustomAIPlayer(balance=default_balance)
except Exception as e:
    st.error(f"Errore durante l'inizializzazione dell'AI Player: {str(e)}")

evaluator = Evaluator()

# Cache per risultati dell'equity
@st.cache_data
def calculate_equity_cached(player_hand, community_cards):
    """Calcola l'equity con caching per input ripetuti."""
    return calculate_equity(player_hand, community_cards)

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
    return ("T" if value == "10" else value) + suit

def ai_suggestion(player_hand, community_cards, balance):
    """Genera suggerimenti dell'AI sulla base delle carte fornite."""
    # Validazione e formattazione delle carte
    player_hand = [validate_and_format_card(card) for card in player_hand]
    community_cards = [validate_and_format_card(card) for card in community_cards]

    equity = calculate_equity_cached(player_hand, community_cards)
    if equity > 0.7:
        bet_suggestion = "alto" if balance > 500 else "medio"
        return f"🎯 Suggerimento AI: Punta o Rilancia (Bet/Raise). Equity alta! Consiglio di puntata: {bet_suggestion}."
    elif 0.4 < equity <= 0.7:
        return "🤔 Suggerimento AI: Check o Call. Equity moderata."
    else:
        return "🛑 Suggerimento AI: Fold. Equity bassa."

# Configurazione di Streamlit
st.title("♠️ Poker AI Chat ♣️")
st.markdown("**Inserisci le tue carte e quelle sul tavolo per ricevere suggerimenti dall'AI.**")

# Legenda dei simboli
with st.expander("📜 Legenda dei simboli"):
    st.write(
        """
        - **h**: ❤️ (Cuori, Hearts)
        - **d**: ♦️ (Quadri, Diamonds)
        - **s**: ♠️ (Picche, Spades)
        - **c**: ♣️ (Fiori, Clubs)
        """
    )

# Mostra saldo corrente nella barra laterale
#if hasattr(ai_player, 'balance'):
   # st.sidebar.write(f"💵 Saldo AI corrente: {ai_player.balance}")
#else:
   # st.sidebar.write("❌ Errore: Il saldo non è disponibile.")

# Input dell'utente per le carte
player_hand = st.text_input("🃏 Le tue carte (es. 'As Kd'): ")
community_cards = st.text_input("🂡 Carte sul tavolo (es. '2h 7d 9c'): ")

if st.button("💡 Ottieni suggerimento dall'AI"):
    try:
        # Dividi le carte in liste
        player_hand_list = player_hand.split()
        community_cards_list = community_cards.split()

        # Controlla se i formati delle carte sono validi
        if len(player_hand_list) != 2:
            st.error("⚠️ Devi inserire esattamente due carte per la tua mano.")
        elif len(community_cards_list) not in [0, 3, 4, 5]:
            st.error("⚠️ Le carte sul tavolo devono essere 0, 3, 4 o 5.")
        else:
            # Genera suggerimento dall'AI
            suggestion = ai_suggestion(player_hand_list, community_cards_list, ai_player.balance)
            st.success(suggestion)

            # Aggiorna saldo dopo un'azione (es. Bet/Raise)
            #action_result = update_balance(ai_player, default_bet_cost)
            #st.sidebar.write(action_result)

    except Exception as e:
        st.error(f"❌ Si è verificato un errore: {str(e)}")
