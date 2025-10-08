from Streaming.arquivo_de_midia import ArquivoDeMidia

class Musica(ArquivoDeMidia):
    """
    Representa uma música, uma subclasse de ArquivoDeMidia.

    Attributes:
        genero (str): O gênero da música.
        avaliacoes (list[int]): Uma lista de avaliações de 0 a 5.
    """
    def __init__(self, titulo: str, artista: str, duracao: int, genero: str):
        super().__init__(titulo, artista, duracao)
        self.genero = genero 
        self.avaliacoes = [] 

    def reproduzir(self):
        """
        Simula a reprodução da música.
        """
        super().reproduzir()

    def __str__(self):
        return f"Música: {self.titulo} - Artista: {self.artista} - Duração: {self.duracao} segundos - Gênero: {self.genero}"

    def __repr__(self):
        return (f"Musica(titulo='{self.titulo}', artista='{self.artista}', "
                f"duracao={self.duracao}, genero='{self.genero}')")