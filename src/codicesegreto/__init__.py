def main() -> None:
    print("Hello from codicesegreto!")

import pygame

pygame.init()

screen = pygame.display.set_mode( (1000, 800) )
pygame.display.set_caption("CodiceSegreto")

Titlefont = pygame.font.SysFont('Confortaa', 100)
Normalfont = pygame.font.SysFont('Confortaa', 50)

# calcolo le posizioni per centrare ciò che devo scrivere di seguito
larghezza_schermo = 1000
altezza_schermo = 800

# titolo al centro
Titolo = Titlefont.render("CodiceSegreto", True, "Black")
# larghezza del testo
larghezza_titolo = Titolo.get_width()
#centro orizzontalmente
posizione_x_titolo = (larghezza_schermo - larghezza_titolo) // 2
# distanza dal bordo superiore
posizione_y_titolo = 150

# scrivo le varie opzioni sotto al titolo
opzione1 = Normalfont.render("Lettere (L)", True, "Black")
opzione2 = Normalfont.render("Numeri (N)", True, "Black")
opzione3 = Normalfont.render("Colori (C)", True, "Black")

# calcola quando spazio occupa la scritta di ogni opzione
larghezza_opzione1 = opzione1.get_width()
larghezza_opzione2 = opzione2.get_width()
larghezza_opzione3 = opzione3.get_width()

# centro le opzioni
posizione_x_opzione1 = (larghezza_schermo - larghezza_opzione1) // 2
posizione_x_opzione2 = (larghezza_schermo - larghezza_opzione2) // 2
posizione_x_opzione3 = (larghezza_schermo - larghezza_opzione3) // 2

# Posizioni verticali (una sotto l'altra con spazio)
posizione_y_opzione1 = posizione_y_titolo + 150
posizione_y_opzione2 = posizione_y_opzione1 + 80
posizione_y_opzione3 = posizione_y_opzione2 + 80

running = True

while running:
    # serve a gestire la X di chiusura in alto
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # colora lo schermo di rosa
    screen.fill("pink")
    # Disegna il titolo (centrato)
    screen.blit(Titolo, (posizione_x_titolo, posizione_y_titolo))
    
    # Disegna le 3 opzioni (centrate, una sotto l'altra)
    screen.blit(opzione1, (posizione_x_opzione1, posizione_y_opzione1))
    screen.blit(opzione2, (posizione_x_opzione2, posizione_y_opzione2))
    screen.blit(opzione3, (posizione_x_opzione3, posizione_y_opzione3))

    # Aggiorna il contenuto dello schermo
    pygame.display.flip()

# Chiude pygame
pygame.quit()
    
    
        
        
        
