# CodiceSegreto - codice principale.
# 
# License: See LICENSE file in the project root for details.
# 
# Authors: 
# Giorgia Silvi giorgiasilvi4@gmail.com
# Giulia Piergiovanni giuliapiergiovanni2009@gmail.com


#import libreria standard
import math    # Libreria per operazioni matematiche (usata per la stella)
import random  # Libreria per generare numeri casuali
import json    # Libreria per salvare/esportare dati sotto forma di testo
import os      # Libreria per interagire con il file della lista dei dati dei giocatori

#import librerie pip
import pygame  # Libreria per creare giochi 2D
from platformdirs import PlatformDirs

# ==============================================
# FUNZIONI DI SALVATAGGIO
# ==============================================
# Nome del file dove salviamo i dati dei giocatori
dirs = PlatformDirs("codicesegreto", ensure_exists=True)
FILE_GIOCATORI = dirs.user_data_dir + "/giocatori.json"


def carica_giocatori():
    """Carica i dati dei giocatori dal file JSON e aggiorna i vecchi profili"""
    # controlla se il file esiste già nella cartella
    if os.path.exists(FILE_GIOCATORI):
        # Apre il file in lettura con codifica UTF-8 per caratteri speciali
        with open(FILE_GIOCATORI, "r", encoding="utf-8") as f:
            # converte il testo del file in un dizionario Python
            giocatori = json.load(f)
        
        # Ripete su tutti i giocatori nel dizionario
        # .items() restituisce coppie (chiave, valore) per ogni giocatore
        for nome_utente, dati in giocatori.items():
            # Se il giocatore non ha il campo 'stelle' (vecchi profili)
            if 'stelle' not in dati:
                dati['stelle'] = 0  # Aggiunge stelle con valore 0
            if 'nome_completo' not in dati:
                dati['nome_completo'] = "Sconosciuto"
        
        return giocatori  # Restituisce il dizionario con tutti i giocatori
    return {}  # Se il file non esiste, restituisce un dizionario vuoto

def salva_giocatori(giocatori):
    """Salva i dati dei giocatori nel file JSON"""
    # Apre il file in scrittura e se non esiste lo crea
    with open(FILE_GIOCATORI, "w", encoding="utf-8") as f:
        # json.dump converte il dizionario in testo e lo salva nel file
        # indent=4 rende il file leggibile con indentazione
        # ensure_ascii=False permette caratteri accentati
        json.dump(giocatori, f, indent=4, ensure_ascii=False)

def crea_nuovo_giocatore(nome_utente, nome_completo):
    """Crea un nuovo profilo giocatore con i dati anagrafici"""
    return {
        "nome_utente": nome_utente,      # Il nickname per giocare
        "nome_completo": nome_completo,  # Nome e cognome reali
        "stelle": 0                      # Stelle accumulate (inizia da 0)
    }

# ==============================================
# FUNZIONE PER DISEGNARE LA STELLA
# ==============================================
def disegna_stella(screen, colore, centro_x, centro_y, dimensione):
    """
    Disegna una stella a 5 punte centrata in (centro_x, centro_y)
    screen: lo schermo dove disegnare
    colore: colore RGB della stella (es. (255,215,0) per oro)
    centro_x, centro_y: coordinate del centro della stella
    dimensione: grandezza della stella (più alto = più grande)
    """
    # Punti base di una stella (coordinate relative al centro)
    # Ogni tupla (x, y) è un punto della stella
    punti_base = [
        (0, -50), (15, -15), (50, -15), (20, 10),
        (30, 50), (0, 25), (-30, 50), (-20, 10),
        (-50, -15), (-15, -15)
    ]
    
    # Lista vuota per i punti trasformati
    punti = []
    # Per ogni punto della stella base
    for x, y in punti_base:
        # Calcola la nuova posizione: centro + (punto_base * dimensione/50)
        # dimensione/50 è il fattore di scala
        punti.append((
            centro_x + x * dimensione / 50,
            centro_y + y * dimensione / 50
        ))
    
    # pygame.draw.polygon disegna un poligono usando i punti calcolati
    pygame.draw.polygon(screen, colore, punti)

def main() -> None:
    print("Hello from codicesegreto!")

    # ==============================================
    # INIZIALIZZAZIONE PYGAME
    # ==============================================
    pygame.init()  # Avvia tutti i moduli di pygame
    
    # Crea la finestra di gioco con dimensioni 1200x900 pixel
    screen = pygame.display.set_mode((1200, 900))
    # Imposta il titolo della finestra
    pygame.display.set_caption("CodiceSegreto")
    
    # ==============================================
    # CARICAMENTO STILI DEL TESTO
    # ==============================================
    # pygame.font.SysFont carica un font di sistema
    # Parametri: (nome_font, dimensione)
    Titlefont = pygame.font.SysFont('Arial', 100)  # Font grande per titoli
    Normalfont = pygame.font.SysFont('Arial', 50)   # Font medio per testi normali
    Fontpiccolo = pygame.font.SysFont('Arial', 30)  # Font piccolo per istruzioni
    
    # Dimensioni dello schermo (costanti)
    larghezza_schermo = 1200
    altezza_schermo = 900
    
    # ==============================================
    # VARIABILI DI STATO DEL GIOCO
    # ==============================================
    stato = "login"  # Stato attuale: "login" (registrazione), "menu", "gioco"
    dove_siamo = "menu"  # Dove ci troviamo nel gioco
    running = True  # Variabile per il loop principale (True = gioco in esecuzione)
    
    # ==============================================
    # VARIABILI PER IL GIOCATORE
    # ==============================================
    giocatori = carica_giocatori()  # Carica tutti i giocatori dal file
    giocatore_corrente = None  # Dati del giocatore attualmente loggato
    
    # Campi del modulo di registrazione
    campo_corrente = 0  # 0 = nome completo, 1  = nome utente
    nome_completo = ""   # Memorizza il nome e cognome inseriti
    nome_utente = ""     # Memorizza il nome utente scelto
    
    # Testo inserito nel campo corrente (quello che l'utente sta scrivendo)
    input_testo = ""
    
    # Messaggio di errore (es. "Nome utente già esistente")
    messaggio_errore = ""
    
    # ==============================================
    # VARIABILI PER IL GIOCO (condivise tra le modalità)
    # ==============================================
    in_gioco_numeri = False   # True se stiamo giocando a Numeri
    in_gioco_lettere = False  # True se stiamo giocando a Lettere
    in_gioco_colori = False   # True se stiamo giocando a Colori
    codice_segreto = ""        # Il codice da indovinare (varia in base alla modalità)
    tentativo_corrente = ""    # Il tentativo che il giocatore sta inserendo
    tentativi_fatti = 0        # Numero di tentativi fatti finora (max 10)
    feedback_dettagliato = ["", "", "", ""]  # Feedback per ogni posizione (4 posizioni)
    storico_tentativi = []      # Lista di tutti i tentativi fatti (in ordine)
    gioco_finito = False        # True se la partita è finita (vittoria o sconfitta)
    risultato = ""              # "VITTORIA" o "SCONFITTA"
    
    # ==============================================
    # LISTA COLORI DISPONIBILI per la modalità colori
    # ==============================================
    # Ogni colore è una tupla RGB (Rosso, Verde, Blu) con valori 0-255
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
    
    # Dizionario che associa un numero al nome del colore corrispondente
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
    
    # ==============================================
    # LOOP PRINCIPALE DEL GIOCO
    # ==============================================
    # Questo loop continua finché running == True
    while running:
        # ==============================================
        # GESTIONE DEGLI EVENTI (tastiera, mouse, ecc.)
        # ==============================================
        # pygame.event.get() restituisce tutti gli eventi accaduti
        for event in pygame.event.get():
            # Se l'utente clicca sulla X per chiudere la finestra
            if event.type == pygame.QUIT:
                # Salva i dati del giocatore prima di uscire
                if giocatore_corrente:
                    giocatori[nome_utente] = giocatore_corrente
                    salva_giocatori(giocatori)
                running = False  # Esce dal loop principale
            
            # Se viene premuto un tasto sulla tastiera
            elif event.type == pygame.KEYDOWN:
                # ==============================================
                # STATO LOGIN - MODULO REGISTRAZIONE
                # ==============================================
                if stato == "login":
                    
                    # Tasto INVIO per passare al campo successivo o confermare
                    if event.key == pygame.K_RETURN:
                        
                        # Se siamo al campo 0 (nome completo)
                        if campo_corrente == 0:
                            if input_testo:
                                nome_completo = input_testo
                                campo_corrente = 1
                                input_testo = nome_utente
                                messaggio_errore = ""
                            else:
                                messaggio_errore = "Inserisci nome e cognome"
                        
                        
                        # Se siamo al campo 1 (nome utente) - CONFERMA FINALE
                        elif campo_corrente == 1:
                            if input_testo:
                                nome_utente = input_testo
                                
                                # Controlla che tutti i campi siano compilati
                                if nome_completo and nome_utente:
                                    
                                    # ===== PARTE CORRETTA PER IL CARICAMENTO =====
                                    # Verifica se il nome utente ESISTE GIA'
                                    if nome_utente in giocatori:
                                        # GIOCATORE ESISTENTE - carica i suoi dati
                                        giocatore_corrente = giocatori[nome_utente]
                                        
                                        # Verifica che i dati anagrafici corrispondano (sicurezza)
                                        if (giocatore_corrente['nome_completo'] == nome_completo):
                                            
                                            print(f"Bentornato {nome_utente}! Hai {giocatore_corrente['stelle']}")
                                            
                                            # Vai al menu
                                            stato = "menu"
                                            dove_siamo = "menu"
                                            # Reset variabili login
                                            campo_corrente = 0
                                            nome_completo = ""
                                            nome_utente = ""
                                            input_testo = ""
                                            messaggio_errore = ""
                                            
                                        else:
                                            # I dati anagrafici non corrispondono
                                            messaggio_errore = "Nome utente già esistente con altri dati!"
                                    
                                    else:
                                        # NUOVO GIOCATORE - crea nuovo profilo
                                        giocatore_corrente = crea_nuovo_giocatore(
                                            nome_utente, 
                                            nome_completo
                                        )
                                        giocatori[nome_utente] = giocatore_corrente
                                        salva_giocatori(giocatori)
                                        print(f"Benvenuto {nome_utente}!")
                                        
                                        # Vai al menu
                                        stato = "menu"
                                        dove_siamo = "menu"
                                        # Reset variabili login
                                        campo_corrente = 0
                                        nome_completo = ""
                                        anno_nascita = ""
                                        nome_utente = ""
                                        input_testo = ""
                                        messaggio_errore = ""
                                        
                                else:
                                    messaggio_errore = "Compila tutti i campi!"
                            else:
                                messaggio_errore = "Scegli un nome utente"
                        
                        continue
                    
                    # Tasto BACKSPACE per cancellare l'ultimo carattere
                    elif event.key == pygame.K_BACKSPACE:
                        input_testo = input_testo[:-1]  # Toglie l'ultimo carattere
                        # Aggiorna anche la variabile del campo corrente
                        if campo_corrente == 0:
                            nome_completo = input_testo
                        
                        elif campo_corrente == 1:
                            nome_utente = input_testo
                    
                    # Altri tasti stampabili (lettere, numeri, ecc.)
                    elif event.key <= 127 and event.unicode.isprintable():
                        # Limiti di lunghezza per ogni campo
                        if campo_corrente == 0 and len(input_testo) < 30:
                            input_testo += event.unicode  # Aggiunge il carattere
                            nome_completo = input_testo
                        
                        elif campo_corrente == 1 and len(input_testo) < 10:
                            input_testo += event.unicode
                            nome_utente = input_testo

                # ==============================================
                # STATO MENU
                # ==============================================
                elif stato == "menu":
                    # Tasto N per andare alla modalità Numeri
                    if event.key == pygame.K_n and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "numeri"
                        stato = "gioco"
                        # Resetta le variabili di gioco per iniziare una nuova partita
                        in_gioco_numeri = False
                        in_gioco_lettere = False
                        in_gioco_colori = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        gioco_finito = False
                    
                    # Tasto L per andare alla modalità Lettere
                    elif event.key == pygame.K_l and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "lettere"
                        stato = "gioco"
                        # Resetta le variabili
                        in_gioco_numeri = False
                        in_gioco_lettere = False
                        in_gioco_colori = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        gioco_finito = False
                    
                    # Tasto C per andare alla modalità Colori
                    elif event.key == pygame.K_c and not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        dove_siamo = "colori"
                        stato = "gioco"
                        # Resetta le variabili
                        in_gioco_numeri = False
                        in_gioco_lettere = False
                        in_gioco_colori = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        gioco_finito = False
 
                    # Tasto ESC per tornare alla schermata di login
                    elif event.key == pygame.K_ESCAPE:
                        stato = "login"
                        campo_corrente = 0
                        nome_completo = ""
                        nome_utente = ""
                        input_testo = ""
                        messaggio_errore = ""
                        continue
                
                # ==============================================
                # STATO GIOCO
                # ==============================================
                elif stato == "gioco":
                    
                    # Tasti per cambiare modalità (solo se non in partita)
                    if not in_gioco_numeri and not in_gioco_lettere and not in_gioco_colori and not gioco_finito:
                        if event.key == pygame.K_n:
                            dove_siamo = "numeri"
                            print("=== MODALITÀ NUMERI ===")
                            continue
                        elif event.key == pygame.K_l:
                            dove_siamo = "lettere"
                            print("=== MODALITÀ LETTERE ===")
                            continue
                        elif event.key == pygame.K_c:
                            dove_siamo = "colori"
                            print("=== MODALITÀ COLORI ===")
                            continue
                    
                    # Tasto I per iniziare una partita a NUMERI
                    if event.key == pygame.K_i and dove_siamo == "numeri" and not in_gioco_numeri:
                        in_gioco_numeri = True  # Entra in modalità gioco
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""

                        # Genera codice segreto per i numeri (4 cifre da 1 a 6)
                        codice_segreto = ""
                        for _ in range(4):
                            cifra = random.randint(1, 6)
                            codice_segreto += str(cifra)  # Converte in stringa e concatena
                        continue
                    
                    # Tasto I per iniziare una partita a LETTERE
                    elif event.key == pygame.K_i and dove_siamo == "lettere" and not in_gioco_lettere:
                        in_gioco_lettere = True
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""

                        # Genera codice segreto per le lettere (4 lettere a-z)
                        codice_segreto = ""
                        for _ in range(4):
                            # chr(random.randint(97,122)) converte numero in lettera
                            # 97 = 'a', 122 = 'z'
                            lettera = chr(random.randint(97, 122))
                            codice_segreto += lettera
                        continue
                    
                    # Tasto I per iniziare una partita a COLORI
                    elif event.key == pygame.K_i and dove_siamo == "colori" and not in_gioco_colori:
                        in_gioco_colori = True
                        gioco_finito = False
                        tentativi_fatti = 0
                        tentativo_corrente = ""
                        feedback_dettagliato = ["", "", "", ""]
                        storico_tentativi = []
                        risultato = ""

                        # Genera codice segreto per i colori (lista di 4 numeri 1-8)
                        codice_segreto = []
                        for _ in range(4):
                            colore = random.randint(1, 8)
                            codice_segreto.append(colore)  # Aggiunge alla lista
                        continue
                    
                    # Tasto ESC per tornare al menu
                    elif event.key == pygame.K_ESCAPE:
                        if in_gioco_numeri or in_gioco_lettere or in_gioco_colori or gioco_finito:
                            # Se si sta giocando, resetta tutto
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
                        # Tasto I per rigiocare nella stessa modalità
                        if event.key == pygame.K_i:
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
                                
                                continue
                        
                        # Tasto ESC per tornare alle istruzioni
                        elif event.key == pygame.K_ESCAPE:
                            if dove_siamo == "numeri":
                                in_gioco_numeri = False
                            elif dove_siamo == "lettere":
                                in_gioco_lettere = False
                            elif dove_siamo == "colori":
                                in_gioco_colori = False
                            gioco_finito = False
                            stato = "menu"
                            dove_siamo = "menu"
                            continue
                    
                    # ==============================================
                    # GESTIONE INPUT NUMERI
                    # ==============================================
                    if in_gioco_numeri and not gioco_finito:
                        # Tasti numerici 1-6 per inserire il codice
                        if pygame.K_1 <= event.key <= pygame.K_6:
                            if len(tentativo_corrente) < 4:  # Massimo 4 cifre
                                numero = chr(event.key)  # Converte il tasto in carattere ('1', '2', ecc.)
                                tentativo_corrente += numero  # Aggiunge alla stringa

                        # BACKSPACE cancella l'ultimo carattere
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]
                        
                        # INVIO conferma il tentativo (solo se sono 4 cifre)
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1  # Aumenta il contatore tentativi
                            
                            # Salva il tentativo nello storico
                            storico_tentativi.append(tentativo_corrente)
                            
                            # Calcola il feedback per ogni posizione
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if tentativo_corrente[pos] == codice_segreto[pos]:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                                else:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"

                            # Controlla quali numeri sono presenti ma in posizione sbagliata
                            numeri_presenti = []
                            for pos in range(4):
                                if (tentativo_corrente[pos] != codice_segreto[pos] and 
                                    tentativo_corrente[pos] in codice_segreto):
                                    # Evita di aggiungere duplicati
                                    if tentativo_corrente[pos] not in numeri_presenti:
                                        numeri_presenti.append(tentativo_corrente[pos])
                            
                            print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                            
                            # Controlla se ha vinto (tentativo uguale al codice)
                            if tentativo_corrente == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_numeri = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                                
                                # Aggiunge una stella al giocatore
                                if giocatore_corrente:
                                    giocatore_corrente["stelle"] += 1
                                    giocatori[nome_utente] = giocatore_corrente
                                    salva_giocatori(giocatori)  # Salva immediatamente
                                    print(f"Ora hai {giocatore_corrente['stelle']} stelle!")
                                
                            # Controlla se ha perso (10 tentativi)
                            elif tentativi_fatti >= 10:
                                risultato = "SCONFITTA"
                                gioco_finito = True
                                in_gioco_numeri = False
                                print(f"HAI PERSO! Il codice era: {codice_segreto}")
                            else:
                                tentativo_corrente = ""  # Resetta per il prossimo tentativo
                    
                    # ==============================================
                    # GESTIONE INPUT LETTERE
                    # ==============================================
                    if in_gioco_lettere and not gioco_finito:
                        # Tasti lettera A-Z per inserire il codice
                        if pygame.K_a <= event.key <= pygame.K_z:
                            if len(tentativo_corrente) < 4:
                                lettera = chr(event.key)  # Converte il tasto in lettera
                                tentativo_corrente += lettera

                        # BACKSPACE cancella l'ultimo carattere
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]

                        # INVIO conferma il tentativo
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1
                            
                            storico_tentativi.append(tentativo_corrente)
                            
                            # Calcola feedback
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if tentativo_corrente[pos] == codice_segreto[pos]:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} CORRETTO"
                                else:
                                    feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} SBAGLIATO"
                            
                            # Controlla lettere presenti ma in posizione sbagliata
                            lettere_presenti = []
                            for pos in range(4):
                                if (tentativo_corrente[pos] != codice_segreto[pos] and 
                                    tentativo_corrente[pos] in codice_segreto):
                                    if tentativo_corrente[pos] not in lettere_presenti:
                                        lettere_presenti.append(tentativo_corrente[pos])
                            
                            print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                            
                            # Controlla vittoria
                            if tentativo_corrente == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_lettere = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                                
                                # Aggiunge una stella
                                if giocatore_corrente:
                                    giocatore_corrente["stelle"] += 1
                                    giocatori[nome_utente] = giocatore_corrente
                                    salva_giocatori(giocatori)
                                    print(f"Ora hai {giocatore_corrente['stelle']} stelle!")
                                
                            # Controlla sconfitta
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
                        # Tasti numerici 1-8 per scegliere i colori
                        if pygame.K_1 <= event.key <= pygame.K_8:
                            if len(tentativo_corrente) < 4:
                                numero = chr(event.key)
                                tentativo_corrente += numero
                        
                        # BACKSPACE cancella l'ultimo numero
                        elif event.key == pygame.K_BACKSPACE:
                            tentativo_corrente = tentativo_corrente[:-1]
                        
                        # INVIO conferma il tentativo
                        elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 4:
                            tentativi_fatti += 1
                            
                            storico_tentativi.append(tentativo_corrente)
                            
                            # Calcola feedback
                            feedback_dettagliato = ["", "", "", ""]
                            
                            for pos in range(4):
                                if pos < len(tentativo_corrente) and pos < len(codice_segreto):
                                    if int(tentativo_corrente[pos]) == codice_segreto[pos]:
                                        feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} {nomi_colori[int(tentativo_corrente[pos])]} CORRETTO"
                                    else:
                                        feedback_dettagliato[pos] = f"Posizione {pos+1}: {tentativo_corrente[pos]} {nomi_colori[int(tentativo_corrente[pos])]} SBAGLIATO"
                            
                            # Controlla vittoria (confronta liste di interi)
                            tentativo_lista = [int(x) for x in tentativo_corrente]
                            
                            print(f"Tentativo {tentativi_fatti}: {tentativo_corrente}")
                            
                            if tentativo_lista == codice_segreto:
                                risultato = "VITTORIA"
                                gioco_finito = True
                                in_gioco_colori = False
                                print(f"HAI VINTO in {tentativi_fatti} tentativi!")
                                
                                # Aggiunge una stella
                                if giocatore_corrente:
                                    giocatore_corrente["stelle"] += 1
                                    giocatori[nome_utente] = giocatore_corrente
                                    salva_giocatori(giocatori)
                                    print(f"Ora hai {giocatore_corrente['stelle']} stelle!")
                                
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
            # screen.fill riempie lo schermo con un colore RGB
            screen.fill((200, 220, 240))  # Azzurrino
            
            # Titolo principale
            # render crea un'immagine del testo con colore e anti-aliasing (tecnica per linee curve)
            titolo = Titlefont.render("CODICE SEGRETO", True, (0, 0, 150))
            # Calcola la posizione X per centrare il testo
            x_titolo = (larghezza_schermo - titolo.get_width()) // 2
            screen.blit(titolo, (x_titolo, 50))  # Disegna il testo a (x, y=50)
            
            # Sottotitolo
            sottotitolo = Normalfont.render("Registrazione Nuovo Giocatore", True, (0, 0, 0))
            x_sotto = (larghezza_schermo - sottotitolo.get_width()) // 2
            screen.blit(sottotitolo, (x_sotto, 150))
            
            # ==============================================
            # CAMPO 1: NOME E COGNOME
            # ==============================================
            label1 = Normalfont.render("Nome e Cognome:", True, (0, 0, 0))
            screen.blit(label1, (300, 245))
            
            # Riquadro per il campo 1 (Rect: x, y, larghezza, altezza)
            rect1 = pygame.Rect(300, 300, 600, 60)
            # Bordo blu se è il campo corrente, altrimenti grigio
            colore_bordo1 = (0, 100, 200) if campo_corrente == 0 else (100, 100, 100)
            # Disegna il rettangolo bianco di sfondo
            pygame.draw.rect(screen, (255, 255, 255), rect1, border_radius=8)
            # Disegna il bordo
            pygame.draw.rect(screen, colore_bordo1, rect1, 3, border_radius=8)
            
            # Testo inserito nel campo
            testo1 = Fontpiccolo.render(nome_completo, True, (0, 0, 0))
            screen.blit(testo1, (310, 315))
            
            # Cursore lampeggiante (appare e scompare ogni 500ms)
            # pygame.time.get_ticks() restituisce millisecondi dall'avvio
            if campo_corrente == 0 and pygame.time.get_ticks() % 1000 < 500:
                cursore_x = 310 + testo1.get_width()
                pygame.draw.line(screen, (0, 0, 0), (cursore_x, 315), (cursore_x, 345), 2)
            
            # ==============================================
            # CAMPO 2: NOME UTENTE
            # ==============================================
            label2 = Normalfont.render("Nome Utente (unico):", True, (0, 0, 0))
            screen.blit(label2, (300, 380))
            # Riquadro per il campo 3 (Rect: x, y, larghezza, altezza)
            rect2 = pygame.Rect(300, 430, 600, 60)
            # Bordo blu se è il campo corrente, altrimenti grigio
            colore_bordo2 = (0, 100, 200) if campo_corrente == 1 else (100, 100, 100)
            # Disegna il rettangolo bianco di sfondo
            pygame.draw.rect(screen, (255, 255, 255), rect2, border_radius=8)
            # Disegna il bordo
            pygame.draw.rect(screen, colore_bordo2, rect2, 3, border_radius=8)
            
            # Testo inserito nel campo
            testo2 = Fontpiccolo.render(nome_utente, True, (0, 0, 0))
            screen.blit(testo2, (310, 445))
            
            # Cursore lampeggiante (appare e scompare ogni 500ms)
            # pygame.time.get_ticks() restituisce millisecondi dall'avvio
            if campo_corrente == 2 and pygame.time.get_ticks() % 1000 < 500:
                cursore_x = 310 + testo3.get_width()
                pygame.draw.line(screen, (0, 0, 0), (cursore_x, 380), (cursore_x, 445), 2)
            
            # ==============================================
            # MESSAGGI E ISTRUZIONI
            # ==============================================
            
            # Mostra messaggio di errore se presente
            if messaggio_errore:
                errore_render = Fontpiccolo.render(messaggio_errore, True, (200, 0, 0))
                x_errore = (larghezza_schermo - errore_render.get_width()) // 2
                screen.blit(errore_render, (x_errore, 640))
            
            # Indicazione più specifica
            messaggio = Fontpiccolo.render("premere INVIO per passare al secondo campo di inserimento", True, (100, 100, 100))
            x_messaggio = (larghezza_schermo - messaggio.get_width()) //2
            screen.blit(messaggio, (x_messaggio, 575))
            
        # ==============================================
        # SCHERMATA MENU
        # ==============================================
        elif stato == "menu":
            screen.fill((255, 182, 193))  # Rosa chiaro
            
            # Info giocatore in alto a destra (tutte allineate)
            if giocatore_corrente:
                # Nome utente
                nome_text = Fontpiccolo.render(f"Utente: {giocatore_corrente['nome_utente']}", True, (0, 0, 0))
                screen.blit(nome_text, (850, 40))
                
                # Stella con numero (allineata sotto le scritte)
                stelle_totali = giocatore_corrente['stelle']
                disegna_stella(screen, (255, 215, 0), 865, 120, 20)
                testo_stelle = Fontpiccolo.render(str(stelle_totali), True, (255, 220, 0))
                screen.blit(testo_stelle, (890, 110))
            
            # Titolo del gioco centrato
            Titolo = Titlefont.render("CodiceSegreto", True, (0, 0, 0))
            x_titolo = (larghezza_schermo - Titolo.get_width()) // 2
            screen.blit(Titolo, (x_titolo, 180))
            
            # Opzioni di gioco (centrate verticalmente)
            opzioni = ["Numeri (N)", "Colori (C)", "Lettere (L)"]
            for i, testo in enumerate(opzioni):
                testo_render = Normalfont.render(testo, True, (0, 0, 0))
                x = (larghezza_schermo - testo_render.get_width()) // 2
                y = 350 + i * 100  # Distanza 100 pixel tra le opzioni
                screen.blit(testo_render, (x, y))

                # Aggiungi indicazione del tasto in grigio sotto ogni opzione
                if i == 0:  # Numeri
                    tasto_indicazione = Fontpiccolo.render("premi N", True, (100, 100, 100))
                elif i == 1:  # Colori
                    tasto_indicazione = Fontpiccolo.render("premi C", True, (100, 100, 100))
                else:  # Lettere
                    tasto_indicazione = Fontpiccolo.render("premi L", True, (100, 100, 100))
                
                x_tasto = (larghezza_schermo - tasto_indicazione.get_width()) // 2
                y_tasto = y + 45  # Metti l'indicazione sotto l'opzione
                screen.blit(tasto_indicazione, (x_tasto, y_tasto))
                
            
            # Istruzione per cambiare utente
            cambio = Fontpiccolo.render("Premi ESC per cambiare utente", True, (100, 100, 100))
            x_cambio = (larghezza_schermo - cambio.get_width()) // 2
            screen.blit(cambio, (x_cambio, 750))
            
            # Indicazione per il giocatore
            indicazione = Fontpiccolo.render("Premi la lettera associata tra parentesi per scegliere la modalità di gioco", True, (100, 100, 100))
            screen.blit(indicazione, (x_cambio, 900))
        
        # ==============================================
        # STATO GIOCO - NUMERI
        # ==============================================
        # Questo blocco viene eseguito solo quando siamo nello stato "gioco" 
        # e abbiamo scelto la modalità "numeri"
        elif stato == "gioco" and dove_siamo == "numeri":
            
            # ==============================================
            # SCHERMATA ISTRUZIONI (prima di iniziare la partita)
            # ==============================================
            # Questa parte viene eseguita quando NON siamo in gioco (in_gioco_numeri = False)
            # e la partita NON è finita (gioco_finito = False)
            if not in_gioco_numeri and not gioco_finito:
                # Imposta il colore di sfondo (Lavanda chiaro - RGB)
                screen.fill((230, 220, 250))
                
                # Crea il titolo "MODALITÀ NUMERI" con font grande e colore viola scuro
                titolo_numeri = Titlefont.render("MODALITÀ NUMERI", True, (75, 0, 130))
                # Calcola la posizione X per centrare il titolo orizzontalmente
                # (larghezza_schermo - larghezza_del_testo) // 2
                x_titolo = (larghezza_schermo - titolo_numeri.get_width()) // 2
                # Disegna il titolo alla posizione calcolata (x centrata, y=50)
                screen.blit(titolo_numeri, (x_titolo, 50))
                
                # Lista delle istruzioni da mostrare
                testi = [
                    "Qui giocherai con i numeri!",
                    "Il computer penserà a 4 numeri (da 1 a 6)",
                    "Tu dovrai indovinarli in 10 tentativi",
                    "Attenzione! i numeri possono essere ripetuti!",
                    "Premi I per iniziare a giocare",
                    "Premi ESC per tornare al menu"
                ]
                
                # Mostra le istruzioni una sotto l'altra
                # enumerate restituisce sia l'indice (i) che il testo
                for i, testo in enumerate(testi):
                    # Crea l'immagine del testo con font medio e colore nero
                    testo_render = Normalfont.render(testo, True, (0, 0, 0))
                    # Centra orizzontalmente
                    x = (larghezza_schermo - testo_render.get_width()) // 2
                    # Posizione verticale: parte da 200 e aumenta di 70 pixel per ogni riga
                    y = 200 + i * 70
                    # Disegna il testo
                    screen.blit(testo_render, (x, y))
            
            # ==============================================
            # SCHERMATA DI GIOCO (durante la partita)
            # ==============================================
            # Questa parte viene eseguita quando siamo IN GIOCO (in_gioco_numeri = True)
            elif in_gioco_numeri:
                # Imposta lo sfondo (Lavanda medio)
                screen.fill((210, 200, 240))
                
                # Titolo "GIOCO NUMERI" in alto centrato
                titolo_gioco = Titlefont.render("GIOCO NUMERI", True, (75, 0, 130))
                x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
                screen.blit(titolo_gioco, (x_titolo, 30))
                
                # ==============================================
                # INFO GIOCATORE (in alto a destra)
                # ==============================================
                # Mostra i dati del giocatore corrente se esiste
                if giocatore_corrente:
                    # Nome utente (nickname) a (1000, 40)
                    nome_text = Fontpiccolo.render(f"Utente: {giocatore_corrente['nome_utente']}", True, (0, 0, 0))
                    screen.blit(nome_text, (1000, 40))
                    
                    # Stella con numero di vittorie
                    stelle_totali = giocatore_corrente['stelle']
                    # Disegna una stella dorata centrata a (1024, 110) di dimensione 20
                    disegna_stella(screen, (255, 215, 0), 1024, 110, 20)
                    # Mostra il numero di stelle accanto alla stella
                    testo_stelle = Fontpiccolo.render(str(stelle_totali), True, (255, 215, 0))
                    screen.blit(testo_stelle, (1060, 100))
                
                # ==============================================
                # AREA DI GIOCO PRINCIPALE
                # ==============================================
                
                # Mostra il numero del tentativo corrente (es. "Tentativo: 3/10")
                tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                screen.blit(tentativi_text, (150, 160))
                
                # Istruzione per l'input (cosa deve inserire il giocatore)
                input_label = Normalfont.render("Inserisci 4 numeri (1-6):", True, (0, 0, 0))
                screen.blit(input_label, (150, 230))
                
                # ==============================================
                # DISEGNA LE 4 CASELLE PER INSERIRE I NUMERI
                # ==============================================
                # Crea 4 caselle in orizzontale
                for i in range(4):
                    # Calcola la posizione X: parte da 150 e aumenta di 120 pixel per ogni casella
                    x = 150 + i * 120
                    y = 300  # Tutte le caselle alla stessa altezza
                    
                    # Colore della casella: azzurro se la posizione è piena, bianco se vuota
                    # len(tentativo_corrente) indica quante cifre ha inserito finora
                    colore_casella = (180, 220, 255) if i < len(tentativo_corrente) else (255, 255, 255)
                    
                    # Disegna il rettangolo della casella (80x80 pixel) con angoli arrotondati
                    pygame.draw.rect(screen, colore_casella, (x, y, 80, 80), border_radius=10)
                    # Disegna il bordo blu spesso 3 pixel
                    pygame.draw.rect(screen, (0, 100, 200), (x, y, 80, 80), 3, border_radius=10)
                    
                    # Se c'è un numero in questa posizione, lo mostra
                    if i < len(tentativo_corrente):
                        # Crea l'immagine del numero (es. '3')
                        num_text = Normalfont.render(tentativo_corrente[i], True, (0, 0, 0))
                        # Calcola la posizione per centrare il numero nella casella
                        num_x = x + 40 - num_text.get_width() // 2
                        num_y = y + 40 - num_text.get_height() // 2
                        screen.blit(num_text, (num_x, num_y))
                    else:
                        # Segnaposto per le posizioni vuote (scritta "Pos 1", "Pos 2", ecc.)
                        segnaposto = Fontpiccolo.render(f"Pos {i+1}", True, (100, 100, 100))
                        # Centra il segnaposto nella casella
                        segnaposto_x = x + 40 - segnaposto.get_width() // 2
                        segnaposto_y = y + 40 - segnaposto.get_height() // 2
                        screen.blit(segnaposto, (segnaposto_x, segnaposto_y))
                
                # ==============================================
                # SUGGERIMENTI (feedback per l'ultimo tentativo)
                # ==============================================
                # Viene mostrato solo se ci sono feedback o tentativi precedenti
                if feedback_dettagliato[0] or storico_tentativi:
                    # Titolo della sezione "SUGGERIMENTI" in verde
                    suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                    screen.blit(suggerimenti_label, (700, 160))
                    
                    y_pos = 210  # Posizione verticale iniziale per i suggerimenti
                    
                    # Mostra il feedback per ogni posizione (es. "Posizione 1: 3 CORRETTO")
                    if feedback_dettagliato[0]:
                        for i, fb in enumerate(feedback_dettagliato):
                            if fb:  # Se c'è un feedback per questa posizione
                                # Verde per CORRETTO, rosso per SBAGLIATO
                                colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)
                                fb_text = Fontpiccolo.render(fb, True, colore)
                                screen.blit(fb_text, (720, y_pos))
                                y_pos += 30  # Sposta in basso per il prossimo feedback
                    
                    # Mostra i numeri che sono presenti ma in posizione sbagliata
                    if storico_tentativi:
                        # Prende l'ultimo tentativo fatto
                        ultimo = storico_tentativi[-1]
                        numeri_presenti = []
                        # Controlla ogni posizione
                        for pos in range(4):
                            # Se il numero è diverso da quello segreto MA è presente nel codice
                            if (ultimo[pos] != codice_segreto[pos] and 
                                ultimo[pos] in codice_segreto):
                                # Evita di aggiungere duplicati
                                if ultimo[pos] not in numeri_presenti:
                                    numeri_presenti.append(ultimo[pos])
                        
                        # Se ci sono numeri presenti, li mostra
                        if numeri_presenti:
                            presenti_text = f"Presenti: {', '.join(numeri_presenti)}"
                            presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                            screen.blit(presenti_render, (720, y_pos))
                            y_pos += 30
                
                # ==============================================
                # STORICO TENTATIVI
                # ==============================================
                # Mostra tutti i tentativi fatti finora
                if storico_tentativi:
                    storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                    screen.blit(storico_label, (700, 370))
                    
                    y_pos = 420  # Posizione iniziale per i tentativi
                    # Itera su tutti i tentativi nello storico
                    for i, codice in enumerate(storico_tentativi):
                        numero = i + 1  # Numero del tentativo (1, 2, 3, ...)
                        # Formatta come "1) 1234"
                        tent_text = Fontpiccolo.render(f"{numero}) {codice}", True, (0, 0, 0))
                        screen.blit(tent_text, (720, y_pos))
                        y_pos += 30  # Sposta in basso per il prossimo tentativo
                
                # ==============================================
                # CONSIGLIO (dopo 6 tentativi)
                # ==============================================
                # Crea un rettangolo per il consiglio (x=150, y=440, larghezza=380, altezza=180)
                rettangolo_consiglio = pygame.Rect(150, 440, 380, 180)
                # Disegna lo sfondo color crema
                pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)
                # Disegna il bordo grigio
                pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)
    
                # Titolo "CONSIGLIO" centrato nel rettangolo
                consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))
                # Calcola la posizione X per centrare il titolo
                x_titolo_consiglio = rettangolo_consiglio.x + (rettangolo_consiglio.width - consiglio_titolo.get_width()) // 2
                screen.blit(consiglio_titolo, (x_titolo_consiglio, 455))

                # Calcola il consiglio solo dopo 6 tentativi
                if tentativi_fatti >= 6:
                    # Conta quanti numeri pari e dispari ci sono nel codice segreto
                    pari = 0
                    dispari = 0
                    for num in codice_segreto:
                        if int(num) % 2 == 0:  # Se il numero è divisibile per 2
                            pari += 1
                        else:
                            dispari += 1
                    
                    # Sceglie il testo in base alla maggioranza
                    if pari == 4:
                        testo_maggioranza = "Tutti PARI"
                    elif dispari == 4:
                        testo_maggioranza = "Tutti DISPARI"
                    elif pari > dispari:
                        testo_maggioranza = "Maggioranza PARI"
                    else:
                        testo_maggioranza = "Maggioranza DISPARI"
                    
                    # Mostra il testo della maggioranza centrato
                    testo_magg_render = Fontpiccolo.render(testo_maggioranza, True, (0, 100, 200))
                    x_magg = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_magg_render.get_width()) // 2
                    screen.blit(testo_magg_render, (x_magg, 500))
                    
                    # Mostra il conteggio dei numeri pari
                    testo_pari = f"Pari: {pari}"
                    testo_pari_render = Fontpiccolo.render(testo_pari, True, (80, 80, 80))
                    x_pari = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_pari_render.get_width()) // 2
                    screen.blit(testo_pari_render, (x_pari, 540))
                    
                    # Mostra il conteggio dei numeri dispari
                    testo_dispari = f"Dispari: {dispari}"
                    testo_dispari_render = Fontpiccolo.render(testo_dispari, True, (80, 80, 80))
                    x_dispari = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_dispari_render.get_width()) // 2
                    screen.blit(testo_dispari_render, (x_dispari, 570))
                else:
                    # Messaggio di attesa prima del 6° tentativo
                    tentativi_mancanti = 6 - tentativi_fatti
                    
                    # Gestisce il singolare/plurale
                    if tentativi_mancanti == 1:
                        messaggio = f"Disponibile tra 1 tentativo"
                    else:
                        messaggio = f"Disponibile tra {tentativi_mancanti} tentativi"
                    
                    # Mostra il messaggio centrato in grigio
                    testo_attesa = Fontpiccolo.render(messaggio, True, (150, 150, 150))
                    x_attesa = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_attesa.get_width()) // 2
                    screen.blit(testo_attesa, (x_attesa, 520))
                
                # ==============================================
                # ISTRUZIONI (sempre visibili in basso a sinistra)
                # ==============================================
                istruzioni = [
                    "ISTRUZIONI:",
                    "- Usa tasti 1-6 per inserire numeri",
                    "- BACKSPACE cancella",
                    "- INVIO conferma",
                    "- ESC per tornare"
                ]
    
                y_pos = 670  # Posizione verticale iniziale
                for testo in istruzioni:
                    # Grigio per le istruzioni, nero per il titolo "ISTRUZIONI"
                    colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                    testo_render = Fontpiccolo.render(testo, True, colore)
                    screen.blit(testo_render, (150, y_pos))
                    y_pos += 30  # Sposta in basso per la prossima istruzione
            
            # ==============================================
            # SCHERMATA FINE GIOCO (vittoria o sconfitta)
            # ==============================================
            elif gioco_finito:
                # Sfondo lavanda chiaro
                screen.fill((230, 220, 250))
                
                # Titolo in base al risultato (verde per vittoria, rosso per sconfitta)
                if risultato == "VITTORIA":
                    titolo_risultato = Titlefont.render("HAI VINTO!", True, (0, 150, 0))
                else:
                    titolo_risultato = Titlefont.render("HAI PERSO!", True, (200, 0, 0))
                
                # Centra il titolo
                x_titolo = (larghezza_schermo - titolo_risultato.get_width()) // 2
                screen.blit(titolo_risultato, (x_titolo, 80))
                
                # Info sui tentativi effettuati
                info1 = Normalfont.render(f"Hai fatto {tentativi_fatti} tentativi su 10", True, (0, 0, 0))
                x_info1 = (larghezza_schermo - info1.get_width()) // 2
                screen.blit(info1, (x_info1, 200))
                
                # Testo "Il codice corretto era:"
                codice_label = Normalfont.render("Il codice corretto era:", True, (0, 0, 0))
                x_codice_label = (larghezza_schermo - codice_label.get_width()) // 2
                screen.blit(codice_label, (x_codice_label, 280))
                
                # ==============================================
                # CASELLE CON IL CODICE CORRETTO
                # ==============================================
                # Calcola la posizione X per centrare le 4 caselle
                # (4 caselle * 120 pixel di larghezza ciascuna)
                x_inizio_caselle = (larghezza_schermo - (4 * 120)) // 2
                for i in range(4):
                    # Posizione X: parte da x_inizio_caselle e aumenta di 130 pixel per ogni casella
                    x = x_inizio_caselle + i * 130
                    y = 360  # Tutte alla stessa altezza
                    
                    # Caselle verdi per il codice corretto
                    pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                    pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                    
                    # Mostra il numero del codice segreto
                    num_text = Normalfont.render(codice_segreto[i], True, (0, 0, 0))
                    num_x = x + 40 - num_text.get_width() // 2
                    num_y = y + 40 - num_text.get_height() // 2
                    screen.blit(num_text, (num_x, num_y))
                
                # Istruzioni per continuare
                continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                screen.blit(continua_text, (x_continua, 550))
                
                rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                screen.blit(rigioca_text, (x_rigioca, 620))
        
        # ==============================================
        # STATO GIOCO - LETTERE
        # ==============================================
        # Questo blocco viene eseguito solo quando siamo nello stato "gioco" 
        # e abbiamo scelto la modalità "lettere"
        elif stato == "gioco" and dove_siamo == "lettere":
            
            # ==============================================
            # SCHERMATA ISTRUZIONI (prima di iniziare la partita)
            # ==============================================
            # Questa parte viene eseguita quando NON siamo in gioco (in_gioco_lettere = False)
            # e la partita NON è finita (gioco_finito = False)
            if not in_gioco_lettere and not gioco_finito:
                # Imposta il colore di sfondo giallo chiaro (RGB)
                screen.fill((255, 250, 200))
                
                # Crea il titolo "MODALITÀ LETTERE" con font grande e colore arancione scuro
                titolo_lettere = Titlefont.render("MODALITÀ LETTERE", True, (200, 100, 0))
                # Calcola la posizione X per centrare il titolo orizzontalmente
                x_titolo = (larghezza_schermo - titolo_lettere.get_width()) // 2
                # Disegna il titolo alla posizione calcolata (x centrata, y=50)
                screen.blit(titolo_lettere, (x_titolo, 50))
                
                # Lista delle istruzioni da mostrare
                testi = [
                    "Qui giocherai con le lettere!",
                    "Il computer penserà a 4 lettere (dalla a alla z)",
                    "Tu dovrai indovinarle in 10 tentativi",
                     "Attenzione! Le lettere possono essere ripetuti!",
                    "Premi I per iniziare a giocare",
                    "Premi ESC per tornare al menu"
                ]
                
                # Mostra le istruzioni una sotto l'altra
                for i, testo in enumerate(testi):
                    # Crea l'immagine del testo con font medio e colore nero
                    testo_render = Normalfont.render(testo, True, (0, 0, 0))
                    # Centra orizzontalmente
                    x = (larghezza_schermo - testo_render.get_width()) // 2
                    # Posizione verticale: parte da 200 e aumenta di 70 pixel per ogni riga
                    y = 200 + i * 70
                    # Disegna il testo
                    screen.blit(testo_render, (x, y))
            
            # ==============================================
            # SCHERMATA DI GIOCO (durante la partita)
            # ==============================================
            # Questa parte viene eseguita quando siamo IN GIOCO (in_gioco_lettere = True)
            elif in_gioco_lettere:
                # Imposta lo sfondo lavanda medio (stesso colore dei numeri per coerenza)
                screen.fill((210, 200, 240))
                
                # Titolo "GIOCO LETTERE" in alto centrato
                titolo_gioco = Titlefont.render("GIOCO LETTERE", True, (75, 0, 130))
                x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
                screen.blit(titolo_gioco, (x_titolo, 30))
                
                # ==============================================
                # INFO GIOCATORE
                # ==============================================
                if giocatore_corrente:
                    # Nome utente (nickname)
                    nome_text = Fontpiccolo.render(f"Utente: {giocatore_corrente['nome_utente']}", True, (0, 0, 0))
                    screen.blit(nome_text, (1000, 40))
                    
                    
                    # Stella con numero di vittorie
                    stelle_totali = giocatore_corrente['stelle']
                    disegna_stella(screen, (255, 215, 0), 1024, 110, 20)
                    # Mostra il numero di stelle accanto alla stella
                    testo_stelle = Fontpiccolo.render(str(stelle_totali), True, (255, 215, 0))
                    screen.blit(testo_stelle, (1060, 100))
                
                # ==============================================
                # AREA DI GIOCO PRINCIPALE
                # ==============================================
                
                # Mostra il numero del tentativo corrente
                tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                screen.blit(tentativi_text, (150, 160))
                
                # Istruzione per l'input (dice di inserire lettere)
                input_label = Normalfont.render("Inserisci 4 lettere (a-z):", True, (0, 0, 0))
                screen.blit(input_label, (150, 230))
                
                # ==============================================
                # DISEGNA LE 4 CASELLE PER INSERIRE LE LETTERE
                # ==============================================
                for i in range(4):
                    # Calcola la posizione X: parte da 150 e aumenta di 120 pixel per ogni casella
                    x = 150 + i * 120
                    y = 300  # Tutte alla stessa altezza
                    
                    # Colore della casella: azzurro se piena, bianco se vuota
                    colore_casella = (180, 220, 255) if i < len(tentativo_corrente) else (255, 255, 255)
                    
                    # Disegna la casella
                    pygame.draw.rect(screen, colore_casella, (x, y, 80, 80), border_radius=10)
                    pygame.draw.rect(screen, (0, 100, 200), (x, y, 80, 80), 3, border_radius=10)
                    
                    # Se c'è una lettera in questa posizione, la mostra
                    if i < len(tentativo_corrente):
                        num_text = Normalfont.render(tentativo_corrente[i], True, (0, 0, 0))
                        # Centra la lettera nella casella
                        num_x = x + 40 - num_text.get_width() // 2
                        num_y = y + 40 - num_text.get_height() // 2
                        screen.blit(num_text, (num_x, num_y))
                    else:
                        # Segnaposto per le posizioni vuote
                        segnaposto = Fontpiccolo.render(f"Pos {i+1}", True, (100, 100, 100))
                        segnaposto_x = x + 40 - segnaposto.get_width() // 2
                        segnaposto_y = y + 40 - segnaposto.get_height() // 2
                        screen.blit(segnaposto, (segnaposto_x, segnaposto_y))
                
                # ==============================================
                # SUGGERIMENTI (feedback per l'ultimo tentativo)
                # ==============================================
                if feedback_dettagliato[0] or storico_tentativi:
                    # Titolo della sezione in verde
                    suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                    screen.blit(suggerimenti_label, (700, 160))
                    
                    y_pos = 210  # Posizione verticale iniziale
                    
                    # Mostra il feedback per ogni posizione
                    if feedback_dettagliato[0]:
                        for i, fb in enumerate(feedback_dettagliato):
                            if fb:
                                # Verde per CORRETTO, rosso per SBAGLIATO
                                colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)
                                fb_text = Fontpiccolo.render(fb, True, colore)
                                screen.blit(fb_text, (720, y_pos))
                                y_pos += 30
                    
                    # Mostra le lettere presenti ma in posizione sbagliata
                    if storico_tentativi:
                        ultimo = storico_tentativi[-1]
                        lettere_presenti = []
                        for pos in range(4):
                            # Se la lettera è diversa da quella segreta MA è presente nel codice
                            if (ultimo[pos] != codice_segreto[pos] and 
                                ultimo[pos] in codice_segreto):
                                if ultimo[pos] not in lettere_presenti:
                                    lettere_presenti.append(ultimo[pos])
                        
                        if lettere_presenti:
                            presenti_text = f"Presenti: {', '.join(lettere_presenti)}"
                            presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                            screen.blit(presenti_render, (720, y_pos))
                            y_pos += 30
                
                # ==============================================
                # STORICO TENTATIVI
                # ==============================================
                if storico_tentativi:
                    storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                    screen.blit(storico_label, (700, 370))
                    
                    y_pos = 420
                    # Mostra tutti i tentativi fatti
                    for i, codice in enumerate(storico_tentativi):
                        numero = i + 1
                        tent_text = Fontpiccolo.render(f"{numero}) {codice}", True, (0, 0, 0))
                        screen.blit(tent_text, (720, y_pos))
                        y_pos += 30
                
                # ==============================================
                # CONSIGLIO LETTERE (analisi vocali/consonanti)
                # ==============================================
                # Crea un rettangolo per il consiglio
                rettangolo_consiglio = pygame.Rect(150, 440, 380, 200)
                pygame.draw.rect(screen, (255, 255, 240), rettangolo_consiglio, border_radius=15)
                pygame.draw.rect(screen, (100, 100, 100), rettangolo_consiglio, 3, border_radius=15)
                
                # Titolo "CONSIGLIO" centrato
                consiglio_titolo = Normalfont.render("CONSIGLIO:", True, (0, 0, 150))
                x_titolo_consiglio = rettangolo_consiglio.x + (rettangolo_consiglio.width - consiglio_titolo.get_width()) // 2
                screen.blit(consiglio_titolo, (x_titolo_consiglio, 455))
                
                # Calcola il consiglio solo dopo 6 tentativi
                if tentativi_fatti >= 6:
                    # Lista delle vocali (minuscole)
                    vocali = ['a', 'e', 'i', 'o', 'u']
                    conteggio_vocali = 0
                    conteggio_consonanti = 0
                    
                    # Conta vocali e consonanti nel codice segreto
                    for lettera in codice_segreto:
                        if lettera in vocali:
                            conteggio_vocali += 1
                        else:
                            conteggio_consonanti += 1
                    
                    # Sceglie il testo in base alla maggioranza
                    if conteggio_vocali == 4:
                        testo_maggioranza = "Tutte VOCALI"
                    elif conteggio_consonanti == 4:
                        testo_maggioranza = "Tutte CONSONANTI"
                    elif conteggio_vocali > conteggio_consonanti:
                        testo_maggioranza = "Maggioranza VOCALI"
                    else:
                        testo_maggioranza = "Maggioranza CONSONANTI"
                    
                    # Mostra il testo della maggioranza (in viola)
                    testo_magg_render = Fontpiccolo.render(testo_maggioranza, True, (150, 0, 150))
                    x_magg = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_magg_render.get_width()) // 2
                    screen.blit(testo_magg_render, (x_magg, 500))
                    
                    # Mostra il conteggio delle vocali
                    testo_vocali = f"Vocali: {conteggio_vocali}"
                    testo_vocali_render = Fontpiccolo.render(testo_vocali, True, (80, 80, 80))
                    x_vocali = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_vocali_render.get_width()) // 2
                    screen.blit(testo_vocali_render, (x_vocali, 540))
                    
                    # Mostra il conteggio delle consonanti
                    testo_consonanti = f"Consonanti: {conteggio_consonanti}"
                    testo_consonanti_render = Fontpiccolo.render(testo_consonanti, True, (80, 80, 80))
                    x_consonanti = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_consonanti_render.get_width()) // 2
                    screen.blit(testo_consonanti_render, (x_consonanti, 570))
                else:
                    # Messaggio di attesa prima del 6° tentativo
                    tentativi_mancanti = 6 - tentativi_fatti
                    
                    if tentativi_mancanti == 1:
                        messaggio = f"Disponibile tra 1 tentativo"
                    else:
                        messaggio = f"Disponibile tra {tentativi_mancanti} tentativi"
                    
                    testo_attesa = Fontpiccolo.render(messaggio, True, (150, 150, 150))
                    x_attesa = rettangolo_consiglio.x + (rettangolo_consiglio.width - testo_attesa.get_width()) // 2
                    screen.blit(testo_attesa, (x_attesa, 520))
                
                # ==============================================
                # ISTRUZIONI (sempre visibili in basso a sinistra)
                # ==============================================
                istruzioni = [
                    "ISTRUZIONI:",
                    "- Usa tasti A-Z per inserire lettere",
                    "- BACKSPACE cancella",
                    "- INVIO conferma",
                    "- ESC per tornare"
                ]
                
                y_pos = 670
                for testo in istruzioni:
                    # Grigio per le istruzioni, nero per il titolo "ISTRUZIONI"
                    colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                    testo_render = Fontpiccolo.render(testo, True, colore)
                    screen.blit(testo_render, (150, y_pos))
                    y_pos += 30
            
            # ==============================================
            # SCHERMATA FINE GIOCO (vittoria o sconfitta)
            # ==============================================
            elif gioco_finito:
                # Sfondo giallo chiaro (come le istruzioni iniziali)
                screen.fill((255, 250, 200))
                
                # Titolo in base al risultato
                if risultato == "VITTORIA":
                    titolo_risultato = Titlefont.render("HAI VINTO!", True, (0, 150, 0))
                else:
                    titolo_risultato = Titlefont.render("HAI PERSO!", True, (200, 0, 0))
                
                # Centra il titolo
                x_titolo = (larghezza_schermo - titolo_risultato.get_width()) // 2
                screen.blit(titolo_risultato, (x_titolo, 80))
                
                # Info sui tentativi effettuati
                info1 = Normalfont.render(f"Hai fatto {tentativi_fatti} tentativi su 10", True, (0, 0, 0))
                x_info1 = (larghezza_schermo - info1.get_width()) // 2
                screen.blit(info1, (x_info1, 200))
                
                # Testo "Il codice corretto era:"
                codice_label = Normalfont.render("Il codice corretto era:", True, (0, 0, 0))
                x_codice_label = (larghezza_schermo - codice_label.get_width()) // 2
                screen.blit(codice_label, (x_codice_label, 280))
                
                # ==============================================
                # CASELLE CON IL CODICE CORRETTO (in MAIUSCOLO)
                # ==============================================
                # Calcola la posizione X per centrare le 4 caselle
                x_inizio_caselle = (larghezza_schermo - (4 * 120)) // 2
                for i in range(4):
                    x = x_inizio_caselle + i * 130
                    y = 360
                    
                    # Caselle verdi per il codice corretto
                    pygame.draw.rect(screen, (200, 255, 200), (x, y, 80, 80), border_radius=10)
                    pygame.draw.rect(screen, (0, 100, 0), (x, y, 80, 80), 3, border_radius=10)
                    
                    # Mostra la lettera in MAIUSCOLO (.upper()) per maggiore leggibilità
                    lettera_text = Normalfont.render(codice_segreto[i].upper(), True, (0, 0, 0))
                    lettera_x = x + 40 - lettera_text.get_width() // 2
                    lettera_y = y + 40 - lettera_text.get_height() // 2
                    screen.blit(lettera_text, (lettera_x, lettera_y))
                
                # Istruzioni per continuare
                continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                screen.blit(continua_text, (x_continua, 550))
                
                rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                screen.blit(rigioca_text, (x_rigioca, 620))
        
        # ==============================================
        # STATO GIOCO - COLORI
        # ==============================================
            
        # Questo blocco viene eseguito solo quando siamo nello stato "gioco" 
        # e abbiamo scelto la modalità "colori"
        elif stato == "gioco" and dove_siamo == "colori":
            
            # ==============================================
            # SCHERMATA ISTRUZIONI (prima di iniziare la partita)
            # ==============================================
            # Questa parte viene eseguita quando NON siamo in gioco (in_gioco_colori = False)
            # e la partita NON è finita (gioco_finito = False)
            if not in_gioco_colori and not gioco_finito:
                # Imposta il colore di sfondo azzurro chiaro (RGB)
                screen.fill((200, 230, 255))
                
                # Crea il titolo "MODALITÀ COLORI" con font grande e colore blu scuro
                titolo_colori = Titlefont.render("MODALITÀ COLORI", True, (0, 0, 150))
                # Calcola la posizione X per centrare il titolo orizzontalmente
                x_titolo = (larghezza_schermo - titolo_colori.get_width()) // 2
                # Disegna il titolo alla posizione calcolata (x centrata, y=50)
                screen.blit(titolo_colori, (x_titolo, 50))
                
                # Lista delle istruzioni da mostrare
                testi = [
                    "Qui giocherai con i colori!",
                    "Il computer penserà a 4 colori (numeri da 1 a 8)",
                    "Tu dovrai indovinarli in 10 tentativi",
                     "Attenzione! I colori possono essere ripetuti!",
                    "Premi I per iniziare a giocare",
                    "Premi ESC per tornare al menu"
                ]
                
                # Mostra le istruzioni una sotto l'altra
                for i, testo in enumerate(testi):
                    # Crea l'immagine del testo con font medio e colore nero
                    testo_render = Normalfont.render(testo, True, (0, 0, 0))
                    # Centra orizzontalmente
                    x = (larghezza_schermo - testo_render.get_width()) // 2
                    # Posizione verticale: parte da 200 e aumenta di 70 pixel per ogni riga
                    y = 200 + i * 70
                    # Disegna il testo
                    screen.blit(testo_render, (x, y))
            
            # ==============================================
            # SCHERMATA DI GIOCO (durante la partita)
            # ==============================================
            # Questa parte viene eseguita quando siamo IN GIOCO (in_gioco_colori = True)
            elif in_gioco_colori:
                # Imposta lo sfondo lavanda medio (stesso colore delle altre modalità)
                screen.fill((210, 200, 240))
                
                # Titolo "GIOCO COLORI" in alto centrato
                titolo_gioco = Titlefont.render("GIOCO COLORI", True, (75, 0, 130))
                x_titolo = (larghezza_schermo - titolo_gioco.get_width()) // 2
                screen.blit(titolo_gioco, (x_titolo, 30))
                
                # ==============================================
                # INFO GIOCATORE (in alto a destra) - STESSA POSIZIONE
                # ==============================================
                if giocatore_corrente:
                    # Nome utente (nickname)
                    nome_text = Fontpiccolo.render(f"Utente: {giocatore_corrente['nome_utente']}", True, (0, 0, 0))
                    screen.blit(nome_text, (1000, 40))
                    
                    
                    # Stella con numero di vittorie
                    stelle_totali = giocatore_corrente['stelle']
                    disegna_stella(screen, (255, 215, 0), 1024, 110, 20)
                    # Mostra il numero di stelle accanto alla stella
                    testo_stelle = Fontpiccolo.render(str(stelle_totali), True, (255, 215, 0))
                    screen.blit(testo_stelle, (1060, 100))
                
                # ==============================================
                # AREA DI GIOCO PRINCIPALE
                # ==============================================
                
                # Mostra il numero del tentativo corrente
                tentativi_text = Normalfont.render(f"Tentativo: {tentativi_fatti}/10", True, (0, 0, 0))
                screen.blit(tentativi_text, (150, 160))
                
                # Istruzione per l'input (dice di inserire numeri da 1 a 8)
                input_label = Normalfont.render("Inserisci 4 numeri (1-8):", True, (0, 0, 0))
                screen.blit(input_label, (150, 230))
                
                # ==============================================
                # DISEGNA LE 4 CASELLE COLORATE
                # ==============================================
                for i in range(4):
                    # Calcola la posizione X: parte da 150 e aumenta di 120 pixel per ogni casella
                    x = 150 + i * 120
                    y = 300  # Tutte alla stessa altezza
                    
                    # Colore di partenza: bianco (default)
                    colore_casella = (255, 255, 255)
                    # Se la casella è piena e contiene un numero valido
                    if i < len(tentativo_corrente) and tentativo_corrente[i].isdigit():
                        # Converte il carattere in numero (es. '3' -> 3)
                        indice = int(tentativo_corrente[i]) - 1  # -1 perché gli indici partono da 0
                        # Controlla che l'indice sia valido (0-7)
                        if 0 <= indice < len(colori_disponibili):
                            # Imposta il colore della casella al colore corrispondente
                            colore_casella = colori_disponibili[indice]
                    
                    # Disegna la casella con il colore calcolato
                    pygame.draw.rect(screen, colore_casella, (x, y, 80, 80), border_radius=10)
                    pygame.draw.rect(screen, (0, 100, 200), (x, y, 80, 80), 3, border_radius=10)
                    
                    # Se c'è un numero in questa posizione, lo mostra
                    if i < len(tentativo_corrente):
                        num_text = Normalfont.render(tentativo_corrente[i], True, (0, 0, 0))
                        # Centra il numero nella casella
                        num_x = x + 40 - num_text.get_width() // 2
                        num_y = y + 40 - num_text.get_height() // 2
                        screen.blit(num_text, (num_x, num_y))
                    else:
                        # Segnaposto per le posizioni vuote
                        segnaposto = Fontpiccolo.render(f"Pos {i+1}", True, (100, 100, 100))
                        segnaposto_x = x + 40 - segnaposto.get_width() // 2
                        segnaposto_y = y + 40 - segnaposto.get_height() // 2
                        screen.blit(segnaposto, (segnaposto_x, segnaposto_y))
                
                # ==============================================
                # LEGENDA COLORI
                # ==============================================
                # Posizione verticale della scritta "LEGENDA COLORI"
                legenda_y = 450
                legenda_label = Normalfont.render("LEGENDA COLORI:", True, (0, 0, 150))
                screen.blit(legenda_label, (150, legenda_y))
                
                # Mostra gli 8 colori disponibili su 2 righe da 4
                for i in range(8):
                    # Calcola riga e colonna (2 righe, 4 colonne)
                    riga = i // 4
                    colonna = i % 4
                    # Posizione X: parte da 170 e aumenta di 130 pixel per colonna
                    x = 170 + colonna * 130
                    # Posizione Y: legenda_y + 85 (spazio sotto il titolo) + riga * 45
                    y = legenda_y + 85 + riga * 45
                    
                    # Disegna un cerchio colorato
                    pygame.draw.circle(screen, colori_disponibili[i], (x, y), 15)
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), 15, 1)
                    
                    # Mostra il numero del colore accanto al cerchio
                    num_leg = Fontpiccolo.render(str(i+1), True, (0, 0, 0))
                    screen.blit(num_leg, (x + 20, y - 8))
                
                # ==============================================
                # SUGGERIMENTI (feedback per l'ultimo tentativo)
                # ==============================================
                if feedback_dettagliato[0] or storico_tentativi:
                    # Titolo della sezione in verde
                    suggerimenti_label = Normalfont.render("SUGGERIMENTI:", True, (0, 100, 0))
                    screen.blit(suggerimenti_label, (700, 160))
                    
                    y_pos = 210  # Posizione verticale iniziale
                    
                    # Mostra il feedback per ogni posizione
                    if feedback_dettagliato[0]:
                        for i, fb in enumerate(feedback_dettagliato):
                            if fb:
                                # Verde per CORRETTO, rosso per SBAGLIATO
                                colore = (0, 150, 0) if "CORRETTO" in fb else (200, 0, 0)
                                fb_text = Fontpiccolo.render(fb, True, colore)
                                screen.blit(fb_text, (720, y_pos))
                                y_pos += 30
                    
                    # Mostra i numeri presenti ma in posizione sbagliata
                    if storico_tentativi:
                        ultimo = storico_tentativi[-1]
                        numeri_presenti = []
                        for pos in range(4):
                            # Controlla ogni posizione
                            if pos < len(ultimo) and pos < len(codice_segreto):
                                # Se il numero è diverso da quello segreto MA è presente nel codice
                                if int(ultimo[pos]) != codice_segreto[pos] and int(ultimo[pos]) in codice_segreto:
                                    # Evita duplicati
                                    if ultimo[pos] not in numeri_presenti:
                                        numeri_presenti.append(ultimo[pos])
                        
                        if numeri_presenti:
                            presenti_text = f"Presenti: {', '.join(numeri_presenti)}"
                            presenti_render = Fontpiccolo.render(presenti_text, True, (200, 100, 0))
                            screen.blit(presenti_render, (720, y_pos))
                            y_pos += 30
                
                # ==============================================
                # TENTATIVI (con cerchietti colorati)
                # ==============================================
                if storico_tentativi:
                    storico_label = Normalfont.render("TENTATIVI:", True, (0, 0, 150))
                    screen.blit(storico_label, (700, 400))
                    
                    y_pos = 450
                    # Mostra tutti i tentativi fatti
                    for i in range(len(storico_tentativi)):
                        numero = i + 1
                        codice = storico_tentativi[i]
                        
                        # Mostra il numero del tentativo (es. "1)")
                        num_tent = Fontpiccolo.render(f"{numero})", True, (0, 0, 0))
                        screen.blit(num_tent, (700, y_pos))
                        
                        # Per ogni posizione, disegna un cerchietto del colore corrispondente
                        for j in range(4):
                            if j < len(codice) and codice[j].isdigit():
                                indice = int(codice[j]) - 1
                                if 0 <= indice < len(colori_disponibili):
                                    x_cerchio = 750 + j * 35
                                    # Disegna un cerchio colorato più piccolo (raggio 10)
                                    pygame.draw.circle(screen, colori_disponibili[indice], (x_cerchio, y_pos + 20), 10)
                                    pygame.draw.circle(screen, (0, 0, 0), (x_cerchio, y_pos + 20), 10, 1)
                        
                        y_pos += 35  # Sposta in basso per il prossimo tentativo
                
                # ==============================================
                # ISTRUZIONI (sempre visibili in basso a sinistra)
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
                    # Grigio per le istruzioni, nero per il titolo "ISTRUZIONI"
                    colore = (100, 100, 100) if not testo.startswith("ISTRUZIONI") else (0, 0, 0)
                    testo_render = Fontpiccolo.render(testo, True, colore)
                    screen.blit(testo_render, (150, y_pos))
                    y_pos += 30
            
            # ==============================================
            # SCHERMATA FINE GIOCO (vittoria o sconfitta)
            # ==============================================
            elif gioco_finito:
                # Sfondo azzurro (come le istruzioni iniziali)
                screen.fill((200, 230, 255))
                
                # Titolo in base al risultato
                if risultato == "VITTORIA":
                    titolo_risultato = Titlefont.render("HAI VINTO!", True, (0, 150, 0))
                else:
                    titolo_risultato = Titlefont.render("HAI PERSO!", True, (200, 0, 0))
                
                # Centra il titolo
                x_titolo = (larghezza_schermo - titolo_risultato.get_width()) // 2
                screen.blit(titolo_risultato, (x_titolo, 80))
                
                # Info sui tentativi effettuati
                info1 = Normalfont.render(f"Hai fatto {tentativi_fatti} tentativi su 10", True, (0, 0, 0))
                x_info1 = (larghezza_schermo - info1.get_width()) // 2
                screen.blit(info1, (x_info1, 200))
                
                # Testo "Il codice corretto era:"
                codice_label = Normalfont.render("Il codice corretto era:", True, (0, 0, 0))
                x_codice_label = (larghezza_schermo - codice_label.get_width()) // 2
                screen.blit(codice_label, (x_codice_label, 280))
                
                # ==============================================
                # CERCHI CON IL CODICE CORRETTO
                # ==============================================
                # Calcola la posizione X per centrare i 4 cerchi
                x_inizio = (larghezza_schermo - (4 * 115)) // 2
                for i in range(4):
                    x = x_inizio + i * 120
                    y = 360
                    
                    if i < len(codice_segreto):
                        # Trova l'indice del colore (codice_segreto[i] è un numero da 1 a 8)
                        indice = codice_segreto[i] - 1
                        colore = colori_disponibili[indice]
                        
                        # Disegna un cerchio grande con il colore corretto
                        pygame.draw.circle(screen, colore, (x + 40, y + 40), 35)
                        pygame.draw.circle(screen, (0, 0, 0), (x + 40, y + 40), 35, 3)
                        
                        # Mostra il numero al centro del cerchio
                        num_text = Normalfont.render(str(codice_segreto[i]), True, (0, 0, 0))
                        num_x = x + 40 - num_text.get_width() // 2
                        num_y = y + 40 - num_text.get_height() // 2
                        screen.blit(num_text, (num_x, num_y))
                
                # Istruzioni per continuare
                continua_text = Normalfont.render("Premi ESC per tornare alle istruzioni", True, (0, 0, 0))
                x_continua = (larghezza_schermo - continua_text.get_width()) // 2
                screen.blit(continua_text, (x_continua, 580))
                
                rigioca_text = Normalfont.render("Premi I per rigiocare", True, (0, 0, 0))
                x_rigioca = (larghezza_schermo - rigioca_text.get_width()) // 2
                screen.blit(rigioca_text, (x_rigioca, 650))
        
        # pygame.display.flip() aggiorna tutto lo schermo
        # Mostra tutte le modifiche fatte in questo ciclo
        pygame.display.flip()
    
    # pygame.quit() chiude tutti i moduli pygame quando si esce dal loop
    pygame.quit()

# Questo if esegue main() solo se il file è eseguito direttamente
# (non se viene importato come modulo)
if __name__ == "__main__":
    main()



