from Streaming.musica import Musica

class Analises:
    """
    Classe para gerar análises e estatísticas sobre os dados do sistema.
    """
    @staticmethod
    def top_musicas_reproduzidas(musicas, top_n):
        """
        Retorna as top músicas mais reproduzidas.
        """
        return sorted(musicas, key=lambda m: m.reproducoes, reverse=True)[:top_n]

    @staticmethod
    def playlist_mais_popular(playlists):
        """
        Retorna a playlist mais ouvida.
        """
        return max(playlists, key=lambda p: p.reproducoes)

    @staticmethod
    def usuario_mais_ativo(usuarios):
        """
        Retorna o usuário que ouviu o maior número de mídias.
        """
        return max(usuarios, key=lambda u: len(u.historico))

    @staticmethod
    def total_reproducoes(usuarios):
        """
        Retorna o total de reproduções feitas por todos os usuários.
        """
        return sum(len(u.historico) for u in usuarios)

    # INOVAÇÃO
    @staticmethod
    def recomendar_musicas(usuario_alvo, todos_usuarios, todas_musicas, n_recomendacoes=3):
        """
        Recomenda músicas para um usuário com base no que outros usuários com
        gostos similares ouviram.
        """
        if not usuario_alvo.historico:
            # Recomenda as músicas mais populares se o usuário não ouviu nada
            return Analises.top_musicas_reproduzidas(todas_musicas, n_recomendacoes)

        historico_alvo_titulos = {
            m.titulo for m in usuario_alvo.historico if isinstance(m, Musica)
        }

        # Encontra usuários com gostos similares
        usuarios_similares = []
        for usuario in todos_usuarios:
            if usuario != usuario_alvo:
                historico_outro_titulos = {
                    m.titulo for m in usuario.historico if isinstance(m, Musica)
                }
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

        # Ordena as recomendações 
        recomendacoes_ordenadas = sorted(
            recomendacoes.keys(), key=lambda m: recomendacoes[m], reverse=True
        )
        return recomendacoes_ordenadas[:n_recomendacoes]