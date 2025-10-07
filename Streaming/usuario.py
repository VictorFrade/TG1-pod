from Streaming.playlist import Playlist
from Streaming.arquivo_de_midia import ArquivoDeMidia

class Usuario:
    """
    Representa um usuário do sistema de streaming.

    Attributes:
        nome (str): O nome do usuário.
        playlists (list[Playlist]): Lista de playlists criadas pelo usuário.
        historico (list[ArquivoDeMidia]): Histórico de mídias ouvidas pelo usuário.
    """
    qntd_instancias = 0

    def __init__(self, nome: str):
        self.nome = nome 
        self.playlists = [] 
        self.historico = [] 
        Usuario.qntd_instancias += 1

    def ouvir_midia(self, midia: ArquivoDeMidia):
        """
        Simula o usuário ouvindo uma mídia, adicionando-a ao histórico.
        """
        midia.reproduzir()
        self.historico.append(midia) 

    def criar_playlist(self, nome_playlist: str) -> Playlist:
        """
        Cria uma nova playlist para o usuário.
        """
        for p in self.playlists:
            if p.nome.lower() == nome_playlist.lower():
                raise ValueError(f"Playlist '{nome_playlist}' já existe para o usuário {self.nome}.")
        
        nova_playlist = Playlist(nome_playlist, self)
        self.playlists.append(nova_playlist)
        return nova_playlist

    def __str__(self):
        """
        Retorna o nome do usuário.
        """
        return self.nome

    def __repr__(self):
        """
        Retorna uma representação detalhada do objeto Usuario.
        """
        return f"Usuario(nome='{self.nome}')"
