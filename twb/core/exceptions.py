class VillageInitException(Exception):
    """
    Erro quando a inicialização da vila não ocorre corretamente
    """


class VillageNotExists(Exception):
    """
    Uma vila foi adicionada ao bot que não está configurada no arquivo de configuração
    """


class InvalidGameStateException(Exception):
    """
    Houve um erro ao ler o estado do jogo da vila
    """


class InvalidUnitTemplateException(Exception):
    """
    O template de unidade selecionada para a vila está ausente ou corrompido
    """


class InvalidJSONException(Exception):
    """
    O arquivo JSON que estou tentando ler está corrompido e não pode ser analisado
    """


class FileNotFoundException(Exception):
    """
    O arquivo que estou tentando ler não existe e era esperado que estivesse presente
    """


class UnsupportedPythonVersion(Exception):
    """
    Você está tentando executar o bot com uma versão desatualizada do Python
    Atualizar para Python3 resolve este problema
    """


class NoInternetException(Exception):
    """
    Erro ao inicializar a vila devido à falta de conexão com a internet
    """
