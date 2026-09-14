import customtkinter as ctk
import json
from pathlib import Path
from tkinter import messagebox as msg
from typing import Literal

from src.lib.admDB import CRUD_DB, Task_DB, path_DB
from src.lib.modErros import ModularErros

validador = ModularErros(fonte= "GUI - Modulos")
class  auxiliares:
    def _destroyer(self, telas: ctk.CTkLabel):
        telas.configure(fg_color= "#ffffff")
        for widget in telas.winfo_children():
            widget.destroy()
        pass
    def _limitar_tamanho(self, texto, limite):
        return len(texto) <= limite
    def _TextCampo(self):
        msg.showerror("ERRO", f"Erro: Todos os campos de texto devem ser preenchidos!")
        print("Erro: Todos os campos de texto devem ser preenchidos!")

    def _LImpar(self, estado):
        self.entryDesc.configure(state="normal")
        self.entryModulo.configure(state="normal")
        self.entryClasse.configure(state="normal")
        self.boxEstado.configure(state="normal")
        self.btAplicar.configure(state="normal")

        self.entryID.delete(0, 'end')
        self.entryDesc.delete(0, 'end')
        self.entryModulo.delete(0, 'end')
        self.entryClasse.delete(0, 'end')


        estado.set("0")
        pass
    def _Pesquisar(self, Mapa, estado):
        if self.etapa == "Apagar":
            self.entryDesc.configure(state="normal")
            self.entryModulo.configure(state="normal")
            self.entryClasse.configure(state="normal")
            self.boxEstado.configure(state="normal")

        chave = self.entryID.get()
        if chave not in Mapa.keys():
            self.entryDesc.insert(0, "Codigo não encotrado")
            self.entryModulo.delete(0, 'end')
            self.entryClasse.delete(0, 'end')

            print(f"Chave '{chave}' não encontrada.")
            return
        
        if self.base == 'task':
            self.entryDesc.delete(0, 'end')
            self.entryDesc.insert(0, Mapa[chave]["NOME"])

            self.entryModulo.delete(0, 'end')
            self.entryModulo.insert(0, Mapa[chave]["DIAS"])

            estado.set(Mapa[chave]["ESTADO"])
            self.boxEstado.configure(state="normal")
            self.entryClasse.configure(state="disabled")
            pass
        elif self.base == 'rota':
            self.entryDesc.delete(0, 'end')
            valor = Path(Mapa[chave]["PATH"])
            self.entryDesc.insert(0, valor.name)
            self.entryModulo.delete(0, 'end')
            calor = Mapa[chave]["VARIAVEL"]
            self.entryModulo.insert(0, calor)
            estado.set(Mapa[chave]["ESTADO"])
            
            self.boxEstado.configure(state="normal")
            self.entryClasse.configure(state="disabled")

        else:
            self.entryDesc.delete(0, 'end')
            self.entryDesc.insert(0, Mapa[chave]["_Nomenclatura"])

            self.entryModulo.delete(0, 'end')
            self.entryModulo.insert(0, Mapa[chave]["_Modulo"])

            self.entryClasse.delete(0, 'end')
            self.entryClasse.insert(0, Mapa[chave]["_classes"])

            estado.set(Mapa[chave]["_estado"])
            self.boxEstado.configure(state="normal")
        if self.etapa == "Apagar":
            self.entryDesc.configure(state="disabled")
            self.entryModulo.configure(state="disabled")
            self.entryClasse.configure(state="disabled")
            self.boxEstado.configure(state="disabled")

        pass
    pass
class CRUD_(auxiliares):
    def __init__(self, base= Literal["modulos", "bots", "task", "rota"]):
        self.etapa = None

        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"

        self.base = base
        self.ancoraDB = CRUD_DB(base= base)
        self.ancoraTesk = Task_DB()
        self.ancoraRota = path_DB()
        
        self.meu_estado_var = ctk.StringVar(value= "0")
        pass

    def __Contructor(self, telas, Mapa):
        if self.base == 'task':
            desc = "Tarefa"
            mod = "Dias [EX: 2,5]"
            valor = "disabled"
            limite = 22
        elif self.base == 'rota':
            desc = "Path"
            mod = "Variavel"
            valor = "disabled"
            limite = 10000
        else:
            desc = "Nomeclatura"
            mod = "Modulo"
            valor = "normal"
            limite = 22

        self.entryID = ctk.CTkEntry(
            telas,
            placeholder_text= "Codigo",
            font= (self.familia, 16, 'bold'),
            border_width= 3,
            text_color= self.vermelho,
            border_color= self.preto,
            fg_color= self.branco,
            validate='key',
            validatecommand= (telas.register(lambda texto: self._limitar_tamanho(texto, 7)), '%P')
        )
        self.entryDesc = ctk.CTkEntry(
            telas,
            placeholder_text= desc,
            font= (self.familia, 16, 'bold'),
            border_width= 3,
            text_color= self.vermelho,
            border_color= self.preto,
            fg_color= self.branco,
            validate='key',
            validatecommand= (telas.register(lambda texto: self._limitar_tamanho(texto, limite)), '%P')
        )
        self.entryModulo = ctk.CTkEntry(
            telas,
            placeholder_text= mod,
            font= (self.familia, 16, 'bold'),
            border_width= 3,
            text_color= self.vermelho,
            border_color= self.preto,
            fg_color= self.branco,
            validate='key',
            validatecommand= (telas.register(lambda texto: self._limitar_tamanho(texto, 14)), '%P')
        )
        self.entryClasse = ctk.CTkEntry(
            telas,
            placeholder_text= "Classe",
            font= (self.familia, 16, 'bold'),
            border_width= 3,
            text_color= self.vermelho,
            border_color= self.preto,
            fg_color= self.branco,
            validate='key',
            state= valor,
            validatecommand= (telas.register(lambda texto: self._limitar_tamanho(texto, 14)), '%P')
            )
        self.boxEstado = ctk.CTkCheckBox(
            telas,
            text="Estado do Módulo",
            variable=self.meu_estado_var,
            onvalue= "1",
            offvalue= "0",
            font=(self.familia, 16, 'bold'),
            text_color=self.vermelho,
            fg_color=self.marrom,
            hover_color=self.marromClaro,
            border_color=self.preto,
        )

        self.btPesquisar = ctk.CTkButton(
            telas,
            text= "Pesquisar",
            font= (self.familia, 16, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._Pesquisar(Mapa, self.meu_estado_var)
        )
        self.btAplicar = ctk.CTkButton(
            telas,
            text= "Aplicar",
            font= (self.familia, 16, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._Aplicar(self.etapa)
        )
        self.btLimpar = ctk.CTkButton(
            telas,
            text= "Limpar",
            font= (self.familia, 16, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._LImpar(self.meu_estado_var)
        )

        # Locaziador dos componentes
        self.entryID.place_configure(relx= 0.02, rely= 0.04, relheight= 0.20, relwidth= 0.24)
        self.entryDesc.place_configure(relx= 0.28, rely= 0.04, relheight= 0.20, relwidth= 0.70)
        self.entryModulo.place_configure(relx= 0.02, rely= 0.28, relheight= 0.20, relwidth= 0.30)
        self.entryClasse.place_configure(relx= 0.34, rely= 0.28, relheight= 0.20, relwidth= 0.30)
        self.boxEstado.place_configure(relx= 0.02, rely= 0.50, relheight= 0.20, relwidth= 0.40)

        self.btPesquisar.place_configure(relx= 0.02, rely= 0.70, relheight= 0.20, relwidth= 0.25)
        self.btAplicar.place_configure(relx= 0.29, rely= 0.70, relheight= 0.20, relwidth= 0.25)
        self.btLimpar.place_configure(relx= 0.56, rely= 0.70, relheight= 0.20, relwidth= 0.25)

        pass
    def _Aplicar(self, contrato: Literal["cadastrar", "editar", "Apagar"]):
        try:
            chave = self.entryID.get().strip()

            if not chave:
                msg.showwarning("AVISO", "O campo ID (chave)  é obrigatório!")
                print("Erro: O campo ID (Chave) é obrigatório!")
                return
            match contrato:
                case "Apagar":
                    if self.base == 'task':
                        valor = self.ancoraTesk.DeletarVlr((chave,))
                    elif self.base == 'rota':
                        valor = self.ancoraRota.DeletarVlr((chave,))
                    else:
                        valor = self.ancoraDB.DeletarVlr((chave,))
                    if valor:
                        msg.showinfo("FEITO", f"Registro '{chave}' apagado com sucesso!")
                        print(f"Registro '{chave}' apagado com sucesso!")
                    else:
                        msg.showerror("Erro", f"Registro '{chave}' não foi encontrado na base de dados.")
                        print(f"Aviso: Tentativa de apagar a chave '{chave}', mas ela não existe.")       
                case "cadastrar" | "editar":
                    if self.base == 'task':
                        self.entryClasse.configure(state="disabled")

                        nome = self.entryDesc.get().strip()
                        estado = self.boxEstado.get()

                        texto_usuario = self.entryModulo.get().strip()
                        dias_lista = [int(dia.strip()) for dia in texto_usuario.split(",") if dia.strip()]
                        dias = json.dumps(dias_lista)

                        if not nome or not dias:
                            self._TextCampo()
                            return
                        
                        if contrato == "cadastrar":
                            self.ancoraTesk.InserirVle((chave, nome, dias, estado,))
                            msg.showinfo("FEITO", f"Registro '{chave}' cadastrado com sucesso!")
                            print(f"Registro '{chave}' cadastrado com sucesso!")
                        
                        elif contrato == "editar":
                            self.ancoraTesk.EditarVlr((nome, dias, estado, chave,))
                            msg.showinfo("FEITO", f"Registro '{chave}' atualizado com sucesso!")
                            print(f"Registro '{chave}' atualizado com sucesso!")
                        pass
                    elif self.base == 'rota':
                        self.entryClasse.configure(state="disabled")
                        path = self.entryDesc.get().strip()
                        var = self.entryModulo.get()
                        estado = self.boxEstado.get()
                        if not path or not var:
                            self._TextCampo()
                            return
                        if contrato == "cadastrar":
                            self.ancoraRota.InserirVle((chave, var, path, estado,))
                            msg.showinfo("FEITO", f"Registro '{chave}' cadastrado com sucesso!")
                            print(f"Registro '{chave}' cadastrado com sucesso!")
                        
                        elif contrato == "editar":
                            self.ancoraRota.EditarVlr((var, path, estado, chave,))
                            msg.showinfo("FEITO", f"Registro '{chave}' atualizado com sucesso!")
                            print(f"Registro '{chave}' atualizado com sucesso!")
                        pass
                    else: 
                        nome = self.entryDesc.get().strip()
                        modulo = self.entryModulo.get().strip()
                        clase = self.entryClasse.get().strip()
                        estado = self.boxEstado.get()

                        if not nome or not modulo or not clase:
                            self._TextCampo()
                            return
                        
                        if contrato == "cadastrar":
                            self.ancoraDB.InserirVle((chave, nome, modulo, clase, estado,))
                            msg.showinfo("FEITO", f"Registro '{chave}' cadastrado com sucesso!")
                            print(f"Registro '{chave}' cadastrado com sucesso!")
                        
                        elif contrato == "editar":
                            self.ancoraDB.EditarVlr((nome, modulo, clase, estado, chave,))
                            msg.showinfo("FEITO", f"Registro '{chave}' atualizado com sucesso!")
                            print(f"Registro '{chave}' atualizado com sucesso!")

            self.entryID.delete(0, "end")
            self.entryDesc.delete(0, "end")
            self.entryModulo.delete(0, 'end')
            self.entryClasse.delete(0, 'end')
            self.meu_estado_var.set("0")
        except Exception as e:
            validador.registrar_log(e, "_Aplicar")

    def Consultas(self, telas: ctk.CTkLabel):
        self._destroyer(telas)
        telas.configure(fg_color= self.marromClaro)
        try:
            if self.base == 'task':
                mapa = self.ancoraTesk.BuscarVlr()
                on = []
                off = []
                coluna = f"{'CHAVE':^7} | {'Tarefa':^30} | {'dias':^14} | {'Estado':^6}\n"
                separador = "-" * 75
                tabela = coluna + separador + "\n"
                if mapa:
                    for chave in mapa.keys():
                        linha = f"{chave:<7} | {mapa[chave]['NOME']:<30} | {mapa[chave]['DIAS']:<14} | {mapa[chave]['ESTADO']:^6}\n"
                        if mapa[chave]['ESTADO'] == '1':
                            on.append(mapa[chave]['ESTADO'])
                        elif mapa[chave]['ESTADO'] == '0':
                            off.append(mapa[chave]['ESTADO'])
                        tabela += linha
                else:
                    linha = f"{'TASK000':<7} | {'BASE VAZIA':<30} | {'SEM REGISTRO':<14}| {'-':^6}\n"
                    tabela += linha 
            elif self.base == 'rota':
                mapa = self.ancoraRota.BuscarVlr()
                on = []
                off = []
                coluna = f"{'CHAVE':^7} | {'PATH':^30} | {'VARIAVEL':^14} | {'Estado':^6}\n"
                separador = "-" * 75
                tabela = coluna + separador + "\n"
                if mapa:
                    for chave in mapa.keys():
                        path = mapa[chave]['PATH']
                        caminho = Path(path)
                        nome = caminho.name
                        path_formatado = f"{nome[:27]}..." if len(nome) > 30 else f"{nome:<30}"
                        linha = f"{chave:<7} | {path_formatado:<30} | {mapa[chave]['VARIAVEL']:<14} | {mapa[chave]['ESTADO']:^6}\n"
                        if mapa[chave]['ESTADO'] == '1':
                            on.append(mapa[chave]['ESTADO'])
                        elif mapa[chave]['ESTADO'] == '0':
                            off.append(mapa[chave]['ESTADO'])
                        tabela += linha
                else:
                    linha = f"{'TASK000':<7} | {'BASE VAZIA':<30} | {'SEM REGISTRO':<14}| {'-':^6}\n"
                    tabela += linha 
            else:
                mapa = self.ancoraDB.BuscarVlr()
                on = []
                off = []
                coluna = f"{'CHAVE':^7} | {'Nomenclatura':^22} | {'Modulo':^14} | {'Classe':^14} | {'Estado':^6}\n"
                separador = "-" * 75
                tabela = coluna + separador + "\n"
                if mapa:
                    for chave in mapa.keys():
                        linha = f"{chave:<7} | {mapa[chave]['_Nomenclatura']:<22} | {mapa[chave]['_Modulo']:<14} | {mapa[chave]['_classes']:<14} | {mapa[chave]['_estado']:^6}\n"
                        if mapa[chave]['_estado'] == '1':
                            on.append(mapa[chave]['_estado'])
                        elif mapa[chave]['_estado'] == '0':
                            off.append(mapa[chave]['_estado'])
                        tabela += linha
                else:
                    linha = f"{'MOD_000':<7} | {'BASE VAZIA':<22} | {'SEM REGISTRO':<14} | {'-':<14} | {'-':^6}\n"
                    tabela += linha 

            total = len(mapa)
            self.logMOD = ctk.CTkTextbox(
                telas,
                fg_color= self.branco,
                font= (self.familia, 12),

                border_color= self.preto,
                text_color= self.preto,
                border_width= 2,
                border_spacing= 1,
                state= 'normal'
            )
            self.labelVlr = ctk.CTkLabel(
                telas,
                text= f"Registrados: {total} | Ativos: {len(on)} | Desativados: {len(off)}",
                fg_color= self.branco,
                border_width= 2,
                border_color= self.preto,
                font=(self.familia, 16),
                text_color= self.preto,
                anchor= "center",
            )
            self.logMOD.insert("0.0", tabela)
            self.logMOD.configure(state='disabled')
            self.logMOD.place_configure(relx= 0.0, rely= 0.0, relheight= 0.89, relwidth= 1)
            self.labelVlr.place_configure(relx= 0.0, rely= 0.88, relheight= 0.12, relwidth= 1)
        except Exception as e:
            validador.registrar_log(e, "Consultas")
        pass
    def Editar(self, telas: ctk.CTkLabel):
        try:
            self.etapa = "editar"
            if self.base == 'task':
                mapa = self.ancoraTesk.BuscarVlr()
            elif self.base == 'rota':
                mapa = self.ancoraRota.BuscarVlr()
            else:
                mapa = self.ancoraDB.BuscarVlr()

            self._destroyer(telas)
            self.__Contructor(telas, mapa)
        except Exception as e:
            validador.registrar_log(e, "Editar")
        pass
    def Cadastrar(self, telas: ctk.CTkLabel):
        try:
            self.etapa = "cadastrar"
            if self.base == 'task':
                mapa = self.ancoraTesk.BuscarVlr()
            elif self.base == 'rota':
                mapa = self.ancoraRota.BuscarVlr()
            else:
                mapa = self.ancoraDB.BuscarVlr()

            lista = []

            self._destroyer(telas)
            self.__Contructor(telas, mapa)
            for chave in mapa.keys():
                valor = chave.split("_")
                vlInt = int(valor[1])
                lista.append(vlInt)
            if lista:
                maior = max(lista)
            else:
                maior = 0

            match self.base:
                case "modulos":
                    keys = "MOD_"
                case "bots": 
                    keys = "BOT_"
                case "task":
                    keys = "TAR_"
                case "rota":
                    keys = "ARQ_"

            self.entryID.insert(0, f"{keys}{maior+1:03d}")
            self.entryID.configure(state="disabled")
            self.btPesquisar.configure(state='disabled')
        except Exception as e:
            validador.registrar_log(e, "Cadastrar")

        pass
    def Apagar(self, telas: ctk.CTkLabel):
        try:
            self.etapa = "Apagar"
            if self.base == 'task':
                mapa = self.ancoraTesk.BuscarVlr()
            elif self.base == 'rota':
                mapa = self.ancoraRota.BuscarVlr()
            else:
                mapa = self.ancoraDB.BuscarVlr()

            self._destroyer(telas)
            self.__Contructor(telas, mapa)
            self.entryDesc.configure(state="disabled")
            self.entryModulo.configure(state="disabled")
            self.entryClasse.configure(state="disabled")
            self.boxEstado.configure(state="disabled")
        except Exception as e:
            validador.registrar_log(e, "Apagar")
