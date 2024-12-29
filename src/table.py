# Lookup table mapping an int -> position of "1" bit
# Ex: 4 (100) -> 2

def generate_table():
    TABLE = {}
    #Create the table
    val = 1
    for i in range(64):
        TABLE[val] = i
        val *= 2

    return TABLE


class Table:
    def __init__(self):
        self.players = []
        self.community_cards = []
        self.pot = 0

    def add_player(self, player):
        """Aggiunge un giocatore al tavolo."""
        self.players.append(player)

    def start_hand(self):
        """Inizia una nuova mano di poker."""
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.hand = []  # Reset della mano
            player.active = True

    def apply_action(self, player, action, amount=0):
        """Applica un'azione al tavolo."""
        if action == "fold":
            player.active = False
        elif action == "call":
            self.pot += amount
        elif action == "raise":
            self.pot += amount
        else:
            raise ValueError("Azione non valida")
