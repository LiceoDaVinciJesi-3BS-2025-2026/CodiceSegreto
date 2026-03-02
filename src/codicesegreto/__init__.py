import pygame
import random
import json
import os

# ==============================================
# FUNZIONI DI SALVATAGGIO
# ==============================================
FILE_GIOCATORI = "giocatori.json"

def carica_giocatori():
    """Carica i dati dei giocatori dal file JSON"""
    if os.path.exists(FILE_GIOCATORI):
        with open(FILE_GIOCATORI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salva_giocatori(giocatori):
    """Salva i dati dei giocatori nel file JSON"""
    with open(FILE_GIOCATORI, "w", encoding="utf-8") as f:
        json.dump(giocatori, f, indent=4, ensure_ascii=False)

def main() -> None:
    print("Hello from codicesegreto!")

    pygame.init()
    
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("CodiceSegreto")
    
    Titlefont = pygame.font.SysFont('Arial', 100)
    Normalfont = pygame.font.SysFont('Arial', 50)
    Fontpiccolo = pygame.font.SysFont('Arial', 30)
    
    larghezza_schermo = 1200
    altezza_schermo = 900
    
    # VARIABILI DI STATO
    stato = "login"  # "login" o "menu" o "gioco"
    dove_siamo = "menu"
    running = True
    
    # VARIABILI PER IL GIOCATORE
    giocatori = carica_giocatori()
    nome_giocatore = ""
    input_testo = ""
    
    # VARIABILI PER IL GIOCO
    
    in_gioco_numeri = False
    codice_segreto = ""
    tentativo_corrente = ""
    tentativi_fatti = 0
    feedback_dettagliato = ["", "", "", ""]
    storico_tentativi = []  # Qui salviamo TUTTI i codici in ordine
    gioco_finito = False
    risultato = ""
    in_gioco_lettere = False
    in_gioco_colori = False
    
    # LISTA COLORI DISPONIBILI (in RGB) per la modalità colori
    colori_disponibili = [
        (255, 0, 0),    # 1 Rosso
        (255, 255, 0),  # 2 Giallo
        (0, 0, 255),    # 3 Blu
        (128, 0, 128),  # 4 Viola
        (255, 165, 0),  # 5 Arancione
        (0, 255, 0),    # 6 Verde
        (255, 255, 255),# 7 Bianco
        (128, 128, 128),# 8 Grigio
    ]
    
    # NOMI DEI COLORI
    nomi_colori = {
        1: "Rosso",
        2: "Giallo",
        3: "Blu",
        4: "Viola",
        5: "Arancione",
        6: "Verde",
        7: "Bianco",
        8: "Grigio"
    }
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Salva prima di uscire
                if nome_giocatore:
                    giocatori[nome_giocatore] = {"nome": nome_giocatore}
                    salva_giocatori(giocatori)
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # ==============================================
                # STATO LOGIN - inserimento nome
                # ==============================================
                if stato == "login":
                    if event.key == pygame.K_RETURN and input_testo:
                        # Conferma nome
                        nome_giocatore = input_testo
                        if nome_giocatore in giocatori:
                            print(f"Bentornato {nome_giocatore}!")
                        else:
                            giocatori[nome_giocatore] = {"nome": nome_giocatore}
                            print(f"Benvenuto {nome_giocatore}!")
                        
                        stato = "menu"
                        dove_siamo = "menu"
                        input_testo = ""
                        continue
                    
                    elif event.key == pygame.K_BACKSPACE:
                        input_testo = input_testo[:-1]
                    
                    elif event.key <= 127 and event.unicode.isprintable():
                        if len(input_testo) < 15:
                            input_testo += event.unicode

                #========================================
                #STATO MENU
                #========================================
                    
                elif stato == "menu":
                    #schermata numeri
                    if event.key == pygame.K_n and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "numeri"
                        stato = "gioco"
                        print("=== MODALITÀ NUMERI ===")
                        
                    #schermata lettere
                    elif event.key == pygame.K_l and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "lettere"
                        stato = "gioco"
                        print("=== MODALITÀ LETTERE ===")
                        
                    #schermata colori
                    elif event.key == pygame.K_c and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "colori"
                        stato = "gioco"
                        print("=== MODALITÀ COLORI ===")

                    #schermata login
                    elif event.key == pygame.K_ESCAPE:
                        stato = "login"
                        input_testo = ""
                        print("Torna al login")
                        continue
                
                # ==============================================
                # STATO GIOCO
                # ==============================================
                elif stato == "gioco":

                    #=============================
                    # A COSA SERVE????
                    #=============================
                    
                    if event.key == pygame.K_n and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "numeri"
                        print("=== MODALITÀ NUMERI ===")
                    
                    elif event.key == pygame.K_l and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "lettere"
                        print("=== MODALITÀ LETTERE ===")
                    
                    elif event.key == pygame.K_c and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "colori"
                        print("=== MODALITÀ COLORI ===")
                    
                    # tasto I per iniziare numeri
                    elif event.key == pygame.K_i and dove_siamo == "numeri" and not in_gioco_numeri:
                        in_gioco_numeri = True
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""

                        #genera CODICE SEGRETO per i numeri
                        codice_segreto = ""
                        for cifre in range(4):
                            cifra = random.randint(1, 6)
                            codice_segreto += str(cifra)
                        
                        print(f"CODICE SEGRETO: {codice_segreto}")
                        continue
                        
                    # tasto i per iniziare lettere
                    elif event.key == pygame.K_i and dove_siamo == "lettere" and not in_gioco_lettere:
                        in_gioco_lettere = True
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""
        
                        # genera CODICE SEGRETO per le lettere
                        codice_segreto = ""
                        for _ in range(4):
                            lettera = chr(random.randint(97, 122))
                            codice_segreto += lettera
                        
                        print(f"CODICE SEGRETO LETTERE: {codice_segreto}")
                        continue
        
                    # tasto i per iniziare colori
                    elif event.key == pygame.K_i and dove_siamo == "colori" and not in_gioco_colori:
                        in_gioco_colori = True
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""
        
                        # genera 4 numeri casuali da 1 a 8
                        #CODICE SERETO per i colori
                        codice_segreto = []
                        for _ in range(4):
                            colore = random.randint(1, 8)
                            codice_segreto.append(colore)
                        
                        print(f"CODICE SEGRETO COLORI: {codice_segreto}")
                        continue
        
                    elif event.key == pygame.K_ESCAPE:
                        if in_gioco_numeri or in_gioco_lettere or in_gioco_colori or gioco_finito:
                            in_gioco_numeri = False
                            in_gioco_lettere = False
                            in_gioco_colori = False
                            gioco_finito = False
                            stato = "menu"
                            dove_siamo = "menu"
                        else:
                            stato = "menu"
                            dove_siamo = "menu"
                        print("Torno al menu")
                        continue
                    
                    # ==============================================
                    # GESTIONE TASTI NELLA SCHERMATA DI FINE GIOCO
                    # ==============================================
                    if gioco_finito:
                        if event.key == pygame.K_i:
                            # Ricomincia nella stessa modalità
                            if dove_siamo == "numeri":
                                in_gioco_numeri = True
                                gioco_finito = False
                                tentativi_fatti = 0
                                tentativo_corrente = ""
                                feedback_dettagliato = ["", "", "", ""]
                                storico_tentativi = []
                                risultato = ""
                                
                                codice_segreto = ""
                                for _ in range(4):
                                    cifra = random.randint(1, 6)
                                    codice_segreto += str(cifra)
                                #PERCHE DEVE SCRIVERLO??
                                print(f"NUOVO CODICE NUMERI: {codice_segreto}")
                                continue
                            
                            elif dove_siamo == "lettere":
                                in_gioco_lettere = True
                                gioco_finito = False
                                tentativi_fatti = 0
                                tentativo_corrente = ""
                                feedback_dettagliato = ["", "", "", ""]
                                storico_tentativi = []
                                risultato = ""
                                
                                codice_segreto = ""
                                for _ in range(4):
                                    lettera = chr(random.randint(97, 122))
                                    codice_segreto += lettera
                                #PERCHE DEVE SCRIVERLO??
                                print(f"NUOVO CODICE LETTERE: {codice_segreto}")
                                continue
                            
                            elif dove_siamo == "colori":
                                in_gioco_colori = True
                                gioco_finito = False
                                tentativi_fatti = 0
                                tentativo_corrente = ""
                                feedback_dettagliato = ["", "", "", ""]
                                storico_tentativi = []
                                risultato = ""
                                
                                codice_segreto = []
                                for _ in range(4):
                                    colore = random.randint(1, 8)
                                    codice_segreto.append(colore)
                                #PERCHE DEVE SCRIVERLO??
                                print(f"NUOVO CODICE COLORI: {codice_segreto}")
                                continue
                        
                        elif event.key == pygame.K_ESCAPE:
                            # Torna alle istruzioni della modalità corrente
                            if dove_siamo == "numeri":
                                in_gioco_numeri = False
                            elif dove_siamo == "lettere":
                                in_gioco_lettere = False
                            elif dove_siamo == "colori":
                                in_gioco_colori = False
                            gioco_finito = False
                            stato = "menu"
                            dove_siamo = "menu"
                            print("Torno al menu")
                            continue
        
                    # ==============================================
                    # GESTIONE INPUT NUMERI
                    # ==============================================
                    
                    if in_gioco_numeri and not gioco_finito:
                    
                        #inserimento del codice da parte dell'utente
                        if pygame.K_1 <= event.key <= pygame.K_6:
                            if len(tentativo_corrente) < 4:
                                numero = chr(event.key)
                                tentativo_corrente += numero

                        #elimina l'ultima lettera scritta
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]
                        
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1
                            
                            # SALVA IL TENTATIVO NELLO STORICO
                            storico_tentativi.append(tentativo_corrente)
                            
                            # Controllo del codice segreto
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if tentativo_corrente[pos] == codice_segreto[pos]:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                                else:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"

                            #controllo dei numeri presenti nelle posizioni sbagliate
                            numeri_presenti = []
                            for pos in range(4):
                                if (tentativo_corrente[pos] != codice_segreto[pos] and 
                                    tentativo_corrente[pos] in codice_segreto):
                                    if tentativo_corrente[pos] not in numeri_presenti:
                                        numeri_presenti.append(tentativo_corrente[pos])
                            
                            print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")

                            #condizione della vittoria
                            if tentativo_corrente == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_numeri = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                                
                            #condizione della sconfitta
                            elif tentativi_fatti >= 10:
                                risultato = "SCONFITTA"
                                gioco_finito = True
                                in_gioco_numeri = False
                                print(f"HAI PERSO! Il codice era: {codice_segreto}")
                            else:
                                tentativo_corrente = ""
        
                    # ==============================================
                    # GESTIONE INPUT LETTERE
                    # ==============================================
                    if in_gioco_lettere and not gioco_finito:
                        #inserimento lettere dalla A alla Z
                        if pygame.K_a <= event.key <= pygame.K_z:
                            if len(tentativo_corrente) < 4:
                                lettera = chr(event.key)
                                tentativo_corrente += lettera

                        #elimina l'ultima lettera scritta
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]

                        #invia il tentativo, solo se sono state inserite tutte le lettere
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1
                            
                            # SALVA IL TENTATIVO NELLO STORICO
                            storico_tentativi.append(tentativo_corrente)
                            
                            # CALCOLA FEEDBACK DETTAGLIATO
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if tentativo_corrente[pos] == codice_segreto[pos]:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                                else:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"
                            
                            lettere_presenti = []
                            for pos in range(4):
                                if (tentativo_corrente[pos] != codice_segreto[pos] and 
                                    tentativo_corrente[pos] in codice_segreto):
                                    if tentativo_corrente[pos] not in lettere_presenti:
                                        lettere_presenti.append(tentativo_corrente[pos])
                            
                            print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                            
                            if tentativo_corrente == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_lettere = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                            elif tentativi_fatti >= 10:
                                risultato = "SCONFITTA"
                                gioco_finito = True
                                in_gioco_lettere = False
                                print(f"HAI PERSO! Codice era: {codice_segreto}")
                            else:
                                tentativo_corrente = ""
        
                    # ==============================================
                    # GESTIONE INPUT COLORI
                    # ==============================================
                    if in_gioco_colori and not gioco_finito:
                        # Usa i tasti 1-8
                        if pygame.K_1 <= event.key <= pygame.K_8:
                            if len(tentativo_corrente) < 4:
                                numero = chr(event.key)
                                tentativo_corrente += numero
                        
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]
                        
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1
                            
                            # SALVA IL TENTATIVO COME STRINGA DI NUMERI
                            storico_tentativi.append(tentativo_corrente)
                            
                            # CALCOLA FEEDBACK DETTAGLIATO
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if pos < len(tentativo_corrente) and pos < len(codice_segreto):
                                    if int(tentativo_corrente[pos]) == codice_segreto[pos]:
                                        feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} {nomi_colori[int(tentativo_corrente[pos])]} CORRETTO"
                                    else:
                                        feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} {nomi_colori[int(tentativo_corrente[pos])]} SBAGLIATO"
                            
                            # Controlla vittoria
                            tentativo_lista = [int(x) for x in tentativo_corrente]
                            
                            if tentativo_lista == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_colori = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                            elif tentativi_fatti >= 10:
                                risultato = "SCONFITTA"
                                gioco_finito = True
                                in_gioco_colori = False
                                print(f"HAI PERSO! Codice era: {codice_segreto}")
                            else:
                                tentativo_corrente = ""
        
        #====================================        
        # DISEGNA SCHERMATE
        #====================================
        
        # ==============================================
        # SCHERMATA LOGIN
        # ==============================================
        if stato == "login":
            screen.fill((200, 220, 240))
            
            titolo = Titlefont.render("CODICE SEGRETO", True, (0, 0, 150))
            x_titolo = (larghezza_schermo - titolo.get_width()) // 2
            screen.blit(titolo, (x_titolo, 200))
            
            sottotitolo = Normalfont.render("Inserisci il tuo nome:", True, (0, 0, 0))
            x_sotto = (larghezza_schermo - sottotitolo.get_width()) // 2
            screen.blit(sottotitolo, (x_sotto, 320))
            
            # Riquadro per il nome (più grande)
            rect_nome = pygame.Rect(350, 380, 500, 70)
            pygame.draw.rect(screen, (255, 255, 255), rect_nome, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect_nome, 3, border_radius=10)
            
            # Testo inserito (centrato)
            testo_render = Normalfont.render(input_testo, True, (0, 0, 0))
            testo_x = rect_nome.x + (rect_nome.width - testo_render.get_width()) // 2
            testo_y = rect_nome.y + (rect_nome.height - testo_render.get_height()) // 2
            screen.blit(testo_render, (testo_x, testo_y))
            
            # Istruzioni
            istruzioni = Fontpiccolo.render("Premi INVIO per continuare", True, (100, 100, 100))
            x_istr = (larghezza_schermo - istruzioni.get_width()) // 2
            screen.blit(istruzioni, (x_istr, 480))
        
        # ==============================================
        # SCHERMATA MENU
        # ==============================================
        elif stato == "menu":
            # Il tuo codice menu originale, con l'aggiunta del nome utente
            screen.fill((255, 182, 193))
            
            # Aggiunta nome utente in alto a destra
            nome_text = Fontpiccolo.render(f"Utente: {nome_giocatore}", True, (0, 0, 0))
            screen.blit(nome_text, (1000, 50))
            
            Titolo = Titlefont.render("CodiceSegreto", True, (0, 0, 0))
            x_titolo = (larghezza_schermo - Titolo.get_width()) // 2
            screen.blit(Titolo, (x_titolo, 150))
            
            opzioni = ["Lettere (L)", "Numeri (N)", "Colori (C)"]
            for i, testo in enumerate(opzioni):
                testo_render = Normalfont.render(testo, True, (0, 0, 0))
                x = (larghezza_schermo - testo_render.get_width()) // 2
                y = 350 + i * 100
                screen.blit(testo_render, (x, y))
            
            # Istruzione per cambiare utente
            cambio = Fontpiccolo.render("Premi ESC per cambiare utente", True, (100, 100, 100))
            x_cambio = (larghezza_schermo - cambio.get_width()) // 2
            screen.blit(cambio, (x_cambio, 750))
        
        # ==============================================
        # STATO GIOCO
        # ==============================================
        elif stato == "gioco":
            
            #====================================        
            # NUMERI
            #====================================
            if dove_siamo == "numeri":
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
                    
                    tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                    screen.blit(tentativi_text, (150, 160))
                    
                    input_label = Normalfont.render("Inserisci 4 numeri (1-6):", True, (0, 0, 0))
                    screen.blit(input_label, (150, 230))
                    
                    for i in range(4):
                        x = 150 + i * 120
                        y = 300
                        
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
                    # SUGGERIMENTI
                    # ==============================================
                    if feedback_dettagliato[0] or storico_tentativi:
                        suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                        screen.blit(suggerimenti_label, (700, 160))
                        
                        y_pos = 210
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
                    # TUTTI I TENTATIVI
                    # ==============================================
                    if storico_tentativi:
                        storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                        screen.blit(storico_label, (700, 370))
                        
                        y_pos = 420
                        for i, codice in enumerate(storico_tentativi):
                            numero = i + 1
                            tent_text = Fontpiccolo.render(f"{numero}) {codice}", True, (0, 0, 0))
                            screen.blit(tent_text, (720, y_pos))
                            y_pos += 30
                    
                    # ==============================================
                    # CONSIGLIO
                    # ==============================================
                    rettangolo_consiglio = pygame.Rect(150, 440, 380, 180)
                    pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)
                    pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)
        
                    # Titolo del consiglio 
                    consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))
                    x_titolo_consiglio = rettangolo_consiglio.x + (rettangolo_consiglio.width - consiglio_titolo.get_width()) // 2
                    screen.blit(consiglio_titolo, (x_titolo_consiglio, 455))

                    #calcolo del consiglio
                    if tentativi_fatti >= 6:
                        pari = 0
                        dispari = 0
                        for num in codice_segreto:
                            if int(num) % 2 == 0:
                                pari += 1
                            else:
                                dispari += 1
                        
                        #scrittura del consiglio
                        if pari == 4:
                            testo_maggioranza = "Tutti PARI"
                        elif dispari == 4:
                            testo_maggioranza = "Tutti DISPARI"
                        elif pari > dispari:
                            testo_maggioranza = "Maggioranza PARI"
                        else:
                            testo_maggioranza = "Maggioranza DISPARI"
                            
                        testo_magg_render = Fontpiccolo.render(testo_maggioranza, True, (0, 100, 200))
                        x_magg = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_magg_render.get_width()) // 2
                        screen.blit(testo_magg_render, (x_magg, 500))
                        
                        # Testo pari (centrato)
                        testo_pari = f"Pari: {pari}"
                        testo_pari_render = Fontpiccolo.render(testo_pari, True, (80, 80, 80))
                        x_pari = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_pari_render.get_width()) // 2
                        screen.blit(testo_pari_render, (x_pari, 540))
                        
                        # Testo dispari (centrato)
                        testo_dispari = f"Dispari: {dispari}"
                        testo_dispari_render = Fontpiccolo.render(testo_dispari, True, (80, 80, 80))
                        x_dispari = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_dispari_render.get_width()) // 2
                        screen.blit(testo_dispari_render, (x_dispari, 570))
                    else:
                        # Messaggio di attesa (centrato)
                        tentativi_mancanti = 6 - tentativi_fatti
                        
                        if tentativi_mancanti == 1:
                            messaggio = f"Disponibile tra 1 tentativo"
                        else:
                            messaggio = f"Disponibile tra {tentativi_mancanti} tentativi"
                        
                        testo_attesa = Fontpiccolo.render(messaggio, True, (150, 150, 150))
                        x_attesa = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_attesa.get_width()) // 2
                        screen.blit(testo_attesa, (x_attesa, 520))
                    
                    # ==============================================
                    # ISTRUZIONI NUMERI
                    # ==============================================
                    istruzioni = [
                        "ISTRUZIONI:",
                        "- Usa tasti 1-6 per inserire numeri",
                        "- BACKSPACE cancella",
                        "- INVIO conferma",
                        "- ESC per tornare"
                    ]
        
                    y_pos = 670
                    for testo in istruzioni:
                        colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                        testo_render = Fontpiccolo.render(testo, True, colore)
                        screen.blit(testo_render, (150, y_pos))
                        y_pos += 30
                
                elif gioco_finito:
                    #-------------------------------
                    # SCHERMATA FINE GIOCO NUMERI
                    #-------------------------------
                    
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
                        x = x_inizio_caselle + i * 130
                        y = 360
                        
                        pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                        pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                        
                        num_text = Normalfont.render(codice_segreto[i], True, (0, 0, 0))
                        num_x = x + 40 - num_text.get_width() // 2
                        num_y = y + 40 - num_text.get_height() // 2
                        screen.blit(num_text, (num_x, num_y))
                    
                    continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                    x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                    screen.blit(continua_text, (x_continua, 550))
                    
                    rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                    x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                    screen.blit(rigioca_text, (x_rigioca, 620))
        
            #==================================================
            # LETTERE
            #==================================================
            elif dove_siamo == "lettere":
                if not in_gioco_lettere and not gioco_finito:
                    # SCHERMATA ISTRUZIONI LETTERE
                    screen.fill((255, 250, 200))
                    
                    titolo_lettere = Titlefont.render("MODALITÀ LETTERE", True, (200, 100, 0))
                    x_titolo = (larghezza_schermo - titolo_lettere.get_width()) // 2
                    screen.blit(titolo_lettere, (x_titolo, 50))
                    
                    testi = [
                        "Qui giocherai con le lettere!",
                        "Il computer penserà a 4 lettere (dalla a alla z)",
                        "Tu dovrai indovinarle in 10 tentativi",
                        "Premi I per iniziare a giocare",
                        "Premi ESC per tornare al menu"
                    ]
                    
                    for i, testo in enumerate(testi):
                        testo_render = Normalfont.render(testo, True, (0, 0, 0))
                        x = (larghezza_schermo - testo_render.get_width()) // 2
                        y = 200 + i * 70
                        screen.blit(testo_render, (x, y))
                
                elif in_gioco_lettere:
                    # SCHERMATA DI GIOCO LETTERE
                    screen.fill((210, 200, 240))
                    
                    titolo_gioco = Titlefont.render("GIOCO LETTERE", True, (75, 0, 130))
                    x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
                    screen.blit(titolo_gioco, (x_titolo, 30))
                    
                    # AREA GIOCO LETTERE PRINCIPALE
                    tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                    screen.blit(tentativi_text, (150, 160))
                    
                    input_label = Normalfont.render("Inserisci 4 lettere (a-z):", True, (0, 0, 0))
                    screen.blit(input_label, (150, 230))
                    
                    for i in range(4):
                        x = 150 + i * 120
                        y = 300
                        
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
                    
                    # SUGGERIMENTI PER LE LETTERE
                    
                    if feedback_dettagliato[0] or storico_tentativi:
                        suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                        screen.blit(suggerimenti_label, (700, 160))
                        
                        y_pos = 210
                        if feedback_dettagliato[0]:
                            for i, fb in enumerate(feedback_dettagliato):
                                if fb:
                                    colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)
                                    fb_text = Fontpiccolo.render(fb, True, colore)
                                    screen.blit(fb_text, (720, y_pos))
                                    y_pos += 30
                        
                        if storico_tentativi:
                            ultimo = storico_tentativi[-1]
                            lettere_presenti = []
                            for pos in range(4):
                                if (ultimo[pos] != codice_segreto[pos] and 
                                    ultimo[pos] in codice_segreto):
                                    if ultimo[pos] not in lettere_presenti:
                                        lettere_presenti.append(ultimo[pos])
                            
                            if lettere_presenti:
                                presenti_text = f"Presenti: {', '.join(lettere_presenti)}"
                                presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                                screen.blit(presenti_render, (720, y_pos))
                                y_pos += 30
                    
                    #scrittura tentativi lettere
                    if storico_tentativi:
                        storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                        screen.blit(storico_label, (700, 370))
                        
                        y_pos = 420
                        for i, codice in enumerate(storico_tentativi):
                            numero = i + 1
                            tent_text = Fontpiccolo.render(f"{numero}) {codice}", True, (0, 0, 0))
                            screen.blit(tent_text, (720, y_pos))
                            y_pos += 30
                    
                    # ==============================================
                    # CONSIGLIO LETTERE
                    # ==============================================
                    rettangolo_consiglio = pygame.Rect(150, 440, 380, 200)
                    pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)
                    pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)
                    
                    # Titolo del consiglio (centrato)
                    consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))
                    x_titolo_consiglio = rettangolo_consiglio.x + (rettangolo_consiglio.width - consiglio_titolo.get_width()) // 2
                    screen.blit(consiglio_titolo, (x_titolo_consiglio, 455))
                    
                    if tentativi_fatti >= 6:
                        # Analizza il codice per vocali/consonanti
                        vocali = ['a', 'e', 'i', 'o', 'u']
                        conteggio_vocali = 0
                        conteggio_consonanti = 0
                        
                        for lettera in codice_segreto:
                            if lettera in vocali:
                                conteggio_vocali += 1
                            else:
                                conteggio_consonanti += 1
                        
                        # Testo maggioranza
                        if conteggio_vocali == 4:
                            testo_maggioranza = "Tutte VOCALI"
                        elif conteggio_consonanti == 4:
                            testo_maggioranza = "Tutte CONSONANTI"
                        elif conteggio_vocali > conteggio_consonanti:
                            testo_maggioranza = "Maggioranza VOCALI"
                        else:
                            testo_maggioranza = "Maggioranza CONSONANTI"
                        
                        testo_magg_render = Fontpiccolo.render(testo_maggioranza, True, (150, 0, 150))
                        x_magg = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_magg_render.get_width()) // 2
                        screen.blit(testo_magg_render, (x_magg, 500))
                       
                        testo_vocali = f"Vocali: {conteggio_vocali}"
                        testo_vocali_render = Fontpiccolo.render(testo_vocali, True, (80, 80, 80))
                        x_vocali = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_vocali_render.get_width()) // 2
                        screen.blit(testo_vocali_render, (x_vocali, 540))
                       
                        testo_consonanti = f"Consonanti: {conteggio_consonanti}"
                        testo_consonanti_render = Fontpiccolo.render(testo_consonanti, True, (80, 80, 80))
                        x_consonanti = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_consonanti_render.get_width()) // 2
                        screen.blit(testo_consonanti_render, (x_consonanti, 570))
                    else:
                        # Messaggio di attesa
                        tentativi_mancanti = 6 - tentativi_fatti
                        
                        if tentativi_mancanti == 1:
                            messaggio = f"Disponibile tra 1 tentativo"
                        else:
                            messaggio = f"Disponibile tra {tentativi_mancanti} tentativi"
                        
                        testo_attesa = Fontpiccolo.render(messaggio, True, (150, 150, 150))
                        x_attesa = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_attesa.get_width()) // 2
                        screen.blit(testo_attesa, (x_attesa, 520))
                        
                    #-----------------------
                    # ISTRUZIONI LETTERE
                    #-----------------------
                    istruzioni = [
                        "ISTRUZIONI:",
                        "- Usa tasti A-Z per inserire lettere",
                        "- BACKSPACE cancella",
                        "- INVIO conferma",
                        "- ESC per tornare"
                    ]
                    
                    y_pos = 670
                    for testo in istruzioni:
                        colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                        testo_render = Fontpiccolo.render(testo, True, colore)
                        screen.blit(testo_render, (150, y_pos))
                        y_pos += 30
                
                elif gioco_finito:
                    #------------------------------------
                    # SCHERMATA FINE GIOCO LETTERE
                    #------------------------------------
                    
                    screen.fill((255, 250, 200))
                    
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
                        x = x_inizio_caselle + i * 130
                        y = 360
                        
                        pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                        pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                        
                        lettera_text = Normalfont.render(codice_segreto[i].upper(), True, (0, 0, 0))
                        lettera_x = x + 40 - lettera_text.get_width() // 2
                        lettera_y = y + 40 - lettera_text.get_height() // 2
                        screen.blit(lettera_text, (lettera_x, lettera_y))
                    
                    continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                    x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                    screen.blit(continua_text, (x_continua, 550))
                    
                    rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                    x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                    screen.blit(rigioca_text, (x_rigioca, 620))
            
            #==================================================
            #COLORI / schermata
            #==================================================
            
            elif dove_siamo == "colori":
                if not in_gioco_colori and not gioco_finito:
                    #--------------------------------
                    # SCHERMATA ISTRUZIONI COLORI
                    #--------------------------------
                    screen.fill((200, 230, 255))
                    
                    titolo_colori = Titlefont.render("MODALITÀ COLORI", True, (0, 0, 150))
                    x_titolo = (larghezza_schermo - titolo_colori.get_width()) // 2
                    screen.blit(titolo_colori, (x_titolo, 50))
                    
                    testi = [
                        "Qui giocherai con i colori!",
                        "Il computer penserà a 4 colori (numeri da 1 a 8)",
                        "Tu dovrai indovinarli in 10 tentativi",
                        "Premi I per iniziare a giocare",
                        "Premi ESC per tornare al menu"
                    ]
                    
                    for i, testo in enumerate(testi):
                        testo_render = Normalfont.render(testo, True, (0, 0, 0))
                        x = (larghezza_schermo - testo_render.get_width()) // 2
                        y = 200 + i * 70
                        screen.blit(testo_render, (x, y))
                
                elif in_gioco_colori:
                    #----------------------------
                    # SCHERMATA DI GIOCO COLORI
                    #----------------------------
                    screen.fill((210, 200, 240))
                    
                    titolo_gioco = Titlefont.render("GIOCO COLORI", True, (75, 0, 130))
                    x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
                    screen.blit(titolo_gioco, (x_titolo, 30))
                    
                    # ==============================================
                    # AREA GIOCO PRINCIPALE COLORI
                    # ==============================================
                    tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                    screen.blit(tentativi_text, (150, 160))
                    
                    input_label = Normalfont.render("Inserisci 4 numeri (1-8):", True, (0, 0, 0))
                    screen.blit(input_label, (150, 230))
                    
                    # 4 caselle per il tentativo corrente
                    for i in range(4):
                        x = 150 + i * 120
                        y = 300
                        
                        # Colora la casella in base al numero inserito
                        colore_casella = (255, 255, 255)
                        if i < len(tentativo_corrente) and tentativo_corrente[i].isdigit():
                            indice = int(tentativo_corrente[i]) - 1
                            if 0 <= indice < len(colori_disponibili):
                                colore_casella = colori_disponibili[indice]
                        
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
                    # LEGENDA COLORI
                    # ==============================================
                    legenda_colori = 450 
                    legenda_label = Normalfont.render("LEGENDA COLORI:", True, (0, 0, 150))
                    screen.blit(legenda_label, (150, legenda_colori))
                    
                    # Mostra i colori su 2 righe da 4
                    for i in range(8):
                        riga = i // 4
                        colonna = i % 4
                        x = 170 + colonna * 130
                        y = legenda_colori + 85 + riga * 45
                        
                        # Cerchio colorato
                        pygame.draw.circle(screen, colori_disponibili[i], (x, y), 15)
                        pygame.draw.circle(screen, (0, 0, 0), (x, y), 15, 1)
                        
                        # Numero accanto
                        num_leg = Fontpiccolo.render(str(i+1), True, (0, 0, 0))
                        screen.blit(num_leg, (x + 20, y - 8))
                    
                    # ==============================================
                    # SUGGERIMENTI
                    # ==============================================
                    if feedback_dettagliato[0] or storico_tentativi:
                        suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                        screen.blit(suggerimenti_label, (700, 160))
                        
                        y_pos = 210
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
                                if pos < len(ultimo) and pos < len(codice_segreto):
                                    if int(ultimo[pos]) != codice_segreto[pos] and int(ultimo[pos]) in codice_segreto:
                                        if ultimo[pos] not in numeri_presenti:
                                            numeri_presenti.append(ultimo[pos])
                            
                            if numeri_presenti:
                                presenti_text = f"Presenti: {', '.join(numeri_presenti)}"
                                presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                                screen.blit(presenti_render, (720, y_pos))
                                y_pos += 30
                    
                    # ==============================================
                    # TENTATIVI COLORI
                    # ==============================================
                    if storico_tentativi:
                        storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                        screen.blit(storico_label, (700, 400))
                        
                        y_pos = 450
                        for i in range(len(storico_tentativi)):
                            numero = i + 1
                            codice = storico_tentativi[i]
                            
                            num_tent = Fontpiccolo.render(f"{numero})", True, (0, 0, 0))
                            screen.blit(num_tent, (700, y_pos))
                            
                            for j in range(4):
                                if j < len(codice) and codice[j].isdigit():
                                    indice = int(codice[j]) - 1
                                    if 0 <= indice < len(colori_disponibili):
                                        x_cerchio = 750 + j * 35
                                        pygame.draw.circle(screen, colori_disponibili[indice], (x_cerchio, y_pos + 20), 10)
                                        pygame.draw.circle(screen, (0, 0, 0), (x_cerchio, y_pos + 20), 10, 1)
                            
                            y_pos += 35
                    
                    # ==============================================
                    # ISTRUZIONI COLORI
                    # ==============================================
                    istruzioni = [
                        "ISTRUZIONI:",
                        "- Usa tasti 1-8 per scegliere colori",
                        "- BACKSPACE cancella",
                        "- INVIO conferma",
                        "- ESC per tornare"
                    ]
                    
                    y_pos = 680
                    for testo in istruzioni:
                        colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                        testo_render = Fontpiccolo.render(testo, True, colore)
                        screen.blit(testo_render, (150, y_pos))
                        y_pos += 30
                
                elif gioco_finito:
                    # SCHERMATA FINE GIOCO COLORI
                    screen.fill((200, 230, 255))
                    
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
                    
                    x_inizio = (larghezza_schermo - (4 * 115)) // 2
                    for i in range(4):
                        x = x_inizio + i * 120
                        y = 360
                        
                        if i < len(codice_segreto):
                            indice = codice_segreto[i] - 1
                            colore = colori_disponibili[indice]
                            
                            pygame.draw.circle(screen, colore, (x + 40, y + 40), 35)
                            pygame.draw.circle(screen, (0, 0, 0), (x + 40, y + 40), 35, 3)
                            
                            num_text = Normalfont.render(str(codice_segreto[i]), True, (0, 0, 0))
                            num_x = x + 40 - num_text.get_width() // 2
                            num_y = y + 40 - num_text.get_height() // 2
                            screen.blit(num_text, (num_x, num_y))
                    
                    continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                    x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                    screen.blit(continua_text, (x_continua, 580))
                    
                    rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                    x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                    screen.blit(rigioca_text, (x_rigioca, 650))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
