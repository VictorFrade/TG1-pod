class SistemaStreaming:
    def __init__(self, config_file):
        self.musicas = []
        self.podcasts = []
        self.usuarios = []
        self.playlists = []
        self.config_file = config_file
        self._log = 'logs/erros.log'

    def _registrar_erro(self, msg):
        """
        Registra mensagens de erro em um arquivo de log.
        """
        try:
            with open(self._log, 'a') as arq:
                arq.write(msg + '\n')
        except Exception:
            pass

    # Método público para registrar erros externamente (auxilio da IA em debug)
    def log_erro(self, msg: str):
        self._registrar_erro(msg)

    def carregar_dados(self):
        """
        Carrega dados de usuários, músicas, podcasts e playlists a partir do arquivo de configuração.
        """
        try:
            # abre o arquivo e itera linhas, ignorando vazias e mantendo comentários
            with open(self.config_file, 'r') as f:
                secao = None
                for texto in f:
                    linha = texto.strip()
                    if not linha:
                        continue

                    if linha.startswith('#'):
                        secao = linha[1:].strip().upper()
                        continue

                    if linha.startswith('-'):
                        conteudo = linha[1:].strip()
                        if not conteudo:
                            continue
                        partes = [p.strip() for p in conteudo.split(';')]
                        self._processar_linha(secao, partes)

        except FileNotFoundError:
            print(f"Arquivo de configuração '{self.config_file}' ausente.")
            self._registrar_erro(f"Config não encontrada: {self.config_file}")
        except Exception as e:
            print(f"Falha inesperada ao ler dados: {e}")
            self._registrar_erro(f"Falha inesperada ao ler dados: {e}")

    def _processar_linha(self, secao, dados):
        """
        Processa uma linha de dados conforme a seção atual. Usa imports locais para evitar ciclos.
        """
        try:
            # Importações locais para evitar ciclos de importação durante o carregamento do módulo
            if secao == 'MUSICAS':
                from Streaming.musica import Musica
                titulo, artista, duracao, genero = dados
                self.musicas.append(Musica(titulo, artista, int(duracao), genero))
            elif secao == 'PODCASTS':
                from Streaming.podcast import Podcast
                titulo, host, duracao, temporada, episodio = dados
                self.podcasts.append(Podcast(titulo, host, int(duracao), temporada, int(episodio)))
            elif secao == 'USUARIOS':
                from Streaming.usuario import Usuario
                self.usuarios.append(Usuario(dados[0]))
            elif secao == 'PLAYLISTS':
                nome_playlist, nome_usuario, *titulos = dados
                usuario = self.encontrar_usuario(nome_usuario)

                if not usuario:
                    self._registrar_erro(
                        f"Usuário '{nome_usuario}' da playlist '{nome_playlist}' não localizado."
                    )
                    return
                
                playlist = usuario.criar_playlist(nome_playlist)
                for t in titulos:
                    midia = self.encontrar_midia(t)
                    if midia:
                        playlist.adicionar_midia(midia)
                    else:
                        self._registrar_erro(
                            f"Item '{t}' na playlist '{nome_playlist}' não encontrado."
                        )
                self.playlists.append(playlist)

        except (ValueError, IndexError) as e:
            self._registrar_erro(
                f"Formato inválido em '{';'.join(dados)}' na seção '{secao}': {e}"
            )

    def encontrar_usuario(self, nome):
        """
        Encontra um usuário pelo nome.
        """
        alvo = nome.lower()
        for u in self.usuarios:
            try:
                if u.nome.lower() == alvo:
                    return u
            except AttributeError:
                pass
        return None

    def encontrar_midia(self, titulo):
        """
        Encontra uma mídia (música ou podcast) pelo título."""
        alvo = titulo.lower()
        for m in (self.musicas + self.podcasts):
            try:
                if m.titulo.lower() == alvo:
                    return m
            except AttributeError:
                pass
        return None

    def criar_usuario(self, nome):
        """
        Cria um novo usuário no sistema usando a função da classe Usuario.
        """
        if self.encontrar_usuario(nome):
            raise ValueError(f"Usuário '{nome}' já existe.")
        
        from Streaming.usuario import Usuario  # import local para evitar ciclos
        novo = Usuario(nome)
        self.usuarios.append(novo)
        return novo


def main():
    """
    Função principal para iniciar o sistema de streaming.
    """
    # Import local para evitar carregar Menu (e suas dependências) no topo do módulo
    from Streaming.menu import Menu
    caminho_config = 'config/dados.md'
    sistema = SistemaStreaming(caminho_config)
    sistema.carregar_dados()
    Menu(sistema).menu_principal()


if __name__ == "__main__":
    main()