from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    pass

User = get_user_model()

class Game(models.Model):
    player1 = models.ForeignKey(User, related_name='player1_games', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2_games', on_delete=models.CASCADE)
    current_turn = models.ForeignKey(User, related_name='turn_games', on_delete=models.SET_NULL, null=True)
    game_board = models.CharField(max_length=9)  # String to represent 3x3 board
    winner = models.ForeignKey(User, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True)
    draw = models.BooleanField(default=False)

    def __str__(self):
        return f'Game between {self.player1} and {self.player2}'

    def is_winner(self, player):
        """Check if the player has won the game"""
        win_patterns = [
            [0, 1, 2],  # top row
            [3, 4, 5],  # middle row
            [6, 7, 8],  # bottom row
            [0, 3, 6],  # left column
            [1, 4, 7],  # middle column
            [2, 5, 8],  # right column
            [0, 4, 8],  # diagonal
            [2, 4, 6],  # diagonal
        ]
        board = self.game_board
        return any(all(board[i] == player for i in pattern) for pattern in win_patterns)

    def is_draw(self):
        """Check if the game is a draw (board is full and no winner)"""
        return ' ' not in self.game_board and self.winner is None

    def make_move(self, position, player):
        """Make a move for the player at the given position (0-8)"""

        if self.winner or self.draw:
            raise ValueError('Game has already ended. Cannot make a move.')

        if self.game_board[position] != ' ':
            raise ValueError('Invalid move: The position is already taken.')
        
        board_list = list(self.game_board)
        board_list[position] = 'X' if player == self.player1 else 'O'
        self.game_board = ''.join(board_list)

        
        move_number = self.game_board.count('X') + self.game_board.count('O')  # Move number based on count of X and O
        GameHistory.objects.create(
            game=self,
            move_number=move_number,
            player=player,
            move=str(position)  
        )

        # Check for winner or draw
        if self.is_winner(player):
            self.winner = player
        elif self.is_draw():
            self.draw = True
        else:
            self.current_turn = self.player2 if self.current_turn == self.player1 else self.player1
        
        self.save()

class GameHistory(models.Model):
    game = models.ForeignKey(Game, related_name='history', on_delete=models.CASCADE)
    move_number = models.IntegerField()  # The move number (e.g., 1, 2, 3...)
    player = models.ForeignKey(User, related_name='game_moves', on_delete=models.CASCADE)  # The player who made the move
    move = models.CharField(max_length=2)  # The position on the board (e.g., '0', '1', '2'...)

    def __str__(self):
        return f"Move {self.move_number} by {self.player.username} in Game {self.game.id}"


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Game, GameHistory


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']  # Display these fields in the admin panel
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

admin.site.register(User, CustomUserAdmin)  

class GameAdmin(admin.ModelAdmin):
    list_display = ['player1', 'player2', 'current_turn', 'game_board', 'winner', 'draw']
    search_fields = ['player1__username', 'player2__username']
    list_filter = ['winner', 'draw']

admin.site.register(Game, GameAdmin)

class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ['game', 'move_number', 'player', 'move']
    search_fields = ['game__id', 'player__username']
    list_filter = ['game']

admin.site.register(GameHistory, GameHistoryAdmin)
