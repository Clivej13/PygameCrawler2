# character_menu_quests.py

import pygame

class CharacterMenuQuests:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, x, y):
        # Example quests for display
        quests = ["Find the lost sword", "Talk to the village elder", "Collect 5 herbs"]
        for i, quest in enumerate(quests):
            quest_text = self.font.render(f"{i+1}. {quest}", True, (255, 255, 255))
            screen.blit(quest_text, (x, y + i * 30))
