import re
import hashlib
import tkinter as tk
from tkinter import messagebox
import string
import secrets
import urllib.request
import urllib.error


def verifica_brese_securitate(parola):
    sha1_hash = hashlib.sha1(parola.encode('utf-8')).hexdigest().upper()
    prefix, sufix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Proiect-Securitate-CV'})
        with urllib.request.urlopen(req) as response:
            rezultate = response.read().decode('utf-8').splitlines()
        for linie in rezultate:
            hash_primit, count = linie.split(':')
            if hash_primit == sufix: return int(count)
        return 0
    except Exception: return -1

def calculeaza_timp_spargere(parola):
    pool_caractere = 0
    if re.search(r"[a-z]", parola): pool_caractere += 26
    if re.search(r"[A-Z]", parola): pool_caractere += 26
    if re.search(r"\d", parola): pool_caractere += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", parola): pool_caractere += 32
    
    if pool_caractere == 0: return "Instantaneu"
    
    combinatii = pool_caractere ** len(parola)
    incercari_pe_secunda = 10_000_000_000 
    secunde = combinatii / incercari_pe_secunda
    
    if secunde < 1: return "Sub o secundă ❌"
    elif secunde < 60: return f"{int(secunde)} secunde ⚠️"
    elif secunde < 3600: return f"{int(secunde/60)} minute ⚠️"
    elif secunde < 86400: return f"{int(secunde/3600)} ore ⏳"
    elif secunde < 31536000: return f"{int(secunde/86400)} zile 🛡️"
    elif secunde < 3153600000: return f"{int(secunde/31536000)} ani 💪"
    else: return "fffoarte greu de spart"

def evalueaza_parola(parola):
    scor = 0
    if len(parola) >= 12: scor += 1
    if re.search(r"[A-Z]", parola) and re.search(r"[a-z]", parola): scor += 1
    if re.search(r"\d", parola): scor += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", parola): scor += 1

    aparitii_pwned = verifica_brese_securitate(parola)
    
    if aparitii_pwned > 0: return f"COMPROMISĂ! ☠️\nGăsită pe net de {aparitii_pwned} ori!", "#e74c3c"
    elif aparitii_pwned == -1: mesaj_extra = "\n(Eroare rețea API)"
    else: mesaj_extra = "\n(Curată în baze de date ✅)"

    if scor == 4: return "Puternică! 💪" + mesaj_extra, "#27ae60"
    elif scor >= 2: return "Medie. Se poate mai bine. 🧐" + mesaj_extra, "#f39c12"
    else: return "Slabă. Vulnerabilă! 🚩" + mesaj_extra, "#e74c3c"

def proceseaza_parola():
    parola = intrare_parola.get()
    if not parola:
        label_rezultat.config(text="Introdu o parolă!", fg="#e74c3c")
        label_timp.config(text="")
        return
        
    label_rezultat.config(text="Se analizează...", fg="#3498db")
    fereastra.update()
    
    verdict, culoare = evalueaza_parola(parola)
    timp_spargere = calculeaza_timp_spargere(parola)
    hash_final = hashlib.sha256(parola.encode('utf-8')).hexdigest()
    
    label_rezultat.config(text=f"{verdict}", fg=culoare)
    label_timp.config(text=f"Timp estimat (Brute-Force):\n{timp_spargere}", fg="#8e44ad")
    label_hash.config(text=f"Amprentă SHA-256:\n{hash_final}")

def genereaza_parola_sigura():
    alfabet = string.ascii_letters + string.digits + "!@#$%^&*"
    parola_noua = ''.join(secrets.choice(alfabet) for i in range(16))
    
    intrare_parola.delete(0, tk.END)
    intrare_parola.insert(0, parola_noua)
    
    # NOU: Când generăm parola, o facem automat vizibilă
    arata_parola_var.set(1)
    toggle_parola()
    
    proceseaza_parola()

def copiaza_in_clipboard():
    parola = intrare_parola.get()
    if parola:
        fereastra.clipboard_clear()
        fereastra.clipboard_append(parola)
        messagebox.showinfo("Succes", "Parola a fost copiată în clipboard!")

# NOU: Funcția care ascunde/arată parola
def toggle_parola():
    if arata_parola_var.get() == 1:
        intrare_parola.config(show="") # Arată textul
    else:
        intrare_parola.config(show="*") # Ascunde cu steluțe



BG_APP = "#f4f6f9"
BG_CARD = "#ffffff"
TXT_COLOR = "#2c3e50"

fereastra = tk.Tk()
fereastra.title("Security Toolkit: Password Analyzer")
fereastra.geometry("650x650") # Am mărit puțin fereastra
fereastra.configure(bg=BG_APP)

card = tk.Frame(fereastra, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground="#e0e0e0", padx=30, pady=30)
card.pack(pady=40, padx=40, fill="both", expand=True)

titlu = tk.Label(card, text="🔐 Security Toolkit", font=("Segoe UI", 22, "bold"), bg=BG_CARD, fg=TXT_COLOR)
titlu.pack(pady=(0, 20))

# NOU: Am setat show="*" din start pentru a ascunde parola
intrare_parola = tk.Entry(card, font=("Segoe UI", 16), width=30, bg="#f8f9fa", fg="#333", bd=1, relief="solid", justify="center", show="*")
intrare_parola.pack(pady=(15, 5), ipady=8)

# NOU: Checkbox-ul pentru vizualizare parolă
arata_parola_var = tk.IntVar() # Variabilă care ține minte dacă e bifat sau nu (0 sau 1)
check_arata = tk.Checkbutton(card, text="👁️ Vizualizare parolă", variable=arata_parola_var, command=toggle_parola, bg=BG_CARD, fg="#7f8c8d", font=("Segoe UI", 10), activebackground=BG_CARD, cursor="hand2")
check_arata.pack(pady=(0, 15))

frame_butoane = tk.Frame(card, bg=BG_CARD)
frame_butoane.pack(pady=10)

btn_eval = tk.Button(frame_butoane, text="🔍 Evaluează", command=proceseaza_parola, font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", relief="flat", cursor="hand2", padx=15, pady=8)
btn_eval.grid(row=0, column=0, padx=8)

btn_copy = tk.Button(frame_butoane, text="📋 Copiază", command=copiaza_in_clipboard, font=("Segoe UI", 11, "bold"), bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white", relief="flat", cursor="hand2", padx=15, pady=8)
btn_copy.grid(row=0, column=1, padx=8)

btn_gen = tk.Button(frame_butoane, text="🎲 Generează Parolă", command=genereaza_parola_sigura, font=("Segoe UI", 11, "bold"), bg="#9b59b6", fg="white", activebackground="#8e44ad", activeforeground="white", relief="flat", cursor="hand2", padx=15, pady=8)
btn_gen.grid(row=0, column=2, padx=8)

separator = tk.Frame(card, bg="#ecf0f1", height=2)
separator.pack(fill="x", pady=20)

label_rezultat = tk.Label(card, text="Aștept introducerea parolei...", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg="#7f8c8d")
label_rezultat.pack(pady=5)

label_timp = tk.Label(card, text="", font=("Segoe UI", 12, "bold"), bg=BG_CARD)
label_timp.pack(pady=10)

frame_hash = tk.Frame(card, bg="#f1f2f6", padx=10, pady=10)
frame_hash.pack(pady=10, fill="x")

label_hash = tk.Label(frame_hash, text="Amprentă SHA-256 va apărea aici.", font=("Consolas", 10), bg="#f1f2f6", fg="#95a5a6", wraplength=480)
label_hash.pack()

fereastra.mainloop()