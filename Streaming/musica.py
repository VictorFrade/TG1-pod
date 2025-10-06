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

    def avaliar(self, nota: int):
        """
        Adiciona uma nova avaliação à lista de avaliações da música.
        A nota deve estar entre 0 e 5.

        Args:
            nota (int): A nota de avaliação.
        
        Raises:
            ValueError: Se a nota estiver fora do intervalo permitido.
        """
        if 0 <= nota <= 5:
            self.avaliacoes.append(nota) 
        else:
            raise ValueError("A nota de avaliação deve estar entre 0 e 5.")

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