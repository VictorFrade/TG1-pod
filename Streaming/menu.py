import os
import datetime
from Streaming.analises import Analises
from Streaming.playlist import Playlist

class Menu:
    """
    Classe que gerencia os menus de interação com o usuário.
    """
    def __init__(self, sistema):
        self.sistema = sistema

    def _limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _exibir_cabecalho(self, titulo):
        self._limpar_tela()
        print("=" * 40)
        print(f"{titulo:^40}")
        print("=" * 40)

    def menu_principal(self):
        """Exibe o menu principal e gerencia a navegação.""" 
        while True:
            self._exibir_cabecalho("MENU PRINCIPAL")
            print("1. Entrar como usuário") 
            print("2. Criar novo usuário")
            print("3. Listar usuários") 
            print("4. Sair") 
            
            escolha = input(">> Escolha uma opção: ")
            
            if escolha == '1':
                self.entrar_como_usuario()
            elif escolha == '2':
                self.criar_novo_usuario()
            elif escolha == '3':
                self.listar_usuarios()
            elif escolha == '4':
                self.gerar_relatorio_final()
                print("Sistema finalizado. Relatório e logs foram salvos.")
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")

    def entrar_como_usuario(self):
        self._exibir_cabecalho("ENTRAR COMO USUÁRIO")
        nome = input("Digite seu nome de usuário: ")
        usuario = self.sistema.encontrar_usuario(nome)
        
        if usuario:
            self.menu_usuario(usuario)
        else:
            print(f"Usuário '{nome}' não encontrado.")
            input("Pressione Enter para continuar...")

    def criar_novo_usuario(self):
        self._exibir_cabecalho("CRIAR NOVO USUÁRIO")
        nome = input("Digite o nome para o novo usuário: ")
        try:
            self.sistema.criar_usuario(nome)
            print(f"Usuário '{nome}' criado com sucesso!")
        except ValueError as e:
            print(f"Erro: {e}")
            self.sistema.log_erro(str(e))
        input("Pressione Enter para continuar...")

    def listar_usuarios(self):
        self._exibir_cabecalho("LISTA DE USUÁRIOS")
        if not self.sistema.usuarios:
            print("Nenhum usuário cadastrado.")
        else:
            for usuario in self.sistema.usuarios:
                print(f"- {usuario.nome}")
        input("Pressione Enter para continuar...")

    def menu_usuario(self, usuario):
        """Exibe o menu do usuário logado."""
        while True:
            self._exibir_cabecalho(f"Bem-vindo(a), {usuario.nome}!")
            print("1. Reproduzir uma música") 
            print("2. Listar mídias")
            print("3. Listar playlists") 
            print("4. Criar nova playlist")
            print("5. Concatenar playlists")
            print("6. Recomendar músicas")
            print("7. Reproduzir playlist")
            print("8. Sair (Voltar ao menu principal)") 
            
            escolha = input(">> Escolha uma opção: ")

            if escolha == '1':
                self.reproduzir_midia(usuario)
            elif escolha == '2':
                self.listar_midias()
            elif escolha == '3':
                self.listar_playlists(usuario)
            elif escolha == '4':
                self.criar_playlist(usuario)
            elif escolha == '5':
                self.concatenar_playlists(usuario)
            elif escolha == '6':
                self.recomendar_musicas_para_usuario(usuario)
            elif escolha == '7':
                self.reproduzir_playlist(usuario)
            elif escolha == '8':
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")

    def reproduzir_midia(self, usuario):
        self._exibir_cabecalho("REPRODUZIR MÍDIA")
        self.listar_midias(pausar=False)
        titulo = input("Digite o título da mídia que deseja ouvir: ")
        midia = self.sistema.encontrar_midia(titulo)
        if midia:
            usuario.ouvir_midia(midia)
        else:
            print(f"Mídia '{titulo}' não encontrada.")
        input("Pressione Enter para continuar...")

    def listar_midias(self, pausar=True):
        self._exibir_cabecalho("MÚSICAS E PODCASTS") 
        print("\n--- Músicas ---")
        for m in self.sistema.musicas:
            print(m)
        print("\n--- Podcasts ---")
        for p in self.sistema.podcasts:
            print(p)
        if pausar:
            input("\nPressione Enter para continuar...")

    def listar_playlists(self, usuario):
        self._exibir_cabecalho("SUAS PLAYLISTS")
        if not usuario.playlists:
            print("Você ainda não criou nenhuma playlist.")
        else:
            for i, p in enumerate(usuario.playlists):
                print(f"{i+1}. {p}")
        input("Pressione Enter para continuar...")
        
    def criar_playlist(self, usuario):
        self._exibir_cabecalho("CRIAR NOVA PLAYLIST")
        nome_playlist = input("Digite o nome da nova playlist: ")
        try:
            playlist = usuario.criar_playlist(nome_playlist)
            while True:
                print("\nAdicionar mídia à playlist (deixe em branco para finalizar):")
                titulo_midia = input("Título da mídia: ")
                if not titulo_midia:
                    break
                midia = self.sistema.encontrar_midia(titulo_midia)
                if midia:
                    playlist.adicionar_midia(midia)
                    print(f"'{midia.titulo}' adicionada.")
                else:
                    print(f"Mídia '{titulo_midia}' não encontrada.")
            print(f"Playlist '{nome_playlist}' criada com sucesso!")
        except ValueError as e:
            print(f"Erro: {e}")
            self.sistema.log_erro(str(e))
        input("Pressione Enter para continuar...")

    def reproduzir_playlist(self, usuario):
        """Permite ao usuário reproduzir uma de suas playlists."""
        self._exibir_cabecalho("REPRODUZIR PLAYLIST")
        if not usuario.playlists:
            print("Você ainda não criou nenhuma playlist.")
            input("Pressione Enter para continuar...")
            return

        i = 0
        for p in usuario.playlists:
            print(f"{i}. {p.nome} ({len(p)} itens)")
            i += 1

        try:
            idx = int(input("Índice da playlist para reproduzir: "))
            playlist = usuario.playlists[idx]
            playlist.reproduzir()
        except (ValueError, IndexError):
            print("Erro: índice inválido.")
        input("Pressione Enter para continuar...")

    def concatenar_playlists(self, usuario):
        self._exibir_cabecalho("CONCATENAR PLAYLISTS")
        if len(usuario.playlists) < 2:
            print("Você precisa de pelo menos duas playlists para concatenar.")
            input("Pressione Enter para continuar...")
            return

        for i, p in enumerate(usuario.playlists):
            print(f"{i}. {p.nome}")
        
        try:
            idx1 = int(input("Índice da primeira playlist: "))
            idx2 = int(input("Índice da segunda playlist: "))
            
            p1 = usuario.playlists[idx1]
            p2 = usuario.playlists[idx2]
            
            nova_playlist = p1 + p2
            usuario.playlists.append(nova_playlist) # Adiciona a nova playlist ao usuário
            
            print(f"\nPlaylists '{p1.nome}' e '{p2.nome}' concatenadas.")
            print(f"Nova playlist criada: '{nova_playlist.nome}' com {len(nova_playlist)} itens.")
        except (ValueError, IndexError):
            print("Erro: Índices inválidos.")
        input("Pressione Enter para continuar...")
        
    def recomendar_musicas_para_usuario(self, usuario):
        self._exibir_cabecalho("MÚSICAS RECOMENDADAS PARA VOCÊ")
        recomendacoes = Analises.recomendar_musicas(usuario, self.sistema.usuarios, self.sistema.musicas)
        
        if not recomendacoes:
            print("Não foi possível gerar recomendações no momento.")
        else:
            for musica in recomendacoes:
                print(f"- {musica}")
        input("Pressione Enter para continuar...")

    def gerar_relatorio_final(self):
        """Gera e salva o relatório final de reproduções.""" 
        self._exibir_cabecalho("GERANDO RELATÓRIO")
        
        report_path = os.path.join('relatorios', 'relatorio.txt')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 40 + "\n")
            f.write(f"Relatório de Reproduções - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 40 + "\n\n")

            # Top 5 Músicas
            top_5_musicas = Analises.top_musicas_reproduzidas(self.sistema.musicas, 5)
            f.write("--- TOP 5 MÚSICAS MAIS REPRODUZIDAS ---\n")
            for m in top_5_musicas:
                f.write(f"- {m.titulo} por {m.artista} ({m.reproducoes} reproduções)\n")
            f.write("\n")

            # Playlist mais popular
            if self.sistema.playlists:
                playlist_pop = Analises.playlist_mais_popular(self.sistema.playlists)
                f.write("--- PLAYLIST MAIS POPULAR ---\n")
                f.write(f"- {playlist_pop.nome} de {playlist_pop.usuario.nome} ({playlist_pop.reproducoes} reproduções)\n\n")

            # Usuário mais ativo
            if self.sistema.usuarios:
                user_ativo = Analises.usuario_mais_ativo(self.sistema.usuarios)
                f.write("--- USUÁRIO MAIS ATIVO ---\n")
                f.write(f"- {user_ativo.nome} ({len(user_ativo.historico)} mídias ouvidas)\n\n")

            # Média de avaliações
            medias = Analises.media_avaliacoes(self.sistema.musicas)
            f.write("--- MÉDIA DE AVALIAÇÕES DAS MÚSICAS ---\n")
            for titulo, media in medias.items():
                f.write(f"- {titulo}: {media:.2f}\n")
            f.write("\n")

            # Total de reproduções
            total = Analises.total_reproducoes(self.sistema.usuarios)
            f.write("--- TOTAL DE REPRODUÇÕES NO SISTEMA ---\n")
            f.write(f"Total: {total}\n")
