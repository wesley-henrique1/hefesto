from src.lib.settings import _Imagens, _Icone
from src.views.menu import Menu
from src.lib.admDB import CRUD_DB
import webbrowser
import customtkinter as ctk
from PIL import Image

class __auxiliares:
    def FUNC_Iniciar(self):
        print("iniciar 3... 2.. 1...")
    def FUNC_Limpar(self):
        print("Limpando...")
    def FUNC_bot(self):
        print("bot 3... 2.. 1...")
    def FUNC_demandas(self):
        print("demandas 3... 2.. 1...")
    def FUNC_config(self):
        Menu()

    def AbrirGIT(self, event=None):
        webbrowser.open("https://github.com/wesley-henrique1")

class Main(__auxiliares):
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"

        root = ctk.CTk()
        root.title("Gerenciador_8000")
        root.geometry("700x500")
        root.configure(fg_color=self.marromClaro)
        root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)

        modulo = CRUD_DB(base= "modulos")
        dicNome = modulo.BuscarVlr()
        self.ListaBox = []

        self.__Componentes(root)
        self.__TelasImgs()
        self.__clicaveis()
        self.__flegsMOD(dicNome)
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
        pass
    def __TelasImgs(self):
        self.logoPy = ctk.CTkImage(
            light_image= Image.open(_Imagens.logoPy),
            dark_image= Image.open(_Imagens.logoPy),
            size= (130, 130)
        )
        self.labelLogo = ctk.CTkLabel(
            self.painel,
            text="",
            image=self.logoPy,
            fg_color=self.marrom,
            corner_radius= 0,
            padx= 0,
            pady= 0
        )

        self.icone_imagem = ctk.CTkImage(
            light_image= Image.open(_Imagens.perfil),
            dark_image= Image.open(_Imagens.perfil),
            size= (140, 140)
        )
        self.labelPerfil = ctk.CTkLabel(
            self.painel,
            text="",
            image=self.icone_imagem,
            fg_color=self.marrom,
            corner_radius= 0,
            padx= 0,
            pady= 0

        )
        self.labelPerfil.bind("<Button-1>", self.AbrirGIT)
        self.labelPerfil.configure(cursor="hand2")

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
        self.btLimpar = ctk.CTkButton(
            tela,
            text= "Limpar",
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.FUNC_Limpar
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

    def __flegsMOD(self, mapa: dict):
        for chave in mapa.keys():
            var_estado = ctk.StringVar(value="0")
            boxNome = ctk.CTkCheckBox(
                self.pipelines,
                text=mapa[chave]['_Nomenclatura'],
                variable=var_estado,
                onvalue= "1",
                offvalue= "0",
                font=(self.familia, 16, 'bold'),
                text_color=self.preto,
                fg_color=self.vermelho,
                hover_color=self.vermelho,
                border_color=self.preto,
            )
            self.ListaBox.append({"checkbox": boxNome, "var": var_estado, "chave": chave})

        pass
    def __localizador(self):
        self.pipelines.place(rely=0.02, relx=0.01, relwidth=0.77, relheight=0.40)
        self.contador.place(rely=0.44, relx=0.01, relwidth=0.77, relheight=0.10)
        self.logArquivo.place(rely=0.56, relx=0.01, relwidth=0.77, relheight=0.43)
        self.painel.place(rely=0.02, relx=0.79, relwidth=0.20, relheight=0.97)

        # Painel dos Pipelanes
        startX = 0.02
        startY = 0.02

        for i, valor in enumerate(self.ListaBox, 1):
            valor['checkbox'].place(rely=startY, relx=startX, relwidth=0.46, relheight=0.12)
            
            startY += 0.14
            
            if i % 6 == 0:
                startX += 0.50
                startY = 0.02

        # Painel dos Botões (posicionados dentro do self.painel)
        self.btIniciar.place(rely=0.02, relx=0.04, relwidth=0.92, relheight=0.08)
        self.btLimpar.place(rely=0.11, relx=0.04, relwidth=0.92, relheight=0.08)
        self.btBots.place(rely=0.20, relx=0.04, relwidth=0.92, relheight=0.08)
        self.btDemandas.place(rely=0.29, relx=0.04, relwidth=0.92, relheight=0.08)        
        self.btConfig.place(rely=0.38, relx=0.04, relwidth=0.92, relheight=0.08)

        self.labelLogo.place(rely=0.48, relx=0.02, relwidth=0.96, relheight=0.25)
        self.labelPerfil.place(rely=0.74, relx=0.02, relwidth=0.96, relheight=0.25)

        pass

if __name__ == '__main__':
    Main()