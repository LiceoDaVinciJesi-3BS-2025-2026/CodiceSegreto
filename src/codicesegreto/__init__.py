def main() -> None:
    print("Hello from codicesegreto!")

import pygame

pygame.init()

screen = pygame.display.set_mode( (1200, 900) )
pygame.display.set_caption("CodiceSegreto")

Titlefont = pygame.font.SysFont('Arial', 100)
Normalfont = pygame.font.SysFont('Arial', 50)

# calcolo le posizioni per centrare ciò che devo scrivere di seguito
larghezza_schermo = 1200
altezza_schermo = 900

#variabile per sapere in che schermata ci troviamo
dove_siamo = "menu"
running = True

while running:
    #gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # se preme n (maiuscola o minuscola)
            if event.key == pygame.K_n:
                dove_siamo = "numeri"
                print("=== HAI PREMUTO N ===")
                print("Ora sei nella finestra NUMERI")
                print("Premi ESC per tornare al menu")
                print("====================")

            # se preme l (minuscola o maiuscola)
            elif event.key == pygame.K_l:
                dove_siamo = "lettere"
                print("=== HAI PREMUTO L ===")
                print("Ora sei nella finestra LETTERE")
                print("Premi ESC per tornare al menu")
                print("====================")
                
            # Se preme c (minuscola o maiuscola)
            elif event.key == pygame.K_c:
                dove_siamo = "colori"
                print("=== HAI PREMUTO C ===")
                print("Ora sei nella finestra COLORI")
                print("Premi ESC per tornare al menu")
                print("====================")
            
            # Se preme ESC
            elif event.key == pygame.K_ESCAPE:
                dove_siamo = "menu"
                print("Torno al MENU principale")

    # disegna in base alla schermata in cui siamo

    # se siamo nel menu
    if dove_siamo == "menu":
        # Colora lo schermo di rosa
        screen.fill("pink")
        
        # Devo CREARE il titolo e le opzioni DENTRO il while
        # così vengono ridisegnati ogni volta che torno al menu

        # titolo al centro
        Titolo = Titlefont.render("CodiceSegreto", True, "Black")
        # larghezza del testo
        larghezza_titolo = Titolo.get_width()
        #centro orizzontalmente
        posizione_x_titolo = (larghezza_schermo - larghezza_titolo) // 2
        # distanza dal bordo superiore
        posizione_y_titolo = 150
        screen.blit(Titolo, (posizione_x_titolo, posizione_y_titolo))
        
        # scrivo le varie opzioni sotto al titolo
        opzione1 = Normalfont.render("Lettere (L)", True, "Black")
        opzione2 = Normalfont.render("Numeri (N)", True, "Black")
        opzione3 = Normalfont.render("Colori (C)", True, "Black")
        
        # calcola le posizioni
        posizione_x_opzione1 = (larghezza_schermo - opzione1.get_width()) // 2
        posizione_x_opzione2 = (larghezza_schermo - opzione2.get_width()) // 2
        posizione_x_opzione3 = (larghezza_schermo - opzione3.get_width()) // 2
        
        posizione_y_opzione1 = posizione_y_titolo + 150
        posizione_y_opzione2 = posizione_y_opzione1 + 80
        posizione_y_opzione3 = posizione_y_opzione2 + 80
        
        # Disegna le opzioni
        screen.blit(opzione1, (posizione_x_opzione1, posizione_y_opzione1))
        screen.blit(opzione2, (posizione_x_opzione2, posizione_y_opzione2))
        screen.blit(opzione3, (posizione_x_opzione3, posizione_y_opzione3))

    # se siamo nella finestra numeri
    elif dove_siamo == "numeri":
        # Sfondo viola chiaro
        screen.fill((216, 191, 216))  # Thiestle
        
        # Titolo della finestra numeri colore viola scuro
        titolo_numeri = Titlefont.render("MODALITÀ NUMERI", True, "Indigo")
        x_titolo = (larghezza_schermo - titolo_numeri.get_width()) // 2
        screen.blit(titolo_numeri, (x_titolo, 50))
        
        # Cosa ci deve essere scritto e il colore
        testo1 = Normalfont.render("Qui giocherai con i numeri!", True, "Black")
        testo2 = Normalfont.render("Il computer penserà a 4 numeri (da 1 a 6)", True, "Black")
        testo3 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, "Black")
        testo4 = Normalfont.render("Premi ESC per tornare al menu", True, "Red")
        testo5 = Normalfont.render("premi I per iniziare", True, "Black")
        
        # Scrive tutto centrato
        screen.blit(testo1, ((larghezza_schermo - testo1.get_width()) // 2, 200))
        screen.blit(testo2, ((larghezza_schermo - testo2.get_width()) // 2, 270))
        screen.blit(testo3, ((larghezza_schermo - testo3.get_width()) // 2, 340))
        screen.blit(testo4, ((larghezza_schermo - testo4.get_width()) // 2, 450))
        screen.blit(testo5, ((larghezza_schermo - testo5.get_width()) // 2, 570))

     #se preme I
        if event.key == pygame.K_I:
            screen.fill((216, 191, 216)) # Thiestle
       #creazione del codice 
            import random
            codice = ""
            for cifre in range (4):
                cifra = random.randint(1, 6)
                codice += cifra
        #tentativi per indovinare il codice
            for tentativi in range (10):
                #verifica che il numero di cifre sia corretto
                while True:
                    prova = str(input(f"tentativo {tentativi}, inserire il codice:"))
                    if len(prova) == 4:
                        break
                        
                    elif len(prova) > 4:
                        print("hai inserito troppe cifre, ricorda, devono essere solo 4")
                    else:
                        print("hai inserito troppe poche cifre, ricorda, devono essere 4")

                testo7 = Normalfont.render(f"{prova}", True, "Black")
                        
                if prova == codice:
                    testo6 = Normalfont.render(f"Hai vinto in {tentativi} tentativi!", True, "Black")
                    screen.blit(testo6, ((larghezza_schermo - testo6.get_width()) // 2, 200))
                    screen.blit(testo4, ((larghezza_schermo - testo4.get_width()) // 2, 450))
                    break
                    
                else:
                    for elemento in codice:
                        if elemento in prova:
                            print(f"{elemento} presente del codice")
                    for pos in range (0, 4):
                        if codice[pos] == prova[pos]:
                            print(f"{codice[pos]} è nella posizione giusta")
                    continue
                            
                                                        
    # se siamo nella finestra lettere
    elif dove_siamo == "lettere":
        # Sfondo giallo chiaro
        screen.fill((255, 253, 208))  # Moccasin
        
        titolo_lettere = Titlefont.render("MODALITÀ LETTERE", True, "DarkOrange")
        x_titolo = (larghezza_schermo - titolo_lettere.get_width()) // 2
        screen.blit(titolo_lettere, (x_titolo, 50))
        
        # Cosa deve esserci scritto e il colore
        testo_1 = Normalfont.render("Qui giocherai con le lettere!", True, "Black")
        testo_2 = Normalfont.render("Il computer penserà a 4 lettere (dalla a alla z)", True, "Black")
        testo_3 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, "Black")
        testo_4 = Normalfont.render("Premi ESC per tornare al menu", True, "Red")
        testo_5 = Normalfont.render("premi I per iniziare", True, "Black")
        
        # Scrive centrato
        screen.blit(testo_1, ((larghezza_schermo - testo_1.get_width()) // 2, 200))
        screen.blit(testo_2, ((larghezza_schermo - testo_2.get_width()) // 2, 270))
        screen.blit(testo_3, ((larghezza_schermo - testo_3.get_width()) // 2, 340))
        screen.blit(testo_4, ((larghezza_schermo - testo_4.get_width()) // 2, 450))
        screen.blit(testo_5, ((larghezza_schermo - testo_5.get_width()) // 2, 570))
    
    # se siamo nella finestra colori
    elif dove_siamo == "colori":
        # Sfondo azzurro chiaro
        screen.fill((173, 216, 230))  # LightBlue
        
        titolo_colori = Titlefont.render("MODALITÀ COLORI", True, "DarkBlue")
        x_titolo = (larghezza_schermo - titolo_colori.get_width()) // 2
        screen.blit(titolo_colori, (x_titolo, 50))
        
        # Cosa deve esserci scritto e il colore
        testo__1 = Normalfont.render("Qui giocherai con i colori!", True, "Black")
        testo__2 = Normalfont.render("Il computer penserà a 4 colori", True, "Black")
        testo__3 = Normalfont.render("I colori possibili sono blu, rosso, arancione, giallo, viola", True, "Black")
        testo__4 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, "Black")
        testo__5 = Normalfont.render("Premi ESC per tornare al menu", True, "Red")
        testo__6 = Normalfont.render("premi I per iniziare", True, "Black")
        
        # Scirve tutto centrato
        screen.blit(testo__1, ((larghezza_schermo - testo__1.get_width()) // 2, 170))
        screen.blit(testo__2, ((larghezza_schermo - testo__2.get_width()) // 2, 240))
        screen.blit(testo__3, ((larghezza_schermo - testo__3.get_width()) // 2, 300))
        screen.blit(testo__4, ((larghezza_schermo - testo__4.get_width()) // 2, 370))
        screen.blit(testo__5, ((larghezza_schermo - testo__5.get_width()) // 2, 450))
        screen.blit(testo__6, ((larghezza_schermo - testo__6.get_width()) // 2, 570))
    
    # Aggiorna il contenuto dello schermo
    pygame.display.flip()
        
# Chiude pygame
pygame.quit()
            
            
                
                
                
