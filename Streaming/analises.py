from typing import List, Dict
from Streaming.musica import Musica
from Streaming.playlist import Playlist
from Streaming.usuario import Usuario

class Analises:
    """
    Classe utilitária para gerar análises e estatísticas sobre os dados do sistema.
    """

    @staticmethod
    def top_musicas_reproduzidas(musicas: List[Musica], top_n: int) -> List[Musica]:
        """Retorna as top N músicas mais reproduzidas.""" 
        return sorted(musicas, key=lambda m: m.reproducoes, reverse=True)[:top_n]

    @staticmethod
    def playlist_mais_popular(playlists: List[Playlist]) -> Playlist:
        """Retorna a playlist mais ouvida (com mais reproduções)."""
        return max(playlists, key=lambda p: p.reproducoes)

    @staticmethod
    def usuario_mais_ativo(usuarios: List[Usuario]) -> Usuario:
        """Retorna o usuário que mais ouviu mídias (maior histórico)."""
        return max(usuarios, key=lambda u: len(u.historico))

    @staticmethod
    def media_avaliacoes(musicas: List[Musica]) -> Dict[str, float]:
        """Retorna a média de avaliação de cada música que possui avaliações.""" 
        medias = {}
        for musica in musicas:
            if musica.avaliacoes:
                media = sum(musica.avaliacoes) / len(musica.avaliacoes)
                medias[musica.titulo] = round(media, 2)
        return medias

    @staticmethod
    def total_reproducoes(usuarios: List[Usuario]) -> int:
        """Retorna o total de reproduções feitas por todos os usuários."""
        return sum(len(u.historico) for u in usuarios)
        
    # Funcionalidade de Inovação [cite: 100]
    @staticmethod
    def recomendar_musicas(usuario_alvo: Usuario, todos_usuarios: List[Usuario], todas_musicas: List[Musica], n_recomendacoes: int = 3):
        """
        Recomenda músicas para um usuário com base no que outros usuários com
        gostos similares ouviram.
        """
        if not usuario_alvo.historico:
            # Recomenda as mais populares se o usuário não ouviu nada
            return Analises.top_musicas_reproduzidas(todas_musicas, n_recomendacoes)
        
        historico_alvo_titulos = {m.titulo for m in usuario_alvo.historico if isinstance(m, Musica)}
        
        # Encontra usuários com gostos similares
        usuarios_similares = []
        for usuario in todos_usuarios:
            if usuario != usuario_alvo:
                historico_outro_titulos = {m.titulo for m in usuario.historico if isinstance(m, Musica)}
                interseccao = historico_alvo_titulos.intersection(historico_outro_titulos)
                if len(interseccao) > 0:
                    usuarios_similares.append(usuario)
        
        # Coleta músicas que os usuários similares ouviram e o alvo não
        recomendacoes = {}
        for similar in usuarios_similares:
            for musica in similar.historico:
                if isinstance(musica, Musica) and musica.titulo not in historico_alvo_titulos:
                    if musica not in recomendacoes:
                        recomendacoes[musica] = 0
                    recomendacoes[musica] += 1
        
        # Ordena as recomendações pela frequência
        recomendacoes_ordenadas = sorted(recomendacoes.keys(), key=lambda m: recomendacoes[m], reverse=True)
        
        return recomendacoes_ordenadas[:n_recomendacoes]