
from abc import ABC, abstractmethod


class ArquivoDeMidia(ABC):
    """
    Classe abstrata que representa um arquivo de mídia (musica / podcast)

    Atributos:
        titulo (str): Título do arquivo de mídia.
        artista (str): Nome do artista.
        duracao (int): Duração em segundos.
        reproducoes (int): Número de vezes que a mídia foi reproduzida.
    """

    def __init__(self, titulo: str, artista: str, duracao: int):
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao
        self.reproducoes = 0

    @abstractmethod
    def reproduzir(self):
        """
        Simula a reprodução da mídia, incrementando o contador e exibindo informações.
        """
        self.reproducoes += 1
        print(
            f"Reproduzindo: '{self.titulo}' de {self.artista} ({self.duracao} segundos)")

    def __eq__(self, outro):
        """
        Compara se dois arquivos de mídia são iguais com base no título e no artista.
        """
        if not isinstance(outro, ArquivoDeMidia):
            raise NotImplementedError(
                "Você só pode fazer uma comparação entre tipos de arquivos de mídia.")
        else:
            return self.titulo.lower() == outro.titulo.lower() and self.artista.lower() == outro.artista.lower()

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
