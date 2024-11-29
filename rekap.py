import os
import random
import time
import requests
from colorama import Fore, init

init()

def send_to_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

TOKEN = "7319217799:AAFMm4wsA24r54DdgI2f86zgLcGaWp6uY3k"
CHAT_ID = "5839321572"

def format_rupiah(amount):
    return f"Profit -> Rp{amount * 1000:,}".replace(",", ".")

def mainsec():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + '''
▓█████ ▒██   ██▒ ▒█████   ▄▄▄▄    ▒█████  ▄▄▄█████▓
▓█   ▀ ▒▒ █ █ ▒░▒██▒  ██▒▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
▒███   ░░  █   ░▒██░  ██▒▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
▒▓█  ▄  ░ █ █ ▒ ▒██   ██░▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
░▒████▒▒██▒ ▒██▒░ ████▓▒░░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
░░ ▒░ ░▒▒ ░ ░▓ ░░ ▒░▒░▒░ ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
 ░ ░  ░░░   ░▒ ░  ░ ▒ ▒░ ▒░▒   ░   ░ ▒ ▒░     ░    
   ░    ░    ░  ░ ░ ░ ▒   ░    ░ ░ ░ ░ ▒    ░      
   ░  ░ ░    ░      ░ ░   ░          ░ ░           
                               ░                   
Command Line Interface Rekap - By Avoix88          
''' + Fore.RESET) 

    print(Fore.RED + "[" + Fore.WHITE + "+" + Fore.RED + "]" + Fore.WHITE + " 1. Total Profit" + Fore.RESET)
    print(Fore.RED + "[" + Fore.WHITE + "+" + Fore.RED + "]" + Fore.WHITE + " 2. Rekap ( 3 MODE )" + Fore.RESET)
    print(Fore.RED + "[" + Fore.WHITE + "+" + Fore.RED + "]" + Fore.WHITE + " 3. Exit And Rekap ( Send To Tele )" + Fore.RESET)

    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

    total_profit = 0
    if os.path.exists('profit.txt'):
        with open('profit.txt', 'r') as file:
            line = file.readline().strip()
            line = line.replace("Rp", "").replace(".", "")
            total_profit = int(float(line)) if line else 0 

    while True:
        try:
            select = input(Fore.RESET + "Pilih : ")
            if select == "1":
                print(Fore.GREEN + f"Total Profit: {format_rupiah(total_profit)}" + Fore.RESET)
            elif select == "2":
                while True:
                    wordlist_file = input(Fore.RED + "[+] " + Fore.GREEN + "Nominal? (contoh: 50A) : " + Fore.RESET)

                    if wordlist_file == "1":
                        break

                    if not wordlist_file[:-1].isdigit() or wordlist_file[-1].upper() not in 'ABC':
                        print(Fore.RED + "[+] Input tidak valid. Masukkan angka diikuti mode (A, B, atau C)." + Fore.RESET)
                        continue

                    mode = wordlist_file[-1].upper()
                    nominal = int(wordlist_file[:-1])
                    base_value = nominal * 2
                    deduction = base_value * 0.06  

                    if mode == 'A':
                        hasil = round(base_value - deduction)
                        profit = round(base_value - hasil)
                    elif mode == 'B':
                        hasil = round((base_value - deduction) - nominal)
                        profit = round(nominal - hasil)
                    elif mode == 'C':
                        hasil = round((base_value - deduction - nominal) - 1)
                        profit = round(nominal - hasil)

                    total_profit += profit
                    random_color = random.choice(colors)
                    print(Fore.RED + "[" + Fore.WHITE + "+" + Fore.RED + "]" + random_color + f"Hasil : {hasil}, PROFIT : {profit}" + Fore.RESET)

                    with open("profit.txt", "w") as file:
                        file.write(str(total_profit))

            elif select == "3":
                with open("profit.txt", "r") as file:
                    total_profit = int(float(file.readline().strip()))
                
                formatted_content = f"{format_rupiah(total_profit)}\nDATE -> {time.strftime('%d/%m/%Y')}"
                
                with open("profit.txt", "w") as file:
                    file.write(formatted_content)
                
                if send_to_telegram(formatted_content, TOKEN, CHAT_ID):
                    print(Fore.RED + "[" + Fore.WHITE + "+" + Fore.RED + "]" + Fore.GREEN + "Konversi selesai :" + Fore.RESET)
                else:
                    print(Fore.RED + "Gagal mengirim pesan ke Telegram." + Fore.RESET)

                print(Fore.GREEN + formatted_content + Fore.RESET)
                input(Fore.YELLOW + "\nOperation complete. Press Enter to exit..." + Fore.RESET)
                break

        except EOFError:
            print(Fore.YELLOW + "\nOperation complete. Press Enter to exit..." + Fore.RESET)
            input()
            break

if __name__ == "__main__":
    mainsec()
