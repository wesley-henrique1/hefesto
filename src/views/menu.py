import customtkinter as ctk
import sys
import os

# Adiciona a pasta 'src' ao caminho do Python para permitir testes isolados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# A partir daqui, as importações funcionam normalmente
from views.crud_gui import CRUD_
from lib.modErros import ModularErros

validador = ModularErros(fonte= "MENU")
class  auxiliares:
    def _LimparWidget(self,tesk, listBT= list):
        try:
            for button in listBT:
                button.configure(state= tesk)
            for widget in self.telaAlterar.winfo_children():
                widget.destroy()
            self.telaAlterar.configure(fg_color= self.branco)
        except Exception as e:
            validador.registrar_log(e, "_LimparWidget")
    def _desmarcar(self, listbox= list, listBT= list):
        try:
            self._LimparWidget(listBT= listBT, tesk= 'disabled')

            for widget in self.telaAlterar.winfo_children():
                widget.destroy()
            self.telaAlterar.configure(fg_color= self.branco)

            for box in listbox:
                box.deselect()
        except Exception as e:
            validador.registrar_log(e, "_desmarcar")
    def _destroyer(self, telas: ctk.CTkLabel):
        try:
            for widget in telas.winfo_children():
                widget.destroy()
        except Exception as e:
            validador.registrar_log(e, "_destroyer")
    def _limitar_tamanho(self, texto, limite):
        return len(texto) <= limite
    
    def _centerConsulta(self):
        try:
            valor_atual = self.radioVar.get()
            match valor_atual:
                case "MOD":
                    self.modulo.Consultas(telas=self.telaAlterar)
                case "BOT":
                    self.bots.Consultas(telas=self.telaAlterar)
                case "TESK":
                    self.tesk.Consultas(telas=self.telaAlterar)
                case "ROTAS":
                    self.rota.Consultas(telas=self.telaAlterar)

                case _:
                    print("Desconhecido")
        except Exception as e:
            validador.registrar_log(e, "_centerConsulta")
    def _centerEditar(self):
        try:
            valor_atual = self.radioVar.get()
            match valor_atual:
                case "MOD":
                    self.modulo.Editar(telas=self.telaAlterar)
                case "BOT":
                    self.bots.Editar(telas=self.telaAlterar)
                case "TESK":
                    self.tesk.Editar(telas=self.telaAlterar)
                case "ROTAS":
                    self.rota.Editar(telas=self.telaAlterar)

                case _:
                    print("Desconhecido")
        except Exception as e:
            validador.registrar_log(e, "_centerEditar")
    def _centerCadastrar(self):
        try:
            valor_atual = self.radioVar.get()
            match valor_atual:
                case "MOD":
                    self.modulo.Cadastrar(telas=self.telaAlterar)
                case "BOT":
                    self.bots.Cadastrar(telas=self.telaAlterar)
                case "TESK":
                    self.tesk.Cadastrar(telas=self.telaAlterar)
                case "ROTAS":
                    self.rota.Cadastrar(telas=self.telaAlterar)

                case _:
                    print("Desconhecido")
        except Exception as e:
            validador.registrar_log(e, "_centerCadastrar")
    def _centerApagar(self):
        try:
            valor_atual = self.radioVar.get()
            match valor_atual:
                case "MOD":
                    self.modulo.Apagar(telas=self.telaAlterar)
                case "BOT":
                    self.bots.Apagar(telas=self.telaAlterar)
                case "TESK":
                    self.tesk.Apagar(telas=self.telaAlterar)
                case "ROTAS":
                    self.rota.Apagar(telas=self.telaAlterar)
                case _:
                    print("Desconhecido")
        except Exception as e:
            validador.registrar_log(e, "_centerCadastrar")

class Menu(auxiliares):
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"

        root = ctk.CTk()
        root.title("CONFIGURAR")
        root.geometry("572x400")
        root.configure(fg_color=self.marromClaro)
        # root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)
        self.radioVar = ctk.StringVar(value= "COMANDOS")
        
        self.modulo = CRUD_(base= "modulos")
        self.bots = CRUD_(base= "bots")
        self.tesk = CRUD_(base= "task")
        self.rota = CRUD_(base= "rota")
        self.__componentes(root)
        self.__clicaveis()
        self.__BoxFlegs()

        self.buttonList = [self.btApagar, self.btCadastrar, self.btEditar, self.btconsulta]
        self.boxList = [self.boxModulo, self.boxBots, self.boxTarefas]

        self.__localizador()

        root.mainloop()
        pass

    def __componentes(self, tela):
        self.telasFlegs = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        self.telaAlterar = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )

        pass
    def __clicaveis(self):
        self.btconsulta = ctk.CTkButton(
            self.telasFlegs,
            text= "Consultar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._centerConsulta
        )
        self.btEditar = ctk.CTkButton(
            self.telasFlegs,
            text= "Editar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._centerEditar
        )
        self.btCadastrar = ctk.CTkButton(
            self.telasFlegs,
            text= "Cadastrar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._centerCadastrar
        )
        self.btApagar = ctk.CTkButton(
            self.telasFlegs,
            text= "Apagar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._centerApagar
        )
        self.btDesmarcar = ctk.CTkButton(
            self.telasFlegs,
            text= "Desmarcar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._desmarcar(listbox= self.boxList, listBT= self.buttonList)
        )
        pass
    def __BoxFlegs(self):
        self.boxModulo = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "Modulos",
            value= "MOD",
            variable= self.radioVar,
            text_color= self.preto,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._LimparWidget(listBT= self.buttonList, tesk= 'normal'),
        )
        self.boxBots = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "bots",
            value= "BOT",
            variable= self.radioVar,
            text_color= self.preto,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._LimparWidget(listBT= self.buttonList, tesk= 'normal'),
        )
        self.boxTarefas = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "tarefas",
            value= "TESK",
            variable= self.radioVar,
            text_color= self.preto,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._LimparWidget(listBT= self.buttonList, tesk= 'normal'),
        )
        self.boxRotasdf = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "Rotas dados",
            value= "ROTAS",
            variable= self.radioVar,
            text_color= self.preto,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._LimparWidget(listBT= self.buttonList, tesk= 'normal'),
        )
        pass
    def __localizador(self):
        # Localização dos componentes principais
        self.telasFlegs.place_configure(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.36)
        self.telaAlterar.place_configure(relx= 0.02, rely= 0.40, relwidth=0.96, relheight=0.58)

        # Localização dos botão
        self.btconsulta.place_configure(relx= 0.02, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btEditar.place_configure(relx= 0.26, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btCadastrar.place_configure(relx= 0.51, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btApagar.place_configure(relx= 0.76, rely= 0.05, relwidth= 0.22, relheight= 0.24)

        # Localização das caixa de marcação
        self.boxModulo.place_configure(relx= 0.02, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.boxBots.place_configure(relx= 0.27, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.boxTarefas.place_configure(relx= 0.52, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.boxRotasdf.place_configure(relx= 0.77, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.btDesmarcar.place_configure(relx= 0.01, rely= 0.75, relwidth= 0.22, relheight= 0.20)
        pass

if __name__ == "__main__":
    Menu()