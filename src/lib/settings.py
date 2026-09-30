from pathlib import Path
import sys
import os

class _Caminho:
    if getattr(sys, 'frozen', False):
        __diretorioBase = Path(sys.executable).parent
    else:
        __diretorioBase = Path(__file__).parent.parent.parent

    PastaBot = __diretorioBase / "bot"
    PastaMod = __diretorioBase / "mod"

    assets = __diretorioBase / "src" / "assets"
    bancoDados = __diretorioBase / "src" / "db"

class _Icone(_Caminho):
    icones = _Caminho.assets / "icon"

    bigorna = icones / "bigorna.ico"
    caixas = icones / "caixas.ico"
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
