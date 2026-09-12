import customtkinter as ctk


class  auxiliares:
    def _Liberar(self,tesk, listBT= list):
        for button in listBT:
            button.configure(state= tesk)

        pass
    def _desmarcar(self, listbox= list, listBT= list):
        self._Liberar(listBT= listBT, tesk= 'disabled')
        for box in listbox:
            box.deselect()
        pass

class Modulos:
    def __init__(self):
        self.marrom = "#8a541f"
        self.marromClaro = "#d8a859"
        self.branco = "#ffffff"
        self.preto = "#000000"
        self.vermelho = "#8e3312"
        self.familia = "Consolas"

        self.listdrop = []
        pass
    def Consultas(self, telas: ctk.CTkLabel):
        for widget in telas.winfo_children():
            widget.destroy()
        self.logMOD = ctk.CTkTextbox(
            telas,
            fg_color= self.branco,
            font= (self.familia, 12),

            border_color= self.preto,
            border_width= 3,
            border_spacing= 4,
            state= 'disabled'
        )
        self.listdrop.append(self.logMOD)
        self.logMOD.place_configure(relx= 0.02, rely= 0.04, relheight= 0.92, relwidth= 0.96)
        pass
    def Editar(self):
        pass
    def Cadastrar(self):
        pass
    def Apagar(self):
        pass
    def test(self):
        for fahh in self.listdrop:
            fahh.destroy()

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
        root.geometry("400x300")
        root.configure(fg_color=self.marromClaro)
        # root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)
        self.radioVar = ctk.StringVar(value= "COMANDOS")

        self.__componentes(root)
        self.__clicaveis()
        self.__flegs()
        self.buttonList = [self.btApagar, self.btCadastrar, self.btEditar, self.btconsulta]
        self.boxList = [self.boxModulo, self.boxBots, self.boxTarefas]

        self.__resetar()
        self.__localizador()

        root.mainloop()
        pass
    def __centerConsulta(self):
        valor_atual = self.radioVar.get()
        print(valor_atual)
        match valor_atual:
            case "MOD":
                modulo = Modulos()
                modulo.Consultas(telas=self.telaAlterar)
            case _:
                print("Desconhecido")
        pass
    def __resetar(self):
        valor_atual = self.radioVar.get()
        print(valor_atual)
        match valor_atual:
            case "MOD":
                modulo = Modulos()
                modulo.test()
            case _:
                print("Desconhecido")
        
        self.btDesmarcar = ctk.CTkButton(
            self.telasFlegs,
            text= "Desmarcar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._desmarcar(listbox= self.boxList, listBT= self.buttonList)
        )

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
            fg_color= self.branco,
            border_width= 3,
            command= self.__centerConsulta
        )
        self.btEditar = ctk.CTkButton(
            self.telasFlegs,
            text= "Editar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            # command= self.FUNC_bot
        )
        self.btCadastrar = ctk.CTkButton(
            self.telasFlegs,
            text= "Cadastrar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            # command= self.FUNC_bot
        )
        self.btApagar = ctk.CTkButton(
            self.telasFlegs,
            text= "Apagar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3

        )
        pass
    def __flegs(self):
        
        self.boxModulo = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "Modulos",
            value= "MOD",
            command= lambda: self._Liberar(listBT= self.buttonList, tesk= 'normal'),
            variable= self.radioVar,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
        )
        self.boxBots = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "bots",
            value= "BOT",
            variable= self.radioVar,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._Liberar(listBT= self.buttonList, tesk= 'normal'),

        )
        self.boxTarefas = ctk.CTkRadioButton(
            self.telasFlegs,
            text= "tarefas",
            value= "TESK",
            variable= self.radioVar,
            hover_color= self.vermelho,
            fg_color= self.vermelho,
            border_color= self.preto,
            command= lambda: self._Liberar(listBT= self.buttonList, tesk= 'normal'),
        )
        pass
    def __localizador(self):
        self.telasFlegs.place_configure(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.36)
        self.telaAlterar.place_configure(relx= 0.02, rely= 0.40, relwidth=0.96, relheight=0.58)

        self.btconsulta.place_configure(relx= 0.02, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btEditar.place_configure(relx= 0.26, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btCadastrar.place_configure(relx= 0.51, rely= 0.05, relwidth= 0.22, relheight= 0.24)
        self.btApagar.place_configure(relx= 0.76, rely= 0.05, relwidth= 0.22, relheight= 0.24)

        self.boxModulo.place_configure(relx= 0.02, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.boxBots.place_configure(relx= 0.27, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.boxTarefas.place_configure(relx= 0.52, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        self.btDesmarcar.place_configure(relx= 0.77, rely= 0.50, relwidth= 0.22, relheight= 0.20)
        pass

if __name__ == "__main__":
    Menu()