import json

def executar_passo(self):
    # Pega a fase atual que veio do JSON
    fase_atual = self.dictStatus.get('fase', 0)
    
    if fase_atual < 10:
        # Incrementa o progresso
        self.dictStatus['fase'] = fase_atual + 1
        self.dictStatus['textoUI'] = f"Processando o item {fase_atual + 1} de 10"
        self.dictStatus['boleano'] = True # Continua rodando
        print("Modulo:", self.dictStatus['textoUI'])
    else:
        # Chegou no fim
        self.dictStatus['textoUI'] = "Processamento concluído!"
        self.dictStatus['boleano'] = False # Avisa que terminou
        print("Modulo: Finalizado!")

    # Salva o estado atualizado para a interface ler
    with open(self.caminho, "w", encoding="utf-8") as f:
        json.dump(self.dictStatus, f, ensure_ascii=False, indent=4)

