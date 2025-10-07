from Streaming.arquivo_de_midia import ArquivoDeMidia


class Podcast(ArquivoDeMidia):
    """
    Representa um episódio de podcast, classe filha de ArquivoDeMidia.

    Atributos:
        Herdados de ArquivoDeMidia:
        titulo (str): Título do episódio.
        host (str): Host do podcast (equivale ao artista da classe pai).
        duracao (int): Duração do episódio em segundos.

        Proprios da classe Podcast:
        temporada (str): Temporada do episódio.
        episodio (int): Número do episódio.
    """

    def __init__(self, titulo: str, host: str, duracao: int, temporada: str, episodio: int):
        super().__init__(titulo, host, duracao)  # host = artista
        self.temporada = temporada
        self.episodio = episodio

    def reproduzir(self):
        """
        Simula a reprodução de um episódio do podcast.
        """
        super().reproduzir()
        print(f"Ep. {self.episodio} (Temporada: {self.temporada})")

    def __str__(self):
        return f"Podcast: {self.titulo} | Host: {self.artista} | Duração: {self.duracao}s | Temporada: {self.temporada} | Episódio: {self.episodio}"

    def __repr__(self):
        return (f"Podcast(titulo='{self.titulo}', host='{self.artista}', duracao={self.duracao}, temporada='{self.temporada}', episodio={self.episodio})")
