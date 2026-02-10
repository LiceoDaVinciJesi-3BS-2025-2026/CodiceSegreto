while True:
    variabile = str(input("Scrivi la lettera corrispondente per aprire la modalità desiderata"))
    if variabile == L or variabile == l or variabile == N or variabile == n or variabile == C or variabile == c:
        break
    else:
        print("Riprova!\n la modalità inserita non esiste")

if variabile == n or variabile == N:
    stringa_numero = ""
    import random
    for r in range(1,6):
        numero = random.randint(0,9)
        stringa_numero += numero
print("Indovina la combinazione di 5 cifre in 6 tentativi")

# importa ed inizializza la libreria pygame
import pygame

pygame.init()

# lo screen (con titolo)
screen = pygame.display.set_mode( (800, 600) )
pygame.display.set_caption("CodiceSegreto")

Titlefont = pygame.font.SysFont('Confortmaa', 70)
Normalfont = pygame.font.SysFont('Confortmaa', 30)

#oggetto_testo = oggetto_font.render("stringa",True,"colore","sfondo
# facile...
running = True

while running:
    # serve a gestire la X di chiusura in alto
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # colora lo schermo di rosa
    screen.fill("pink")
    screen.bilt()

    # aggiorna il contenuto dello schermo
    pygame.display.flip()

# Chiude pygame
pygame.quit()


print("lettere (L)")
print("numeri (N)")
print("colori (C)")

