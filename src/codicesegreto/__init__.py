def main() -> None:
    print("Hello from codicesegreto!")

import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("CodiceSegreto")

Titlefont = pygame.font.SysFont('Arial', 100)
Normalfont = pygame.font.SysFont('Arial', 50)
Fontpiccolo = pygame.font.SysFont('Arial', 30)

larghezza_schermo = 1200
altezza_schermo = 900

dove_siamo = "menu"
running = True

# VARIABILI PER IL GIOCO NUMERI
in_gioco_numeri = False
codice_segreto = ""
tentativo_corrente = ""
tentativi_fatti = 0
feedback_dettagliato = ["", "", "", ""]
storico_tentativi = []
gioco_finito = False
risultato = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            # SE PREME N (solo se non in gioco)
            if event.key == pygame.K_n and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "numeri"
                print("=== MODALITÀ NUMERI ===")
            
            # SE PREME L
            elif event.key == pygame.K_l and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "lettere"
                print("=== MODALITÀ LETTERE ===")
            
            # SE PREME C
            elif event.key == pygame.K_c and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "colori"
                print("=== MODALITÀ COLORI ===")
            
            # SE PREME I PER INIZIARE IL GIOCO NUMERI
            elif event.key == pygame.K_i and dove_siamo == "numeri" and not in_gioco_numeri:
                in_gioco_numeri = True
                gioco_finito = False
                tentativi_fatti = 0
                tentativo_corrente = ""
                feedback_dettagliato = ["", "", "", ""]
                storico_tentativi = []
                risultato = ""
                
                # GENERA CODICE SEGRETO
                codice_segreto = ""
                for cifre in range(4):
                    cifra = random.randint(1, 6)
                    codice_segreto += str(cifra)
                
                print(f"CODICE SEGRETO: {codice_segreto}")
                print("Usa i tasti 1-6 per inserire, INVIO per confermare")
            
            # SE PREME ESC
            elif event.key == pygame.K_ESCAPE:
                if in_gioco_numeri or gioco_finito:
                    in_gioco_numeri = False
                    gioco_finito = False
                else:
                    dove_siamo = "menu"
                print("Torno indietro")
            
            # SE SIAMO IN GIOCO NUMERI (e non è finito)
            if in_gioco_numeri and not gioco_finito:
                # TASTI NUMERICI 1-6
                if pygame.K_1 <= event.key <= pygame.K_6:
                    if len(tentativo_corrente) < 4:
                        numero = chr(event.key)
                        tentativo_corrente += numero
                
                # BACKSPACE PER CANCELLARE
                elif event.key == pygame.K_BACKSPACE:
                    tentativo_corrente = tentativo_corrente[:-1]
                
                # INVIO PER CONFERMARE
                elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                    tentativi_fatti += 1
                    
                    # SALVA IL TENTATIVO NELLO STORICO
                    storico_tentativi.append(tentativo_corrente)
                    
                    # CALCOLA FEEDBACK DETTAGLIATO
                    feedback_dettagliato = ["", "", "", ""]
                    
                    for pos in range(4):
                        if tentativo_corrente[pos] == codice_segreto[pos]:
                            feedback_dettagliato[pos] = f"✓ Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                        else:
                            feedback_dettagliato[pos] = f"✗ Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"
                    
                    # Aggiungi info numeri presenti ma in posto sbagliato
                    numeri_presenti = []
                    for pos in range(4):
                        if (tentativo_corrente[pos] != codice_segreto[pos] and 
                            tentativo_corrente[pos] in codice_segreto):
                            if tentativo_corrente[pos] not in numeri_presenti:
                                numeri_presenti.append(tentativo_corrente[pos])
                    
                    if numeri_presenti:
                        presenti_text = f"Numeri presenti ma in posto sbagliato: {', '.join(numeri_presenti)}"
                        storico_tentativi[-1] += f" - {presenti_text}"
                    
                    print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                    
                    # CONTROLLA SE HA VINTO O PERSO
                    if tentativo_corrente == codice_segreto:
                        risultato = "VITTORIA"
                        gioco_finito = True
                        in_gioco_numeri = False
                        print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                        print(f"Codice corretto: {codice_segreto}")
                    elif tentativi_fatti >= 10:
                        risultato = "SCONFITTA"
                        gioco_finito = True
                        in_gioco_numeri = False
                        print(f"HAI PERSO! Codice era: {codice_segreto}")
                    else:
                        tentativo_corrente = ""

    # DISEGNA SCHERMATE
    if dove_siamo == "menu":
        # SFONDO ROSA CHIARO
        screen.fill((255, 182, 193))  # Rosa standard
        
        Titolo = Titlefont.render("CodiceSegreto", True, (0, 0, 0))  # Nero su rosa
        x_titolo = (larghezza_schermo - Titolo.get_width()) // 2
        screen.blit(Titolo, (x_titolo, 150))
        
        opzioni = ["Lettere (L)", "Numeri (N)", "Colori (C)"]
        for i, testo in enumerate(opzioni):
            testo_render = Normalfont.render(testo, True, (0, 0, 0))  # Nero su rosa
            x = (larghezza_schermo - testo_render.get_width()) // 2
            y = 350 + i * 100
            screen.blit(testo_render, (x, y))

    elif dove_siamo == "numeri":
        if not in_gioco_numeri and not gioco_finito:
            # SCHERMATA ISTRUZIONI - SFONDO LAVANDA CHIARO
            screen.fill((230, 220, 250))  # Lilla chiarissimo
            
            titolo_numeri = Titlefont.render("MODALITÀ NUMERI", True, (75, 0, 130))  # Indigo scuro
            x_titolo = (larghezza_schermo - titolo_numeri.get_width()) // 2
            screen.blit(titolo_numeri, (x_titolo, 50))
            
            testi = [
                "Qui giocherai con i numeri!",
                "Il computer penserà a 4 numeri (da 1 a 6)",
                "Tu dovrai indovinarli in 10 tentativi",
                "Premi I per iniziare a giocare",
                "Premi ESC per tornare al menu"
            ]
            
            for i, testo in enumerate(testi):
                testo_render = Normalfont.render(testo, True, (0, 0, 0))  # Nero su lilla
                x = (larghezza_schermo - testo_render.get_width()) // 2
                y = 200 + i * 70
                screen.blit(testo_render, (x, y))
        
        elif in_gioco_numeri:
            # SCHERMATA DI GIOCO - SFONDO LAVANDA MEDIO
            screen.fill((210, 200, 240))  # Lilla medio
            
            titolo_gioco = Titlefont.render("GIOCO NUMERI", True, (75, 0, 130))  # Indigo
            x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
            screen.blit(titolo_gioco, (x_titolo, 30))
            
            # ==============================================
            # RETTANGOLO CON CONSIGLIO (SOLO DOPO 6° TENTATIVO)
            # ==============================================
            if tentativi_fatti >= 6:  # SOLO dopo il 6° tentativo
                rettangolo_consiglio = pygame.Rect(800, 100, 350, 200)
                pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)  # Avorio
                pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)  # Bordo grigio
                
                # Titolo del consiglio
                consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))  # Blu scuro
                screen.blit(consiglio_titolo, (810, 110))
                
                # Analizza il codice per dare un consiglio
                pari = 0
                dispari = 0
                for num in codice_segreto:
                    if int(num) % 2 == 0:
                        pari += 1
                    else:
                        dispari += 1
                
                # Crea il testo del consiglio
                if pari == 4:
                    consiglio_testo = "Tutti i numeri sono PARI"
                    colore_consiglio = (0, 100, 200)  # Blu
                elif dispari == 4:
                    consiglio_testo = "Tutti i numeri sono DISPARI"
                    colore_consiglio = (150, 0, 150)  # Viola
                elif pari > dispari:
                    consiglio_testo = f"Maggioranza PARI"
                    colore_consiglio = (0, 150, 0)  # Verde
                else:
                    consiglio_testo = f"Maggioranza DISPARI"
                    colore_consiglio = (200, 100, 0)  # Arancione
                
                # Mostra il consiglio
                consiglio_line1 = Fontpiccolo.render(consiglio_testo, True, colore_consiglio)
                screen.blit(consiglio_line1, (820, 160))
                
                # Dettagli del consiglio
                consigli_dettagli = [
                    f"Pari: {pari} | Dispari: {dispari}",
                    "Range: numeri da 1 a 6",
                    f"Hai {10 - tentativi_fatti} tentativi rimasti"
                ]
                
                y_pos_consigli = 200
                for dettaglio in consigli_dettagli:
                    testo_det = Fontpiccolo.render(dettaglio, True, (80, 80, 80))  # Grigio scuro
                    screen.blit(testo_det, (820, y_pos_consigli))
                    y_pos_consigli += 30
            else:
                # Messaggio che il consiglio apparirà dopo
                if tentativi_fatti < 6:
                    messaggio_attesa = pygame.Rect(800, 100, 350, 150)
                    pygame.draw.rect(screen, (240, 240, 240), messaggio_attesa, border_radius=15)
                    pygame.draw.rect(screen, (150, 150, 150), messaggio_attesa, 3, border_radius=15)
                    
                    attesa_titolo = Normalfont.render("CONSIGLIO:", True, (100, 100, 100))
                    screen.blit(attesa_titolo, (810, 110))
                    
                    attesa_text1 = Fontpiccolo.render("Disponibile dopo", True, (120, 120, 120))
                    attesa_text2 = Fontpiccolo.render(f"il {6 - tentativi_fatti}° tentativo", True, (120, 120, 120))
                    
                    screen.blit(attesa_text1, (830, 160))
                    screen.blit(attesa_text2, (830, 190))
            
            # ==============================================
            # AREA DI GIOCO PRINCIPALE (sinistra)
            # ==============================================
            
            # Tentativi fatti su 10
            tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))  # Nero
            screen.blit(tentativi_text, (100, 120))
            
            # Input corrente
            input_label = Normalfont.render("Inserisci 4 numeri (1-6):", True, (0, 0, 0))  # Nero
            screen.blit(input_label, (100, 200))
            
            # 4 caselle per l'input
            for i in range(4):
                x = 100 + i * 120
                y = 260
                
                # Casella con colore contrastante
                colore_casella = (180, 220, 255) if i < len(tentativo_corrente) else (255, 255, 255)  # Azzurro/Bianco
                pygame.draw.rect(screen, colore_casella, (x, y, 80, 80), border_radius=10)
                pygame.draw.rect(screen, (0, 100, 200), (x, y, 80, 80), 3, border_radius=10)  # Blu scuro
                
                if i < len(tentativo_corrente):
                    num_text = Normalfont.render(tentativo_corrente[i], True, (0, 0, 0))  # Nero
                    num_x = x + 40 - num_text.get_width() // 2
                    num_y = y + 40 - num_text.get_height() // 2
                    screen.blit(num_text, (num_x, num_y))
                else:
                    segnaposto = Fontpiccolo.render(f"Pos {i+1}", True, (100, 100, 100))  # Grigio
                    segnaposto_x = x + 40 - segnaposto.get_width() // 2
                    segnaposto_y = y + 40 - segnaposto.get_height() // 2
                    screen.blit(segnaposto, (segnaposto_x, segnaposto_y))
            
            # Suggerimenti
            if feedback_dettagliato[0] or storico_tentativi:
                suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))  # Verde scuro
                screen.blit(suggerimenti_label, (100, 380))
                
                y_pos = 430
                if feedback_dettagliato[0]:
                    for i, fb in enumerate(feedback_dettagliato):
                        if fb:
                            colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)  # Verde/Rosso
                            fb_text = Fontpiccolo.render(fb, True, colore)
                            screen.blit(fb_text, (120, y_pos))
                            y_pos += 35
                
                if storico_tentativi and len(storico_tentativi[-1]) > 4:
                    if "Numeri presenti" in storico_tentativi[-1]:
                        presenti_text = storico_tentativi[-1].split(" - ")[1]
                        presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))  # Arancione
                        screen.blit(presenti_render, (120, y_pos))
                        y_pos += 35
            
            # Storico tentativi (ultimi 5)
            if storico_tentativi:
                storico_label = Normalfont.render("Ultimi tentativi:", True, (0, 0, 150))  # Blu scuro
                screen.blit(storico_label, (100, 500))
                
                y_pos = 550
                for i, tent in enumerate(storico_tentativi[-5:]):  # Solo ultimi 5
                    codice_tent = tent.split(" - ")[0] if " - " in tent else tent
                    tent_text = Fontpiccolo.render(f"{i+1}. {codice_tent}", True, (0, 0, 0))  # Nero
                    screen.blit(tent_text, (120, y_pos))
                    y_pos += 35
            
            # Istruzioni durante il gioco
            istruzioni = [
                "Istruzioni:",
                "- Usa tasti 1-6 per inserire numeri",
                "- BACKSPACE cancella, INVIO conferma",
                "- ESC per tornare alle istruzioni"
            ]
            
            y_pos = 680
            for testo in istruzioni:
                colore = (100, 100, 100) if not testo.startswith("Istruzioni") else (0, 0, 0)  # Grigio/Nero
                testo_render = Fontpiccolo.render(testo, True, colore)
                screen.blit(testo_render, (100, y_pos))
                y_pos += 35
        
        elif gioco_finito:
            # SCHERMATA RISULTATO FINALE - SFONDO LAVANDA CHIARO
            screen.fill((230, 220, 250))  # Lilla chiarissimo
            
            # Titolo risultato
            if risultato == "VITTORIA":
                titolo_risultato = Titlefont.render("HAI VINTO! 🎉", True, (0, 150, 0))  # Verde brillante
            else:
                titolo_risultato = Titlefont.render("HAI PERSO! 😔", True, (200, 0, 0))  # Rosso brillante
            
            x_titolo = (larghezza_schermo - titolo_risultato.get_width()) // 2
            screen.blit(titolo_risultato, (x_titolo, 80))
            
            # Info partita
            info1 = Normalfont.render(f"Hai fatto {tentativi_fatti} tentativi su 10", True, (0, 0, 0))
            x_info1 = (larghezza_schermo - info1.get_width()) // 2
            screen.blit(info1, (x_info1, 200))
            
            # MOSTRA IL CODICE CORRETTO
            codice_label = Normalfont.render("Il codice corretto era:", True, (0, 0, 0))
            x_codice_label = (larghezza_schermo - codice_label.get_width()) // 2
            screen.blit(codice_label, (x_codice_label, 280))
            
            # Disegna il codice corretto in 4 caselle
            for i in range(4):
                x = 400 + i * 120
                y = 360
                
                # Casella verde chiaro per il codice corretto
                pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                
                # Numero
                num_text = Normalfont.render(codice_segreto[i], True, (0, 0, 0))
                num_x = x + 40 - num_text.get_width() // 2
                num_y = y + 40 - num_text.get_height() // 2
                screen.blit(num_text, (num_x, num_y))
            
            # Mostra il codice anche come testo
            codice_testo = Normalfont.render(f"{codice_segreto}", True, (0, 100, 0))
            x_codice = (larghezza_schermo - codice_testo.get_width()) // 2
            screen.blit(codice_testo, (x_codice, 460))
            
            # TENTATIVI FATTI (IN COLONNA)
            storico_label = Normalfont.render("I tuoi tentativi:", True, (0, 0, 150))
            screen.blit(storico_label, (100, 500))
            
            # Usa due colonne se ci sono molti tentativi
            if len(storico_tentativi) > 8:
                # DUE COLONNE
                colonna1_x = 120
                colonna2_x = 320
                max_per_colonna = len(storico_tentativi) // 2 + 1
                
                # Colonna 1
                y_pos = 550
                for i in range(max_per_colonna):
                    if i < len(storico_tentativi):
                        tent = storico_tentativi[i]
                        codice_tent = tent.split(" - ")[0] if " - " in tent else tent
                        tent_text = Fontpiccolo.render(f"{i+1}. {codice_tent}", True, (0, 0, 0))
                        screen.blit(tent_text, (colonna1_x, y_pos))
                        y_pos += 35
                
                # Colonna 2
                y_pos = 550
                for i in range(max_per_colonna, len(storico_tentativi)):
                    tent = storico_tentativi[i]
                    codice_tent = tent.split(" - ")[0] if " - " in tent else tent
                    tent_text = Fontpiccolo.render(f"{i+1}. {codice_tent}", True, (0, 0, 0))
                    screen.blit(tent_text, (colonna2_x, y_pos))
                    y_pos += 35
            else:
                # UNA COLONNA
                y_pos = 550
                for i, tent in enumerate(storico_tentativi):
                    codice_tent = tent.split(" - ")[0] if " - " in tent else tent
                    tent_text = Fontpiccolo.render(f"{i+1}. {codice_tent}", True, (0, 0, 0))
                    screen.blit(tent_text, (120, y_pos))
                    y_pos += 35
            
            # ISTRUZIONI PER CONTINUARE
            continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
            x_continua = (larghezza_schermo - continua_text.get_width()) // 2
            screen.blit(continua_text, (x_continua, 750))
            
            rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
            x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
            screen.blit(rigioca_text, (x_rigioca, 800))

    elif dove_siamo == "lettere":
        # SFONDO GIALLO CHIARO (non troppo acceso)
        screen.fill((255, 250, 200))  # Giallo crema
        
        titolo_lettere = Titlefont.render("MODALITÀ LETTERE", True, (200, 100, 0))  # Arancione scuro
        x_titolo = (larghezza_schermo - titolo_lettere.get_width()) // 2
        screen.blit(titolo_lettere, (x_titolo, 50))
        
        # Testi in nero per contrasto sul giallo
        testo_1 = Normalfont.render("Qui giocherai con le lettere!", True, (0, 0, 0))
        testo_2 = Normalfont.render("Il computer penserà a 4 lettere (dalla a alla z)", True, (0, 0, 0))
        testo_3 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, (0, 0, 0))
        testo_4 = Normalfont.render("Premi ESC per tornare al menu", True, (200, 0, 0))  # Rosso
        testo_5 = Normalfont.render("premi I per iniziare", True, (0, 0, 0))
        
        screen.blit(testo_1, ((larghezza_schermo - testo_1.get_width()) // 2, 200))
        screen.blit(testo_2, ((larghezza_schermo - testo_2.get_width()) // 2, 270))
        screen.blit(testo_3, ((larghezza_schermo - testo_3.get_width()) // 2, 340))
        screen.blit(testo_4, ((larghezza_schermo - testo_4.get_width()) // 2, 450))
        screen.blit(testo_5, ((larghezza_schermo - testo_5.get_width()) // 2, 570))

    elif dove_siamo == "colori":
        # SFONDO AZZURRO CHIARO (non troppo acceso)
        screen.fill((200, 230, 255))  # Azzurro chiarissimo
        
        titolo_colori = Titlefont.render("MODALITÀ COLORI", True, (0, 0, 150))  # Blu scuro
        x_titolo = (larghezza_schermo - titolo_colori.get_width()) // 2
        screen.blit(titolo_colori, (x_titolo, 50))
        
        # Testi in nero per contrasto sull'azzurro
        testo__1 = Normalfont.render("Qui giocherai con i colori!", True, (0, 0, 0))
        testo__2 = Normalfont.render("Il computer penserà a 4 colori", True, (0, 0, 0))
        testo__3 = Normalfont.render("I colori possibili sono blu, rosso, arancione, giallo, viola", True, (0, 0, 0))
        testo__4 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, (0, 0, 0))
        testo__5 = Normalfont.render("Premi ESC per tornare al menu", True, (200, 0, 0))  # Rosso
        testo__6 = Normalfont.render("premi I per iniziare", True, (0, 0, 0))
        
        screen.blit(testo__1, ((larghezza_schermo - testo__1.get_width()) // 2, 170))
        screen.blit(testo__2, ((larghezza_schermo - testo__2.get_width()) // 2, 240))
        screen.blit(testo__3, ((larghezza_schermo - testo__3.get_width()) // 2, 300))
        screen.blit(testo__4, ((larghezza_schermo - testo__4.get_width()) // 2, 370))
        screen.blit(testo__5, ((larghezza_schermo - testo__5.get_width()) // 2, 450))
        screen.blit(testo__6, ((larghezza_schermo - testo__6.get_width()) // 2, 570))
    
    pygame.display.flip()

pygame.quit()
