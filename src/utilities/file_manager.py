import os
import json
import pygame


class FileManager:
    @staticmethod
    def load_json_file(filename):
        """
        Loads a JSON file from the data directory.
        :param filename: The name of the file to load.
        :return: Parsed JSON data if successful, otherwise None.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file directory (file_manager.py)
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Go up two levels to reach the project root
        file_path = os.path.join(root_dir, "data", filename)  # Construct the full path to the file

        # Load the JSON file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"Successfully loaded JSON data from {file_path}")
                return data
        except FileNotFoundError:
            print(f"Error: The JSON file '{filename}' was not found at {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error: Could not parse the JSON file '{filename}'. JSON error: {e}")

        # Return None if loading fails
        return None

    @staticmethod
    def load_image(filename):
        """
        Loads an image file using Pygame, with error handling.
        :param filename: The name of the image file to load.
        :return: The loaded image surface if successful, otherwise a default placeholder.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file directory (file_manager.py)
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Go up two levels to reach the project root
        file_path = os.path.join(root_dir, "img", filename)  # Construct the full path to the file
        try:
            image = pygame.image.load(file_path).convert_alpha()
            print(f"Successfully loaded image from {file_path}")
            return image
        except pygame.error as e:
            print(f"Error: Could not load the image file '{file_path}'. Pygame error: {e}")
            # Return a default placeholder surface
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 0))  # Red fill for a missing resource
            return placeholder
