from src.lib import settings
import customtkinter as ctk
from pathlib import Path
import math
import os

class outputUI:
    def __init__(self, listPath):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"
        self._Icone = settings._Icone()

        root = ctk.CTkToplevel()
        root.title("Saidas Resultados")
        root.geometry("550x300")
        root.configure(fg_color=self.marromClaro)
        root.iconbitmap(self._Icone.caixas)
        root.resizable(False, False)

        dictSaida = self.__Processar(listPath)
        self.__Componentes(dictSaida, root)
        self.__Clicaveis(root, dictSaida)
        self.__localizador(mapa= dictSaida)
        root.mainloop()
        pass
    
    def FUNC_Iniciar(self, lista_processada):
        marcados = []
        for item in lista_processada:
            if item["estado"].get() == "1":
                marcados.append(item["NomeArquivo"])
                os.startfile(item['Paths'])
        pass
    def __Processar(self, listPath: list):
        retorno = []
        validar = set()
        for index in listPath:
            var_estado = ctk.StringVar(value="0")
            index = Path(index)
            nome = index.name

            if nome in validar:
                continue
            validar.add(nome)
            dictvalor = {
                "checkbox": int,
                "NomeArquivo": nome,
                "Paths": index,
                "estado": var_estado
            }
            retorno.append(dictvalor)
        return retorno

    def __Componentes(self, mapa: list, tela: ctk.CTk):
        self.quadro = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        for valor in mapa:
            for registro in valor.keys():
                boxNome = ctk.CTkCheckBox(
                    self.quadro,
                    text=valor['NomeArquivo'],
                    variable=valor['estado'],
                    onvalue= "1",
                    offvalue= "0",
                    font=(self.familia, 16, 'bold'),
                    text_color=self.preto,
                    fg_color=self.vermelho,
                    hover_color=self.vermelho,
                    border_color=self.preto,
                )
                valor['checkbox'] = boxNome

        pass
    def __Clicaveis(self, telas, valores):
        self.BtInicar = ctk.CTkButton(
            telas, 
            text= "Abrir Arquivo(s) desejado(s)",
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self.FUNC_Iniciar(valores)
        )
        pass
    def __localizador(self, mapa):
        self.BtInicar.place(relx=0.5, rely=0.99, anchor="s", relwidth=0.98, relheight=0.15)
        self.quadro.place_configure(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.82)
        startX = 0.02
        startY = 0.02
        total = len(mapa)

        limite_primeira_coluna = math.ceil(total / 2)

        for index, dicionario in enumerate(mapa):
                dicionario['checkbox'].place(
                    rely=startY, relx=startX, relwidth=0.46, relheight=0.12
                )
                startY += 0.14
                if (index + 1) == limite_primeira_coluna:
                    startX = 0.52
                    startY = 0.02
