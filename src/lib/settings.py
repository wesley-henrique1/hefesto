from pathlib import Path
import sys

class _Caminho:
    if getattr(sys, 'frozen', False):
        __diretorioExterno = Path(sys.executable).resolve().parent
        __diretorioInterno = Path(sys._MEIPASS)
    else:
        __diretorioExterno = Path(__file__).resolve().parent.parent.parent
        __diretorioInterno = __diretorioExterno

    _raiz_str = str(__diretorioExterno)
    if _raiz_str not in sys.path:
        sys.path.insert(0, _raiz_str)

    PastaBot = __diretorioExterno / "bot"
    PastaMod = __diretorioExterno / "mod"
    PastaLog = __diretorioExterno / "log"
    bancoDados = __diretorioExterno / "src" / "db"

    assets = __diretorioInterno / "src" / "assets"
    PastaBot.mkdir(parents=True, exist_ok=True)
    PastaMod.mkdir(parents=True, exist_ok=True)
    PastaLog.mkdir(parents=True, exist_ok=True)
    bancoDados.mkdir(parents=True, exist_ok=True)

class _Icone(_Caminho):
    icones = _Caminho.assets / "icon"

    bigorna = icones / "bigorna.ico"
    caixas = icones / "caixas.ico"
    blocoNotas = icones / "bloco_notas.ico"
    engrenagem = icones / "engrenagem.ico"
    perfil = icones / "perfil.ico"

class _Imagens(_Caminho):
    imagem = _Caminho.assets / "img"

    bigorna = imagem / "bigorna.png"
    blocoNotas = imagem / "bloco_notas.png"
    engrenagem = imagem / "engrenagem.png"
    logoPy = imagem / "logo_python.png"
    perfil = imagem / "perfil.png"

class _DataBase(_Caminho):
    dataBase = _Caminho.bancoDados

    errosdb = dataBase / "errosDb.db"
    keys = dataBase / "keysDB.db"
    botdb = dataBase / "botDB.db"
    modDb = dataBase / "modDB.db"
    taskDb = dataBase / "tarefadb.db"
    rotadb = dataBase / "rotasdb.db"

class _DataJson(_Caminho):
    json = _Caminho.assets / "json"
    rotas = json / "rotas.json"