
import pygame

# We need to init pygame before creating the fonts
# NOTE: From pygame docs:
# It is safe to call this init() more than once: repeated calls will have no effect
pygame.init()

font16 = pygame.font.SysFont('Arial', 16)
font24 = pygame.font.SysFont('Arial', 24)
font32 = pygame.font.SysFont('Arial', 32)
font48 = pygame.font.SysFont('Arial', 48)
font72 = pygame.font.SysFont('Arial', 72)
font96 = pygame.font.SysFont('Arial', 96)
