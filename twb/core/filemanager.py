import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from twb.core.exceptions import FileNotFoundException
from twb.core.exceptions import InvalidJSONException


class FileManager:
    """Fornece métodos para gerenciamento de arquivos e diretórios."""

    @staticmethod
    def get_root() -> Path:
        """Retorna o diretório raiz do projeto."""
        return Path.cwd()

    @staticmethod
    def get_path(path: Union[str, Path]) -> Path:
        """Retorna o caminho completo de um arquivo ou diretório no projeto."""
        return FileManager.get_root() / path

    @staticmethod
    def path_exists(path: Union[str, Path]) -> bool:
        """Retorna Treu se o caminho existir, False caso contrário."""
        return Path(path).exists()

    @staticmethod
    def create_directory(directory: Union[str, Path]) -> None:
        """Cria um diretório se ele não existir."""
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_directories(directories: List[Union[str, Path]]) -> None:
        """Cria uma lista de diretórios no diretório raiz, se eles não existirem."""
        root_directory = FileManager.get_root()
        for directory in directories:
            FileManager.create_directory(root_directory / directory)

    @staticmethod
    def list_directory(
        directory: Union[str, Path], ends_with: Optional[str] = None
    ) -> List[str]:
        """Retorna uma lista de arquivo em um diretório.
        Se ends_with for especificado, retorna apenas arquivos que terminem com o sufixo informado."""
        full_path = FileManager.get_root() / directory
        files = [f.name for f in full_path.iterdir() if f.is_file()]
        if ends_with:
            files = [f for f in files if f.endswith(ends_with)]
        return files

    @staticmethod
    def __open_file(path: Union[str, Path], mode: str = "r"):
        """Abre um arquivo no modo especificado. Privado, Não usar fora do FileManager."""
        full_path = FileManager.get_root() / path
        try:
            return full_path.open(mode, encoding="utf-8")
        except FileNotFoundError as err:
            raise FileNotFoundException from err

    @staticmethod
    def read_file(path: Union[str, Path]) -> Optional[str]:
        """Lê o conteúdo de um arquivo e retorna os dados. Retorna None se o arquivo não existir."""
        full_path = FileManager.get_root() / path

        if not FileManager.path_exists(full_path):
            return None

        with FileManager.__open_file(full_path) as file:
            return file.read()

    @staticmethod
    def read_lines(path: Union[str, Path]) -> Optional[List[str]]:
        """Lê o conteúdo de um arquivo e retorna as linhas. Retorna None se o arquivo não existir."""
        full_path = FileManager.get_root() / path

        if not FileManager.path_exists(full_path):
            return None

        with FileManager.__open_file(full_path) as file:
            return file.readlines()

    @staticmethod
    def remove_file(path: Union[str, Path]) -> None:
        """Remove um arquivo, se ele existir."""
        full_path = FileManager.get_root() / path

        if FileManager.path_exists(full_path):
            full_path.unlink()

    @staticmethod
    def load_json_file(
        path: Union[Path, str], **kwargs
    ) -> Any | None:
        """Carrega um arquivo JSON e retorna os dados. Retorna None se o arquivo não existir."""
        full_path = FileManager.get_root() / path

        if not FileManager.path_exists(full_path):
            return None

        with FileManager.__open_file(full_path) as file:
            try:
                return json.load(file, **kwargs)
            except json.decoder.JSONDecodeError as err:
                raise InvalidJSONException from err

    @staticmethod
    def save_json_file(
        data: Dict[str, Union[str, Dict[str, str]]], path: Union[str, Path], **kwargs
    ) -> None:
        """Salva dados em um arquivo JSON. Se o arquivo não existir, ele será criado."""
        full_path = FileManager.get_root() / path

        with FileManager.__open_file(full_path, mode="w") as file:
            json.dump(data, file, indent=2, sort_keys=False, **kwargs)

    @staticmethod
    def copy_file(src_path: Union[str, Path], dest_path: Union[str, Path]) -> bool:
        """Copia um arquivo do caminho de origem para o caminho de destino."""
        full_src_path = FileManager.get_root() / src_path
        full_dest_path = FileManager.get_root() / dest_path

        if not FileManager.path_exists(full_src_path):
            return False

        full_dest_path.write_text(full_src_path.read_text(), encoding="utf-8")
        return True
