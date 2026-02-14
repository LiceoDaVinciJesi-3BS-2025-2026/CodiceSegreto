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
            if event.key == pygame.K_n and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "numeri"
                print("=== MODALITÀ NUMERI ===")
            
            elif event.key == pygame.K_l and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "lettere"
                print("=== MODALITÀ LETTERE ===")
            
            elif event.key == pygame.K_c and not in_gioco_numeri and not gioco_finito:
                dove_siamo = "colori"
                print("=== MODALITÀ COLORI ===")
            
            elif event.key == pygame.K_i and dove_siamo == "numeri" and not in_gioco_numeri:
                in_gioco_numeri = True
                gioco_finito = False
                tentativi_fatti = 0
                tentativo_corrente = ""
                feedback_dettagliato = ["", "", "", ""]
                storico_tentativi = []
                risultato = ""
                
                codice_segreto = ""
                for cifre in range(4):
                    cifra = random.randint(1, 6)
                    codice_segreto += str(cifra)
                
                print(f"CODICE SEGRETO: {codice_segreto}")
            
            elif event.key == pygame.K_ESCAPE:
                if in_gioco_numeri or gioco_finito:
                    in_gioco_numeri = False
                    gioco_finito = False
                else:
                    dove_siamo = "menu"
                print("Torno indietro")
            
            if in_gioco_numeri and not gioco_finito:
                if pygame.K_1 <= event.key <= pygame.K_6:
                    if len(tentativo_corrente) < 4:
                        numero = chr(event.key)
                        tentativo_corrente += numero
                
                elif event.key == pygame.K_BACKSPACE:
                    tentativo_corrente = tentativo_corrente[:-1]
                
                elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                    tentativi_fatti += 1
                    
                    storico_tentativi.append(tentativo_corrente)
                    
                    feedback_dettagliato = ["", "", "", ""]
                    
                    for pos in range(4):
                        if tentativo_corrente[pos] == codice_segreto[pos]:
                            feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                        else:
                            feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"
                    
                    numeri_presenti = []
                    for pos in range(4):
                        if (tentativo_corrente[pos] != codice_segreto[pos] and 
                            tentativo_corrente[pos] in codice_segreto):
                            if tentativo_corrente[pos] not in numeri_presenti:
                                numeri_presenti.append(tentativo_corrente[pos])
                    
                    print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                    
                    if tentativo_corrente == codice_segreto:
                        risultato = "VITTORIA"
                        gioco_finito = True
                        in_gioco_numeri = False
                        print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                    elif tentativi_fatti >= 10:
                        risultato = "SCONFITTA"
                        gioco_finito = True
                        in_gioco_numeri = False
                        print(f"HAI PERSO! Codice era: {codice_segreto}")
                    else:
                        tentativo_corrente = ""

    if dove_siamo == "menu":
        screen.fill((255, 182, 193))
        
        Titolo = Titlefont.render("CodiceSegreto", True, (0, 0, 0))
        x_titolo = (larghezza_schermo - Titolo.get_width()) // 2
        screen.blit(Titolo, (x_titolo, 150))
        
        opzioni = ["Lettere (L)", "Numeri (N)", "Colori (C)"]
        for i, testo in enumerate(opzioni):
            testo_render = Normalfont.render(testo, True, (0, 0, 0))
            x = (larghezza_schermo - testo_render.get_width()) // 2
            y = 350 + i * 100
            screen.blit(testo_render, (x, y))

    elif dove_siamo == "numeri":
        if not in_gioco_numeri and not gioco_finito:
            screen.fill((230, 220, 250))
            
            titolo_numeri = Titlefont.render("MODALITÀ NUMERI", True, (75, 0, 130))
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
                testo_render = Normalfont.render(testo, True, (0, 0, 0))
                x = (larghezza_schermo - testo_render.get_width()) // 2
                y = 200 + i * 70
                screen.blit(testo_render, (x, y))
        
        elif in_gioco_numeri:
            screen.fill((210, 200, 240))
            
            titolo_gioco = Titlefont.render("GIOCO NUMERI", True, (75, 0, 130))
            x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
            screen.blit(titolo_gioco, (x_titolo, 30))
            
            # ==============================================
            # AREA GIOCO PRINCIPALE (leggermente più in basso)
            # ==============================================
            
            tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
            screen.blit(tentativi_text, (150, 160))  # DA 140 A 160 (20 px più in basso)
            
            input_label = Normalfont.render("Inserisci 4 numeri (1-6):", True, (0, 0, 0))
            screen.blit(input_label, (150, 230))  # DA 200 A 230 (30 px più in basso)
            
            for i in range(4):
                x = 150 + i * 120
                y = 300  # DA 260 A 300 (40 px più in basso)
                
                colore_casella = (180, 220, 255) if i < len(tentativo_corrente) else (255, 255, 255)
                pygame.draw.rect(screen, colore_casella, (x, y, 80, 80), border_radius=10)
                pygame.draw.rect(screen, (0, 100, 200), (x, y, 80, 80), 3, border_radius=10)
                
                if i < len(tentativo_corrente):
                    num_text = Normalfont.render(tentativo_corrente[i], True, (0, 0, 0))
                    num_x = x + 40 - num_text.get_width() // 2
                    num_y = y + 40 - num_text.get_height() // 2
                    screen.blit(num_text, (num_x, num_y))
                else:
                    segnaposto = Fontpiccolo.render(f"Pos {i+1}", True, (100, 100, 100))
                    segnaposto_x = x + 40 - segnaposto.get_width() // 2
                    segnaposto_y = y + 40 - segnaposto.get_height() // 2
                    screen.blit(segnaposto, (segnaposto_x, segnaposto_y))
            
            # ==============================================
            # SUGGERIMENTI (a destra, allineati)
            # ==============================================
            if feedback_dettagliato[0] or storico_tentativi:
                suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                screen.blit(suggerimenti_label, (700, 160))  # Allineato con tentativi
                
                y_pos = 210  # DA 190 A 210
                if feedback_dettagliato[0]:
                    for i, fb in enumerate(feedback_dettagliato):
                        if fb:
                            colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)
                            fb_text = Fontpiccolo.render(fb, True, colore)
                            screen.blit(fb_text, (720, y_pos))
                            y_pos += 30
                
                if storico_tentativi:
                    ultimo = storico_tentativi[-1]
                    numeri_presenti = []
                    for pos in range(4):
                        if (ultimo[pos] != codice_segreto[pos] and 
                            ultimo[pos] in codice_segreto):
                            if ultimo[pos] not in numeri_presenti:
                                numeri_presenti.append(ultimo[pos])
                    
                    if numeri_presenti:
                        presenti_text = f"Presenti: {', '.join(numeri_presenti)}"
                        presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                        screen.blit(presenti_render, (720, y_pos))
                        y_pos += 30
            
            # ==============================================
            # ULTIMI TENTATIVI (a destra, più in basso)
            # ==============================================
            if storico_tentativi:
                storico_label = Normalfont.render("ULTIMI TENTATIVI:", True, (0, 0, 150))
                screen.blit(storico_label, (700, 380))  # DA 340 A 380
                
                y_pos = 430  # DA 390 A 430
                inizio = max(0, len(storico_tentativi) - 5)
                for i in range(inizio, len(storico_tentativi)):
                    numero = i + 1
                    codice = storico_tentativi[i]
                    tent_text = Fontpiccolo.render(f"{numero}) {codice}", True, (0, 0, 0))
                    screen.blit(tent_text, (720, y_pos))
                    y_pos += 35
            
            # ==============================================
            # CONSIGLIO (più in basso)
            # ==============================================
            rettangolo_consiglio = pygame.Rect(150, 440, 380, 240)  # DA 380 A 440 (60 px più in basso)
            pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)
            
            consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))
            screen.blit(consiglio_titolo, (160, 450))  # DA 390 A 450
            
            if tentativi_fatti >= 6:
                pari = 0
                dispari = 0
                for num in codice_segreto:
                    if int(num) % 2 == 0:
                        pari += 1
                    else:
                        dispari += 1
                
                if pari == 4:
                    consiglio_testo = "Tutti i numeri sono PARI"
                    colore_consiglio = (0, 100, 200)
                elif dispari == 4:
                    consiglio_testo = "Tutti i numeri sono DISPARI"
                    colore_consiglio = (150, 0, 150)
                elif pari > dispari:
                    consiglio_testo = "Maggioranza PARI"
                    colore_consiglio = (0, 150, 0)
                else:
                    consiglio_testo = "Maggioranza DISPARI"
                    colore_consiglio = (200, 100, 0)
                
                consiglio_line1 = Fontpiccolo.render(consiglio_testo, True, colore_consiglio)
                screen.blit(consiglio_line1, (170, 500))  # DA 440 A 500
                
                consigli_dettagli = [
                    f"Pari: {pari} | Dispari: {dispari}",
                    "Range: numeri da 1 a 6",
                    f"Hai {10 - tentativi_fatti} tentativi rimasti"
                ]
                
                y_pos_consigli = 540  # DA 480 A 540
                for dettaglio in consigli_dettagli:
                    testo_det = Fontpiccolo.render(dettaglio, True, (80, 80, 80))
                    screen.blit(testo_det, (170, y_pos_consigli))
                    y_pos_consigli += 30
            else:
                tentativi_mancanti = 6 - tentativi_fatti
                
                if tentativi_mancanti == 1:
                    messaggio = f"Disponibile tra 1 tentativo"
                else:
                    messaggio = f"Disponibile tra {tentativi_mancanti} tentativi"
                
                testo_attesa = Fontpiccolo.render(messaggio, True, (150, 150, 150))
                screen.blit(testo_attesa, (200, 520))  # DA 460 A 520
            
            # ==============================================
            # ISTRUZIONI (lasciate uguali)
            # ==============================================
            istruzioni = [
                "ISTRUZIONI:",
                "- Usa tasti 1-6 per inserire numeri",
                "- BACKSPACE cancella",
                "- INVIO conferma",
                "- ESC per tornare"
            ]
            
            y_pos = 700  # DA 680 A 700 (20 px più in basso)
            for testo in istruzioni:
                colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                testo_render = Fontpiccolo.render(testo, True, colore)
                screen.blit(testo_render, (150, y_pos))
                y_pos += 30
        
        elif gioco_finito:
            screen.fill((230, 220, 250))
            
            if risultato == "VITTORIA":
                titolo_risultato = Titlefont.render("HAI VINTO!", True, (0, 150, 0))
            else:
                titolo_risultato = Titlefont.render("HAI PERSO!", True, (200, 0, 0))
            
            x_titolo = (larghezza_schermo - titolo_risultato.get_width()) // 2
            screen.blit(titolo_risultato, (x_titolo, 80))
            
            info1 = Normalfont.render(f"Hai fatto {tentativi_fatti} tentativi su 10", True, (0, 0, 0))
            x_info1 = (larghezza_schermo - info1.get_width()) // 2
            screen.blit(info1, (x_info1, 200))
            
            codice_label = Normalfont.render("Il codice corretto era:", True, (0, 0, 0))
            x_codice_label = (larghezza_schermo - codice_label.get_width()) // 2
            screen.blit(codice_label, (x_codice_label, 280))
            
            x_inizio_caselle = (larghezza_schermo - (4 * 120)) // 2
            for i in range(4):
                x = x_inizio_caselle + i * 120
                y = 360
                
                pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                
                num_text = Normalfont.render(codice_segreto[i], True, (0, 0, 0))
                num_x = x + 40 - num_text.get_width() // 2
                num_y = y + 40 - num_text.get_height() // 2
                screen.blit(num_text, (num_x, num_y))
            
            codice_testo = Normalfont.render(f"{codice_segreto}", True, (0, 100, 0))
            x_codice = (larghezza_schermo - codice_testo.get_width()) // 2
            screen.blit(codice_testo, (x_codice, 460))
            
            continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
            x_continua = (larghezza_schermo - continua_text.get_width()) // 2
            screen.blit(continua_text, (x_continua, 550))
            
            rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
            x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
            screen.blit(rigioca_text, (x_rigioca, 620))

    elif dove_siamo == "lettere":
        screen.fill((255, 250, 200))
        
        titolo_lettere = Titlefont.render("MODALITÀ LETTERE", True, (200, 100, 0))
        x_titolo = (larghezza_schermo - titolo_lettere.get_width()) // 2
        screen.blit(titolo_lettere, (x_titolo, 50))
        
        testo_1 = Normalfont.render("Qui giocherai con le lettere!", True, (0, 0, 0))
        testo_2 = Normalfont.render("Il computer penserà a 4 lettere (dalla a alla z)", True, (0, 0, 0))
        testo_3 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, (0, 0, 0))
        testo_4 = Normalfont.render("Premi ESC per tornare al menu", True, (200, 0, 0))
        testo_5 = Normalfont.render("premi I per iniziare", True, (0, 0, 0))
        
        screen.blit(testo_1, ((larghezza_schermo - testo_1.get_width()) // 2, 200))
        screen.blit(testo_2, ((larghezza_schermo - testo_2.get_width()) // 2, 270))
        screen.blit(testo_3, ((larghezza_schermo - testo_3.get_width()) // 2, 340))
        screen.blit(testo_4, ((larghezza_schermo - testo_4.get_width()) // 2, 450))
        screen.blit(testo_5, ((larghezza_schermo - testo_5.get_width()) // 2, 570))

    elif dove_siamo == "colori":
        screen.fill((200, 230, 255))
        
        titolo_colori = Titlefont.render("MODALITÀ COLORI", True, (0, 0, 150))
        x_titolo = (larghezza_schermo - titolo_colori.get_width()) // 2
        screen.blit(titolo_colori, (x_titolo, 50))
        
        testo__1 = Normalfont.render("Qui giocherai con i colori!", True, (0, 0, 0))
        testo__2 = Normalfont.render("Il computer penserà a 4 colori", True, (0, 0, 0))
        testo__3 = Normalfont.render("I colori possibili sono blu, rosso, arancione, giallo, viola", True, (0, 0, 0))
        testo__4 = Normalfont.render("Tu dovrai indovinarli in 10 tentativi", True, (0, 0, 0))
        testo__5 = Normalfont.render("Premi ESC per tornare al menu", True, (200, 0, 0))
        testo__6 = Normalfont.render("premi I per iniziare", True, (0, 0, 0))
        
        screen.blit(testo__1, ((larghezza_schermo - testo__1.get_width()) // 2, 170))
        screen.blit(testo__2, ((larghezza_schermo - testo__2.get_width()) // 2, 240))
        screen.blit(testo__3, ((larghezza_schermo - testo__3.get_width()) // 2, 300))
        screen.blit(testo__4, ((larghezza_schermo - testo__4.get_width()) // 2, 370))
        screen.blit(testo__5, ((larghezza_schermo - testo__5.get_width()) // 2, 450))
        screen.blit(testo__6, ((larghezza_schermo - testo__6.get_width()) // 2, 570))
    
    pygame.display.flip()

pygame.quit()
