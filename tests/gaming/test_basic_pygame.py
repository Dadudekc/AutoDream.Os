#!/usr/bin/env python3
"""
Basic Pygame Test
Agent-6 Gaming Environment Setup
"""

import pygame
import sys


def test_basic_pygame():
    """Test basic pygame functionality"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Basic Pygame Test")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 100, 200))
        pygame.draw.circle(screen, (255, 255, 0), (400, 300), 50)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    test_basic_pygame()
