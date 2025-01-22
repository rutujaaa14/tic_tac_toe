# game/views.py
from django.shortcuts import get_object_or_404
from .models import Game, GameHistory 
from .serializers import GameSerializer 
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Game  # Add this import
from rest_framework.permissions import IsAuthenticated
from .serializers import GameHistorySerializer


User = get_user_model()


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def index(request):
    return render(request, 'index.html')

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            token_serializer = TokenSerializer(token_data)
            return Response(token_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartGameView(APIView):
    def post(self, request):
        player1_id = request.data.get('player1')
        player2_id = request.data.get('player2')

        if not player1_id or not player2_id:
            return Response({"error": "Both player1 and player2 are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            player1 = User.objects.get(id=player1_id)
            player2 = User.objects.get(id=player2_id)
        except User.DoesNotExist:
            return Response({"error": "One or both players do not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if player1 == player2:
            return Response({"error": "Players must be different."}, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.create(
            player1=player1,
            player2=player2,
            current_turn=player1,  # Player 1 starts the game
            game_board="         "  # Empty 3x3 board
        )

        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

from rest_framework.permissions import IsAuthenticated
from django.db import transaction

class MakeMoveView(APIView):
    permission_classes = [IsAuthenticated]  

    @transaction.atomic  
    def post(self, request):
        game_id = request.data.get('game_id')
        position = request.data.get('position')

        if game_id is None or position is None:
            return Response({'error': 'Both game_id and position are required.'}, status=status.HTTP_400_BAD_REQUEST)

        game = get_object_or_404(Game, id=game_id)

        print(f"Authenticated User: {request.user.username}")
        print(f"Game ID: {game.id}, Player1: {game.player1.username}, Player2: {game.player2.username}")
        print(f"Current Turn before move: {game.current_turn.username}")

        if request.user not in [game.player1, game.player2]:
            return Response({'error': 'You are not part of this game'}, status=status.HTTP_400_BAD_REQUEST)

        if game.winner or game.draw:
            return Response({'error': 'Cannot update a completed game'}, status=status.HTTP_400_BAD_REQUEST)

        if game.current_turn != request.user:
            return Response({'error': 'It is not your turn'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            position = int(position)
            if position < 0 or position > 8:
                return Response({'error': 'Invalid position. Position must be between 0 and 8.'}, status=status.HTTP_400_BAD_REQUEST)
            
            game.make_move(position, request.user)  

            print(f"Turn switched. New turn: {game.current_turn.username}")

            if game.winner:
                return Response({'message': f'{game.winner.username} wins!'}, status=status.HTTP_200_OK)
            elif game.draw:
                return Response({'message': 'The game is a draw!'}, status=status.HTTP_200_OK)

            
            return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GameHistoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        games_as_player1 = Game.objects.filter(player1=request.user)
        games_as_player2 = Game.objects.filter(player2=request.user)
        games = games_as_player1 | games_as_player2
        
        if not games:
            return Response({"error": "No games found."}, status=status.HTTP_404_NOT_FOUND)

        game_histories = []

        for game in games:
            opponent = game.player2 if game.player1 == request.user else game.player1
            result = 'Draw' if game.draw else f'{game.winner.username} wins!' if game.winner else 'In Progress'
            
            moves = GameHistory.objects.filter(game=game).order_by('move_number')

            game_data = {
                'game_id': game.id,
                'opponent': opponent.username,
                'result': result,
                'moves': GameHistorySerializer(moves, many=True).data,
            }
            game_histories.append(game_data)
        
        return Response(game_histories, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request):
        if request.user.is_anonymous:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user

        username = request.data.get('username', user.username)
        email = request.data.get('email', user.email)

        password = request.data.get('password', None)
        if password:
            user.set_password(password)

        user.username = username
        user.email = email
        user.save()

        return Response({'message': 'Profile updated successfully!'}, status=status.HTTP_200_OK)