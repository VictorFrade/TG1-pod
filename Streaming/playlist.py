
from Streaming.arquivo_de_midia import ArquivoDeMidia
from Streaming.usuario import Usuario


class Playlist:
    """
    Representa uma playlist criada por um usuário.

        nome (str): O nome da playlist.
        usuario (Usuario): O usuário que criou a playlist.
        itens (list[ArquivoDeMidia]): A lista de mídias na playlist.
    """

    def __init__(self, nome: str, usuario: 'Usuario'):
        self.nome = nome
        self.usuario = usuario
        self.itens = []
        self.reproducoes = 0

    def adicionar_midia(self, midia: ArquivoDeMidia):
        """Adiciona uma mídia à playlist."""
        self.itens.append(midia)

    def remover_midia(self, midia: ArquivoDeMidia):
        """Remove uma mídia da playlist."""
        self.itens.remove(midia)

    def reproduzir(self):
        """
        Reproduz todas as mídias da playlist em ordem
        """
        print(f"--- Reproduzindo a Playlist: {self.nome} ---")
        self.reproducoes += 1
        for midia in self.itens:
            midia.reproduzir()
        print(f"--- Fim da Playlist: {self.nome} ---")

    def __add__(self, other: 'Playlist'):
        """
        Concatena duas playlists, criando uma nova.
        A nova playlist tem o nome da primeira.
        """
        if not isinstance(other, Playlist):
            raise NotImplementedError(
                "Só é possível concatenar uma Playlist com outra Playlist.")

        nova_playlist = Playlist(self.nome, self.usuario)
        nova_playlist.itens = self.itens + other.itens
        nova_playlist.reproducoes = self.reproducoes + other.reproducoes
        return nova_playlist

    def __len__(self):
        """Retorna o número de itens na playlist."""
        return len(self.itens)

    def __getitem__(self, index: int):
        """Acesso por índice ao item da playlist."""
        return self.itens[index]

    def __eq__(self, other):
        """
        Compara se duas playlists são iguais.
        """
        if not isinstance(other, Playlist):
            raise NotImplementedError(
                "Só é possível comparar uma Playlist com outra Playlist.")
        return (self.nome == other.nome and
                self.usuario == other.usuario and
                self.itens == other.itens)

    def __str__(self):
        return f"Playlist '{self.nome}' (Criada por: {self.usuario.nome}, {len(self.itens)} mídias) | Nº de reproduções: {self.reproducoes}"

    def __repr__(self):
        return f"Playlist(nome='{self.nome}', usuario='{self.usuario.nome}')"
