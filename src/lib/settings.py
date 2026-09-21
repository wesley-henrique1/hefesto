from pathlib import Path

class _Caminho:
    __diretorioAtual = Path(__file__).parent
    PastaBot = __diretorioAtual.parent.parent / "bot"
    PastaMod = __diretorioAtual.parent.parent / "mod"

    assets = __diretorioAtual.parent / "assets"
    bancoDados = __diretorioAtual.parent / "db"

    # lib = _Caminho.diretorioAtual / "lib"
    # views = _Caminho.diretorioAtual / "views"

class _Icone(_Caminho):
    icones = _Caminho.assets / "icon"

    bigorna = icones / "bigorna.ico"
    blocoNotas = icones / "bloco_notas.ico"
    engrenagem = icones / "engrenagem.ico"
    perfil = icones/ "perfil.ico"

    pass
class _Imagens(_Caminho):
    imagem = _Caminho.assets / "img"

    bigorna = imagem / "bigorna.png"
    blocoNotas = imagem / "bloco_notas.png"
    engrenagem = imagem / "engrenagem.png"
    logoPy = imagem / "logo_python.png"
    perfil = imagem / "perfil.png"
    
    pass
class _DataBase(_Caminho):
    dataBase = _Caminho.bancoDados

    errosdb = dataBase / "errosDb.db"

    keys = dataBase / "keysDB.db"
    botdb = dataBase / "botDB.db"
    modDb = dataBase / "modDB.db"
    taskDb = dataBase / "tarefadb.db"
    rotadb = dataBase / "rotasdb.db"
    pass

class _DataJson(_Caminho):
    json = _Caminho.assets / "json"
    rotas = json / "rotas.json"
if __name__ == "__main__":
    ancora = _Caminho()
    _Icone = _Icone()
    _Imagens = _Imagens()
    print(_Caminho)
    print("bigorna:", _Icone.bigorna)
    print("bigorna:", _Imagens.bigorna)
