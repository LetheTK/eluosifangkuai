import pygame
import sys
from tetris.game import TetrisGame

def main():
    pygame.init()
    game = TetrisGame()
    game.run()

if __name__ == "__main__":
    main()