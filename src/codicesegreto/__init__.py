def main() -> None:
    print("Hello from codicesegreto!")

import pygame

pygame.init()

screen = pygame.display.set_mode( (800, 600) )
pygame.display.set_caption("CodiceSegreto")

Titlefont = pygame.font.SysFont('Confortmaa', 70)
Normalfont = pygame.font.SysFont('Confortmaa', 30)

# oggetto_testo = oggetto_font.render("stringa", True, "colore", "sfondo" (opzionale) )
modalità = Normalfont.render("Lettere(L) Numeri (N) Colori (C)", True, "black")
Titolo = Titlefont.render("CodiceSegreto", True, "Black")

running = True

while running:
        # serve a gestire la X di chiusura in alto
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # colora lo schermo di verde
    screen.fill("pink")
    screen.blit(Titolo, (100, 50))
    screen.blit(modalità, (100,110))

        # aggiorna il contenuto dello schermo
    pygame.display.flip()

    # Chiude pygame
pygame.quit()
    
   
    
    
        
        
        
