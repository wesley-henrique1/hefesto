import customtkinter as ctk
from tkinter import messagebox as msg
from typing import Literal

from lib.admDB import CRUD_DB
from lib.modErros import ModularErros

validador = ModularErros(fonte= "GUI - Modulos")
class  auxiliares:
    def _destroyer(self, telas: ctk.CTkLabel):
        telas.configure(fg_color= "#ffffff")
        for widget in telas.winfo_children():
            widget.destroy()
        pass
    def _limitar_tamanho(self, texto, limite):
        return len(texto) <= limite

    def _LImpar(self, estado):
        self.entryID.delete(0, 'end')
        self.entryDesc.delete(0, 'end')
        self.entryModulo.delete(0, 'end')
        self.entryClasse.delete(0, 'end')

        self.entryDesc.configure(state="normal")
        self.entryModulo.configure(state="normal")
        self.entryClasse.configure(state="normal")
        self.boxEstado.configure(state="normal")
        self.btAplicar.configure(state="normal")

        estado.set("0")
        pass
    def _Pesquisar(self, Mapa, estado):
        chave = self.entryID.get()
        if chave not in Mapa.keys():
            self.entryDesc.insert(0, "Codigo não encotrado")
            self.entryModulo.delete(0, 'end')
            self.entryClasse.delete(0, 'end')

            print(f"Chave '{chave}' não encontrada.")
            return
        
        self.entryDesc.delete(0, 'end')
        self.entryDesc.insert(0, Mapa[chave]["_Nomenclatura"])

        self.entryModulo.delete(0, 'end')
        self.entryModulo.insert(0, Mapa[chave]["_Modulo"])

        self.entryClasse.delete(0, 'end')
        self.entryClasse.insert(0, Mapa[chave]["_classes"])

        estado.set(Mapa[chave]["_estado"])
        self.boxEstado.configure(state="normal")
        pass
    pass
class CRUD_(auxiliares):
    def __init__(self, base= Literal["modulos", "bots"]):
        self.etapa = None
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"

        self.ancoraDB = CRUD_DB(base= base)
        
        self.meu_estado_var = ctk.StringVar(value= "0")
        pass

    def __Contructor(self, telas, Mapa):
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
            placeholder_text= "Nomeclatura",
            font= (self.familia, 16, 'bold'),
            border_width= 3,
            text_color= self.vermelho,
            border_color= self.preto,
            fg_color= self.branco,
            validate='key',
            validatecommand= (telas.register(lambda texto: self._limitar_tamanho(texto, 22)), '%P')
        )
        self.entryModulo = ctk.CTkEntry(
            telas,
            placeholder_text= "Modulo",
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
        self.entryDesc.place_configure(relx= 0.28, rely= 0.04, relheight= 0.20, relwidth= 0.60)
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
                    valor = self.ancoraDB.DeletarVlr((chave,))
                    if valor:
                        msg.showinfo("FEITO", f"Registro '{chave}' apagado com sucesso!")
                        print(f"Registro '{chave}' apagado com sucesso!")
                    else:
                        msg.showerror("Erro", f"Registro '{chave}' não foi encontrado na base de dados.")
                        print(f"Aviso: Tentativa de apagar a chave '{chave}', mas ela não existe.")
                        
                case "cadastrar" | "editar":
                    nome = self.entryDesc.get().strip()
                    modulo = self.entryModulo.get().strip()
                    clase = self.entryClasse.get().strip()
                    estado = self.boxEstado.get()

                    if not nome or not modulo or not clase:
                        msg.showerror("ERRO", f"Erro: Todos os campos de texto devem ser preenchidos!")
                        print("Erro: Todos os campos de texto devem ser preenchidos!")
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
            validador.registrar_log(e, "Consultas")

    def Consultas(self, telas: ctk.CTkLabel):
        try:
            self._destroyer(telas)
            telas.configure(fg_color= self.marromClaro)
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
            mapa = self.ancoraDB.BuscarVlr()
            self._destroyer(telas)
            self.__Contructor(telas, mapa)
        except Exception as e:
            validador.registrar_log(e, "Editar")
        pass
    def Cadastrar(self, telas: ctk.CTkLabel):
        try:
            self.etapa = "cadastrar"
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
            self.entryID.insert(0, f"MOD_{maior+1:03d}")
            self.entryID.configure(state="disabled")
            self.btPesquisar.configure(state='disabled')
        except Exception as e:
            validador.registrar_log(e, "Cadastrar")

        pass
    def Apagar(self, telas: ctk.CTkLabel):
        try:
            self.etapa = "Apagar"
            mapa = self.ancoraDB.BuscarVlr()

            self._destroyer(telas)
            self.__Contructor(telas, mapa)
            self.entryDesc.configure(state="disabled")
            self.entryModulo.configure(state="disabled")
            self.entryClasse.configure(state="disabled")
            self.boxEstado.configure(state="disabled")
        except Exception as e:
            validador.registrar_log(e, "Apagar")
