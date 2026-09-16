import customtkinter as ctk

class BotsUI:
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"


        root = ctk.CTk()
        root.title("Gerenciador_8000")
        root.geometry("500x400")
        root.configure(fg_color=self.marromClaro)
        # root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)

        root.mainloop()
        pass

    def Componetes(self, tela):
        self.Painel = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        pass
    def Clicaveis(self):
        pass
    def Componentes(self):
        self.Painel.place_configure(relx= 0.02, rely= 0.02, relheight= 0)
        pass


if __name__ == "__main__":
    BotsUI()