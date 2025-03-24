import dataclasses
import re
from typing import Dict, Optional, Tuple

from bs4 import BeautifulSoup
from requests import Response
from twb.core.request import WebWrapper


class Point:
    """Representa um ponto com coordenadas x e y."""

    def __init__(self, x: int, y: int):
        if not isinstance(x, int):
            raise TypeError("x deve ser um inteiro")
        if not isinstance(y, int):
            raise TypeError("y deve ser um inteiro")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}|{self.y})"

    def __eq__(self, other: "Point") -> bool:
        """Verifica se duas instâncias de Point têm as mesmas coordenadas."""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def distance_to(self, other: "Point") -> float:
        """Calcula o quadrado da distância entre este ponto e outro ponto."""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __str__(self):
        return f"({self.x}|{self.y})"


class Farm:
    """Representa a população da fazenda."""

    def __init__(self, population: str):
        """
        Inicializa um objeto Farm.

        Args:
            population (str): A representação em string da população.
                Formato: 'atual/máxima'.

        Levanta:
            ValueError: Se o formato da string da população for inválido.
        """
        if not re.match(r"\d+/\d+", population):
            raise ValueError("Formato de string de população inválido.")
        current, maximum = map(int, population.split("/"))
        self.current = current
        self.maximum = maximum

    def is_full(self) -> bool:
        """
        Verifica se a fazenda está cheia.

        Retorna:
            bool: True se a fazenda estiver cheia, false caso contrário.
        """
        return self.current == self.maximum

    def calculate_remaining_capacity(self) -> int:
        """
        Calcula a capacidade restante da fazenda.

        Retorna:
            int: A capacidade restante.
        """
        return self.maximum - self.current


class Storage:
    """Representa os recursos de armazenamento (madeira, pedra, ferro)."""

    def __init__(self, resources: str, capacity: str):
        """
        Inicializa um objeto Storage.

        Args:
            resources (str): A representação em string dos recursos.
                Formato: 'madeira,pedra,ferro'.
            capacity (str): A representação em string da capacidade.
                Formato: 'capacidade'.

        Levanta:
            ValueError: Se o formato da string dos recursos for inválido.
            ValueError: Se o formato da string da capacidade for inválido.
        """
        resource_values = resources.replace(".", "").split(" ")
        if len(resource_values) != 3:
            print("Formato inválido da string de recursos")
        try:
            self.wood = int(resource_values[0])
            self.stone = int(resource_values[1])
            self.iron = int(resource_values[2])
        except ValueError as err:
            raise ValueError("Formato inválido da string de recursos") from err
        try:
            self.capacity = int(capacity)
        except ValueError as err:
            raise ValueError("Formato inválido da string de capacidade") from err


class Village:
    """Representa uma aldeia com seu nome, coordenadas e continente."""

    def __init__(
        self,
        village_id: str,
        village_name: str,
        coordinates: Point,
        continent: str,
        points: str,
        storage: Storage,
        farm: Farm,
    ):
        """
        Inicializa um objeto Village.

        Args:
            village_id (str): O ID da aldeia.
            village_name (str): O nome da aldeia.
            coordinates (Point): As coordenadas da aldeia.
            continent (str): O continente da aldeia.
            points (str): Os pontos da aldeia.
            storage (Storage): O armazenamento da aldeia.
            farm (Farm): A fazenda da aldeia.

        Levanta:
            ValueError: Se o formato da string da aldeia for inválido.
        """
        self._village_id = village_id
        self._village_name = village_name
        self._coordinates = coordinates
        self._continent = continent
        self._points = int(points.replace(".", ""))
        self._storage = storage
        self._farm = farm

    def __str__(self) -> str:
        """Retorna uma representação legível da aldeia."""
        return f"Aldeia: {self._village_name}, Coordenadas: {self._coordinates}, Continente: {self._continent}"

    def __repr__(self):
        return f"Village(village_id={self._village_id}, village_name={self._village_name}, coordinates={self._coordinates}, continent={self._continent}, points={self._points}, storage={self._storage}, farm={self._farm})"

    @staticmethod
    def parse_coordinates(cords: str) -> "Point":
        """
        Analisa a string das coordenadas e retorna um objeto Point.

        Args:
            cords (str): A representação em string das coordenadas.

        Retorna:
            Point: O objeto Point com as coordenadas analisadas.
        """
        x, y = map(int, cords.strip("()").split("|"))
        return Point(x, y)

    @property
    def village_id(self) -> str:
        return self._village_id

    @property
    def village_name(self) -> str:
        return self._village_name

    @property
    def coordinates(self) -> Point:
        return self._coordinates

    @property
    def continent(self) -> str:
        return self._continent

    @property
    def points(self) -> int:
        return self._points

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def farm(self) -> Farm:
        return self._farm


@dataclasses.dataclass
class WorldSettings:
    """Representa as configurações do mundo."""

    flags: bool = Optional[bool]
    knight: bool = Optional[bool]
    boosters: bool = Optional[bool]
    quests: bool = Optional[bool]


class OverviewPage:
    """Representa a página de visão geral com os dados da aldeia e as opções do mundo."""

    def __init__(self, wrapper):
        """
        Inicializa um objeto OverviewPage.

        Args:
            wrapper: O objeto wrapper para fazer requisições HTTP.
        """
        self.wrapper: WebWrapper = wrapper
        self.world_settings: WorldSettings = WorldSettings()
        self.result_get: Response = self._get_overview_villages_data()
        self.soup = BeautifulSoup(self.result_get.text, "html.parser")
        self.header_info = self.soup.find("table", id="header_info")
        self.production_table = self.soup.find("table", id="production_table")
        self.villages_data: Dict[str, Village] = {}
        self.parse_production_table()
        self.parse_header_info()

    def _get_overview_villages_data(self):
        """Obtém os dados das aldeias da visão geral usando o objeto wrapper."""
        return self.wrapper.get_url("game.php?screen=overview_villages")

    def parse_production_table(self):
        """Analisa a tabela de produção para extrair os dados das aldeias."""
        if self.production_table:
            rows = self.production_table.find_all("tr")
            for row in rows:
                if row.find_all("td"):
                    cells = row.find_all("td")
                    idx_offset = (
                        1 if len(cells[0].contents) == 0 else 0
                    )  # Compatibilidade com conta premium
                    village_id = cells[idx_offset].contents[1].attrs["data-id"]

                    name, coordinates, continent = self._extract_name_cords_continent(
                        cells[idx_offset].text.strip()
                    )
                    points = cells[1 + idx_offset].text.strip()
                    resources = cells[2 + idx_offset].text.strip()
                    storage_capacity = cells[3 + idx_offset].text.strip()

                    storage = Storage(resources, storage_capacity)
                    farm = Farm(cells[4 + idx_offset].text.strip())
                    village = Village(
                        village_id, name, coordinates, continent, points, storage, farm
                    )
                    self.villages_data[village_id] = village

    def parse_header_info(self) -> None:
        """Analisa as informações do cabeçalho para obter as opções do mundo."""
        text = self.result_get.text

        self.world_settings.flags = "screen=flags" in text
        self.world_settings.knight = "screen=statue" in text
        self.world_settings.boosters = "screen=inventory" in text
        self.world_settings.quests = "Quests.setQuestData" in text

    @staticmethod
    def _extract_name_cords_continent(cell_value: str) -> Tuple[str, Point, str]:
        """Extrai nome, coordenadas e continente do valor da célula."""
        match = re.match(r"(.+)\s\((\d+)\|(\d+)\)\s(.+)", cell_value)
        if match:
            name = match.group(1)
            coordinates = Point(int(match.group(2)), int(match.group(3)))
            continent = match.group(4)
            return name, coordinates, continent
        else:
            print("Formato inválido da string da aldeia. Pulando aldeia..")
