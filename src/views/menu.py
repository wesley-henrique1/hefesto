import tkinter as tk
import customtkinter as ctk

class Menu:
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.familia = "Consolas"

        root = ctk.CTk()
        root.geometry("400x250")
        root.title("Hefesto - Exemplo CTkEntry")

        self.__mod(root)
        self.__localizador()

        root.mainloop()
        pass

    def __mod(self, tela):
        self.entr_id = ctk.CTkEntry(
            tela, 
            width=200, 
            height=35, 
            placeholder_text="ID do Módulo"
        )       
    pass
    def __clicaveis(self):
        pass
    def __localizador(self):
        self.entr_id.place(x=50, y=80)
        pass

if __name__ == "__main__":
    Menu()