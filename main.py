import pygame
from utils import speak, analyze_emotion
from rendering import setup_scene, render_scene

def draw_menu(screen):
    font = pygame.font.Font(None, 36)
    text1 = font.render('1. Diga Olá', True, (255, 255, 255))
    text2 = font.render('2. Pergunte sobre o tempo', True, (255, 255, 255))
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    scene, renderer = setup_scene()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speak("Olá! Como você está?")
                elif event.key == pygame.K_2:
                    speak("O tempo está ótimo hoje!")

        color = render_scene(scene, renderer)
        image = pygame.image.frombuffer(color.tobytes(), color.shape[1::-1], "RGB")

        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        draw_menu(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
