import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

playlist = ["/Users/askarovva/Desktop/Lab7 programming/song1.mp3", 
            "/Users/askarovva/Desktop/Lab7 programming/song2.mp3", 
            "/Users/askarovva/Desktop/Lab7 programming/song3.mp3"]  
current_index = 0

def play_song(index):
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()

def next_song():
    global current_index
    current_index = (current_index + 1) % len(playlist)
    play_song(current_index)

def previous_song():
    global current_index
    current_index = (current_index - 1) % len(playlist)
    play_song(current_index)

play_song(current_index)

running = True
while running:
    screen.fill(WHITE)

    song_text = font.render(f"Now Playing: {os.path.basename(playlist[current_index])}", True, BLACK)
    screen.blit(song_text, (50, 100))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  
                play_song(current_index)
            elif event.key == pygame.K_s:  
                stop_song()
            elif event.key == pygame.K_n:  
                next_song()
            elif event.key == pygame.K_b:  
                previous_song()

pygame.quit()
