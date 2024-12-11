import csv
import os
import locale
from time import sleep
from colors import bcolors

# Metainformation om skriptet
__author__  = "Simon Wristel"
__version__ = "1.0.0"
__email__   = "Simon.wristel@ga.ntig.se"

locale.setlocale(locale.LC_ALL, '')

# Visas i 2 sekunder och försvinner det efter
print(bcolors.BLUE +"""
       _______________________________
      |                               |
      |  Välkommen till snusbolaget!  |
      |_______________________________|""")
sleep(2)  # Väntar 2 sekunder
os.system('cls' if os.name == 'nt' else 'clear')  # Rensar skärmen

# Klassdefinition för produkter
class Product:
    def __init__(self, id, name, desc, price, quantity):
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self): # gör så att meningarna över 35 eller 40 ord blir förkortade med "..." efter
        truncated_name = (self.name[:40] + '...') if len(self.name) > 40 else self.name
        truncated_desc = (self.desc[:35] + '...') if len(self.desc) > 35 else self.desc
        
        return f"{self.id:<5} {truncated_name:<45} {truncated_desc:<40} {locale.currency(self.price, grouping=True):<15} {self.quantity:<8}"


def load_data(filename): 
    products = [] 
    try:
        with open(filename, 'r', encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']
                price = float(row['price'])
                quantity = int(row['quantity'])
                
                products.append(Product(id, name, desc, price, quantity))
    except FileNotFoundError:
        print(bcolors.RED + f"Filen {filename} hittades tyvärr inte.") #om filen är felaktig skriver detta ut
    return products


def remove_product(products, id): #funktion för att ta bort produkter i listan
    temp_product = None

    for product in products:
        if product.id == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)
        return (bcolors.YELLOW + f"Product: {id} {temp_product.name} was removed")
    else:
        return f"Product with id {id} not found"


def view_product(products, id): #funktion för att visa produkten
    for product in products:
        if product.id == id:
            return str(product)
    
    return "Produkten hittas inte"


def view_products(products): #visar produkten i listan
    header = f"{'ID':<5} {'Namn':<45} {'Beskrivning':<40} {'Pris':<15} {'Antal':<8}" 
    product_list = [header]
    for product in products:
        product_list.append(str(product))
    
    return "\n".join(product_list)


def add_product(products, name, desc, price, quantity): #funktion för att lägga till produkter i listan
    if products:
        max_id = max(products, key=lambda x: x.id)
        id_value = max_id.id
    else:
        id_value = 0

    id = id_value + 1

    new_product = Product(id, name, desc, price, quantity)
    products.append(new_product)
    return f"lade till produkt: {id}"
    sleep(1)


# Huvudprogram
products = load_data('db_products.csv')

while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(bcolors.RED + view_products(products))  

        choice = input(bcolors.DEFAULT + "Vill du (V)isa, (T)a bort, (L)ägga till eller (Ä)ndra en produkt? ").strip().upper()

        if choice == "L": #om användaren väljer L så kan användaren lägga in en produkt i listan
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))
            print(add_product(products, name, desc, price, quantity))
            sleep(0.5)

        else:
            id = int(input("Ange produktens ID: "))

            if choice == "V":  
                print(view_product(products, id))
                input("Tryck på enter för att fortsätta...")

            elif choice == "T": 
                print(remove_product(products, id))
                sleep(0.5)

            elif choice == "Ä": #om användaren väljer Ä så kan användaren ändra produkten i listan
                selected_product = next((product for product in products if product.id == id), None)
                if selected_product:
                    print(bcolors.PURPLE + "Skriv något nytt eller tryck enter direkt för att behålla det som var innan.")
                    selected_product.name = input(f"Nytt namn (behåll {selected_product.name}): ") or selected_product.name
                    selected_product.desc = input(f"Ny beskrivning (behåll {selected_product.desc}): ") or selected_product.desc
                    selected_product.price = float(input(f"Nytt pris (behåll {selected_product.price}): ") or selected_product.price)
                    selected_product.quantity = int(input(f"Nytt antal (behåll {selected_product.quantity}): ") or selected_product.quantity)

                    print(bcolors.BLUE + f"Produkten med id {selected_product.id} uppdaterades.")
                    sleep(0.5)

                else:
                    print(bcolors.RED + "Ogiltig produkt")
                    sleep(0.3)
        
    except ValueError:
        print(bcolors.GREEN + "Välj en produkt med siffror")
        sleep(0.5)
