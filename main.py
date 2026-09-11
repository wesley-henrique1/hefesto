from src.lib.caminhos import _Imagens, _Icone
import webbrowser
import tkinter as tk
import customtkinter as ctk
from PIL import Image

class __auxiliares:
    def FUNC_Iniciar(self):
        print("iniciar 3... 2.. 1...")
    def FUNC_bot(self):
        print("bot 3... 2.. 1...")
    def FUNC_demandas(self):
        print("demandas 3... 2.. 1...")
    def FUNC_config(self):
        print("config 3... 2.. 1...")
    def AbrirGIT(self, event=None):
        webbrowser.open("https://github.com/wesley-henrique1")

class Main(__auxiliares):
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.familia = "Consolas"

        root = ctk.CTk()
        root.title("Gerenciador_8000")
        root.geometry("800x600")
        root.configure(fg_color=self.marromClaro)
        root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)

        self.ImagemOrigem = Image.open(_Imagens.perfil)

        self.__Componentes(root)
        self.__clicaveis()
        self.__localizador()
        root.mainloop()
        pass

    def __Componentes(self, tela):
        self.pipelines = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        self.contador = ctk.CTkLabel(
            tela,
            text= "PROGRESSO: 0/0 | MODULO.py | tempo: 00:00:00",
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
            font=(self.familia, 16),
            text_color= self.preto,
            anchor= "center",
        )
        self.logArquivo = ctk.CTkTextbox(
            tela,
            fg_color= self.branco,
            font= (self.familia, 12),

            border_color= self.preto,
            border_width= 3,
            border_spacing= 4,
            state= 'disabled'
        )
        self.painel = ctk.CTkFrame(
            tela,
            fg_color= self.marrom,
            border_width= 3,
            border_color= self.preto,
        )
        self.icone_imagem = ctk.CTkImage(
            light_image= self.ImagemOrigem,
            dark_image= self.ImagemOrigem,
            size=(139, 139)
        )
        self.label_imagem = ctk.CTkLabel(
            self.painel,
            text="",
            image=self.icone_imagem,
            fg_color=self.marrom
        )
        self.label_imagem.bind("<Button-1>", self.AbrirGIT)
        self.label_imagem.configure(cursor="hand2")
        pass
    def __clicaveis(self):
        tela = self.painel

        self.btIniciar = ctk.CTkButton(
            tela,
            text= "Iniciar",
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.FUNC_Iniciar
        )
        self.btBots = ctk.CTkButton(
            tela,
            text= "BOTs",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.FUNC_bot
        )
        self.btDemandas = ctk.CTkButton(
            tela,
            text= "Tarefas dia",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.FUNC_demandas
        )
        self.btConfig = ctk.CTkButton(
            tela,
            text= "Configuração",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.FUNC_config
        )
        pass
    def __localizador(self):
        self.pipelines.place(rely=0.02, relx=0.01, relwidth=0.79, relheight=0.40)
        self.contador.place(rely=0.44, relx=0.01, relwidth=0.79, relheight=0.10)
        self.logArquivo.place(rely=0.56, relx=0.01, relwidth=0.79, relheight=0.43)
        self.painel.place(rely=0.02, relx=0.81, relwidth=0.18, relheight=0.97)

        # Painel dos Botões (posicionados dentro do self.painel)
        self.btIniciar.place(rely=0.04, relx=0.04, relwidth=0.92, relheight=0.08)
        self.btBots.place(rely=0.14, relx=0.04, relwidth=0.92, relheight=0.08)
        self.btDemandas.place(rely=0.24, relx=0.04, relwidth=0.92, relheight=0.08)        
        self.btConfig.place(rely=0.34, relx=0.04, relwidth=0.92, relheight=0.08)

        self.label_imagem.place(rely=0.74, relx=0.02, relwidth=0.96, relheight=0.25)
        pass

if __name__ == '__main__':
    Main()