import sys
from pathlib import Path

file_path = Path(__file__).resolve()
src_path = file_path.parents[1]
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

import customtkinter as ctk
from lib.admDB import CRUD_DB
import math
import os
import pandas as pd
class __auxiliares:
    def _LimparWidget(self,tesk, listBT= list):
        try:
            for button in listBT:
                button.configure(state= tesk)
            for widget in self.Retorno.winfo_children():
                widget.destroy()
            self.Retorno.configure(fg_color= self.branco)
        except Exception as e:
            print(e)
            # validador.registrar_log(e, "_LimparWidget")
    def _desmarcar(self, listBT= list):
        try:
            self._LimparWidget(listBT= listBT, tesk= 'disabled')

            for widget in self.Retorno.winfo_children():
                widget.destroy()
            self.Retorno.configure(fg_color= self.branco)

            for dicionario in self.MapaBox:
                for registro in dicionario.keys():
                    dicionario[registro]['checkbox'].deselect()
        except Exception as e:
            print(e)
            # validador.registrar_log(e, "_desmarcar")
    
    def CapturarFile(self):
        nomeFile = 'ProvisorioFile.xlsx'
        pasta_script = os.path.dirname(os.path.abspath(__file__))

        nomeBOT= ""
        return os.path.join(pasta_script, nomeFile)
    def AbrirFile(self):
        caminho = self.CapturarFile()
        if os.path.exists(caminho):
            os.startfile(caminho)
        else:
            etapas = {
                'transferencia': ["CODPROD"],
                "Retirada": ['CODPROD', 'DTULTENT', 'QTESTGER', 'OBSFL'],
                'transf3707': ["CODPROD", "DESTINO"],
                'Etapa_3': ["CODPROD", "PL_LASTRO", "PL", "CAP", "QTEnd", "V_CAP"],
                'adiconarPK': ["CODPROD", "DESTINO", 'CAPACIDADE', 'PONTO_REP']
            }

            with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
                for nome_aba, colunas in etapas.items():
                    pd.DataFrame(columns=colunas).to_excel(writer, sheet_name=nome_aba, index=False)
            os.startfile(caminho)  

class BotsUI(__auxiliares):
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"


        root = ctk.CTk()
        root.title("AUTOMAÇÃO")
        root.geometry("440x300")
        root.configure(fg_color=self.marromClaro)
        # root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)

        modulo = CRUD_DB(base= "bots")
        dicNome = modulo.BuscarVlr()
        self.MapaBox = []

        radioVar = ctk.StringVar(value= "COMANDOS") 
        for chave in dicNome.keys():
            if  dicNome[chave]['_estado'] == '0':
                    continue
            self.MapaBox.append(
                {chave:{
                    "checkbox": int, 
                    "__estado__": radioVar, 
                    '_Nomenclatura': dicNome[chave]['_Nomenclatura']
                    }
                }
            )

        self.__Componentes(root)
        self.__flegsUnicos()
        self.__clicaveis()
        self.buttonList = [self.btIniciar]

        self.__localizador()

        root.mainloop()
        pass

    def __Componentes(self, tela):
        self.Painel = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        self.Retorno = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        pass
    def __flegsUnicos(self):
        for valor in self.MapaBox:
            for registro in valor.keys():
                boxModulo = ctk.CTkRadioButton(
                    self.Painel,
                    text= valor[registro]['_Nomenclatura'],
                    value= registro,
                    variable= valor[registro]['__estado__'],

                    text_color= self.preto,
                    hover_color= self.vermelho,
                    fg_color= self.vermelho,
                    border_color= self.preto,

                    command= lambda: self._LimparWidget(listBT= self.buttonList, tesk= 'normal'),
                )
                valor[registro]['checkbox'] = boxModulo

    def __clicaveis(self):
        self.btAbrir = ctk.CTkButton(
            self.Painel,
            text= "Abrir Arquivos",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self.AbrirFile()
        )
        self.btIniciar = ctk.CTkButton(
            self.Painel,
            text= "Iniciar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            # command= self._centerApagar
        )
        self.desmarcar = ctk.CTkButton(
            self.Painel,
            text= "Desmarcar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._desmarcar(listBT= self.buttonList)
        )
        pass
    def __localizador(self):
        self.Painel.place_configure(relx= 0.02, rely= 0.02, relheight= 0.40, relwidth= 0.96)
        self.Retorno.place_configure(relx= 0.02, rely= 0.44, relheight= 0.55, relwidth= 0.96)

        self.btAbrir.place_configure(relx= 0.02, rely= 0.70, relheight= 0.20, relwidth= 0.40)
        self.btIniciar.place_configure(relx= 0.44, rely= 0.70, relheight= 0.20, relwidth= 0.22)
        self.desmarcar.place_configure(relx= 0.68, rely= 0.70, relheight= 0.20, relwidth= 0.22)

        startX = 0.02
        startY = 0.06
        total = len(self.MapaBox)

        limite_coluna = math.ceil(total / 3)

        for index, dicionario in enumerate(self.MapaBox):
            for registro in dicionario.keys():
                
                dicionario[registro]['checkbox'].place(
                    rely=startY, relx=startX, relwidth=0.30, relheight=0.20
                )
                startY += 0.22
                if (index + 1) == limite_coluna:
                    startX = 0.35
                    startY = 0.06 
                elif (index + 1) == limite_coluna * 2:
                    startX = 0.68
                    startY = 0.06       
        pass


if __name__ == "__main__":
    BotsUI()