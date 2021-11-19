from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import GameType, Game

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new Gamer, collect the auth Token, and create a sample GameType
        """

        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, gamer, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED THE DATABASE WITH A GAMETYPE
        # This is necessary because the API does not
        # expose a /gametypes URL path for creating GameTypes

        # Create a new instance of GameType
        game_type = GameType()
        game_type.label = "Board game"

        # Save the GameType to the testing database
        game_type.save()

    def test_create_game(self):
        """
        Ensure we can create (POST) a new Game.
        """

        # Define the URL path for creating a new Game
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skillLevel": 5,
            "numberOfPlayers": 6,
            "gameTypeId": 1,
            "description": "More fun than a Barrel Of Monkeys!"
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, game, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['id'], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["maker"], game['maker'])
        self.assertEqual(response.data["skill_level"], game['skillLevel'])
        self.assertEqual(response.data["number_of_players"], game['numberOfPlayers'])
        self.assertEqual(response.data["game_type"]['id'], game['gameTypeId'])

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.description = "Not Sorry!"

        # Save the Game to the testing database
        game.save()

        # Define the URL path for updating an existing Game
        url = f'/games/{game.id}'

        # Define NEW Game properties
        new_game = {
            "title": "Sorry",
            "maker": "Hasbro",
            "skillLevel": 2,
            "numberOfPlayers": 4,
            "gameTypeId": 1,
            "description": "Is it too late now to say sorry?"
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['id'], self.token.user_id)
        self.assertEqual(response.data["title"], new_game['title'])
        self.assertEqual(response.data["maker"], new_game['maker'])
        self.assertEqual(
            response.data["skill_level"], new_game['skillLevel'])
        self.assertEqual(
            response.data["number_of_players"], new_game['numberOfPlayers'])
        self.assertEqual(response.data["game_type"]['id'], new_game['gameTypeId'])

    def test_get_game(self):
        """
        Ensure we can GET an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.gamer_id = 1
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.skill_level = 5
        game.number_of_players = 4
        game.game_type_id = 1

        # Save the Game to the testing database
        game.save()

        # Define the URL path for getting a single Game
        url = f'/games/{game.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['id'], game.gamer_id)
        self.assertEqual(response.data["title"], game.title)
        self.assertEqual(response.data["maker"], game.maker)
        self.assertEqual(response.data["skill_level"], game.skill_level)
        self.assertEqual(response.data["number_of_players"], game.number_of_players)
        self.assertEqual(response.data["game_type"]['id'], game.game_type_id)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.gamer_id = 1
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.skill_level = 5
        game.number_of_players = 4
        game.game_type_id = 1
        game.description = "It's too late to apologize."

        # Save the Game to the testing database
        game.save()

        # Define the URL path for deleting an existing Game
        url = f'/games/{game.id}'

        # Initiate DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
