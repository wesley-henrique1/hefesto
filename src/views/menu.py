import customtkinter as ctk


class Menu:
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


        self.__componentes(root)
        self.__clicaveis(root)
        self.__localizador()

        root.mainloop()
        pass

    def __modulos(self):
        check_var = ctk.StringVar(value=False)

        boxCadastrar = ctk.CTkCheckBox(
            self.telasFlegs,
            text= "Cadastrar",
            # command=  checkbox_event,
            variable= check_var,
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            checkmark_color= self.preto,
            fg_color= self.vermelho,
            hover_color= self.vermelho,
            checkbox_width= 20,
            checkbox_height= 20,
            onvalue= True,
            offvalue= False
        )
        boxEditar = ctk.CTkCheckBox(
            self.telasFlegs,
            text= "Editar",
            # command=  checkbox_event,
            variable= check_var,
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            checkmark_color= self.preto,
            fg_color= self.vermelho,
            hover_color= self.vermelho,
            checkbox_width= 20,
            checkbox_height= 20,
            onvalue= True,
            offvalue= False
        )
        boxCosultar = ctk.CTkCheckBox(
            self.telasFlegs,
            text= "Consultar",
            # command=  checkbox_event,
            variable= check_var,
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            checkmark_color= self.preto,
            fg_color= self.vermelho,
            hover_color= self.vermelho,
            checkbox_width= 20,
            checkbox_height= 20,
            onvalue= True,
            offvalue= False
        )
        boxApagar = ctk.CTkCheckBox(
            self.telasFlegs,
            text= "Apagar",
            # command=  checkbox_event,
            variable= check_var,
            font= (self.familia, 14, 'bold'),
            text_color= self.preto,
            checkmark_color= self.preto,
            fg_color= self.vermelho,
            hover_color= self.vermelho,
            checkbox_width= 20,
            checkbox_height= 20,
            onvalue= True,
            offvalue= False
        )


        boxCadastrar.place_configure(relx= 0.02, rely= 0.22)
        boxEditar.place_configure(relx= 0.29, rely= 0.22)
        boxCosultar.place_configure(relx= 0.49, rely= 0.22)
        boxApagar.place_configure(relx= 0.74, rely= 0.22)
        pass

    def __componentes(self, tela):
        self.telasFlegs = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
            # corner_radius= 0,

        )
        self.telaAlterar = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        pass
    def __clicaveis(self, tela):
        self.btMod = ctk.CTkButton(
            tela,
            text= "Modulos",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            command= self.__modulos
        )
        self.btBots = ctk.CTkButton(
            tela,
            text= "Bots",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            # command= self.FUNC_bot
        )
        self.btTarefas = ctk.CTkButton(
            tela,
            text= "Tarefas",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            # command= self.FUNC_bot
        )
        self.btAplicar = ctk.CTkButton(
            tela, 
            text= "Aplicar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3

        )
        pass
    def __localizador(self):
        self.btMod.place_configure(relx= 0.02, rely= 0.05, relwidth= 0.20, relheight= 0.15)
        self.btBots.place_configure(relx= 0.27, rely= 0.05, relwidth= 0.20, relheight= 0.15)
        self.btTarefas.place_configure(relx= 0.52, rely= 0.05, relwidth= 0.20, relheight= 0.15)
        self.btAplicar.place_configure(relx= 0.78, rely= 0.05, relwidth= 0.20, relheight= 0.15)

        self.telasFlegs.place_configure(relx= 0.02, rely= 0.24, relwidth= 0.96, relheight= 0.15)
        self.telaAlterar.place_configure(relx= 0.02, rely= 0.40, relwidth=0.96, relheight=0.58)
        pass

if __name__ == "__main__":
    Menu()