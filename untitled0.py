from pynput import mouse
from pynput import keyboard
import pyperclip
import threading
import time

HOLD_TIME = 0.2
 
encrypt = ""
message = ""
start = None
stop_event = threading.Event()

def on_press(key):
    
    global encrypt
    global message
    
    if key == keyboard.Key.space:
        encrypt += " "          #  separa lettere
        print(" ")

    if key == keyboard.Key.tab:
        encrypt += " / "   
        print("======================")
         
    if key == keyboard.Key.enter:
        message = parse_morse(encrypt)
        pyperclip.copy(message)
        print("Copiato!")
    
    if key == keyboard.Key.esc:
        print(f"Morse: {message}")
        stop_event.set()        # ← segnala lo stop
        mouse_listener.stop()
        key_listener.stop()

def on_hold(*args):
    print("Hold.")

def on_click(x, y, button, pressed):
    
    global start
    global encrypt
    
    if pressed:
        start = time.time()
        
        
    else:
        if start is not None:
            durata = time.time() - start
            
            if durata >= HOLD_TIME:
                on_hold()
                encrypt += "-"
            else:
                encrypt += "."
                print("Click")

            start = None
             
def parse_morse(s):
    
    message = ""
    
    MORSE_DICT = {"A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...", 
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    " ": " ",}
    
    Reverse = {v:k for k,v in MORSE_DICT.items()}
  
    parole = s.strip().split("/")
    for parola in parole:
        letters = parola.strip().split(" ")
        for code in letters:
            if code == "":
                continue
            if code in Reverse:
                message += Reverse[code]
            else:
                message += "?"
        message += " "
        
    
    return message
            
mouse_listener = mouse.Listener(on_click=on_click)
key_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()  # ← .start() non blocca
key_listener.start()


mouse_listener.join()   # ← aspetta qui
key_listener.join()

stop_event.wait()
print("Programma terminato.")


