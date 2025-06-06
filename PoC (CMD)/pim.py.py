class Usuario:
    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo.lower()


class Chamado:
    _id_counter = 1

    def __init__(self, titulo, descricao, solicitante):
        self.id = Chamado._id_counter
        Chamado._id_counter += 1
        self.titulo = titulo
        self.descricao = descricao
        self.solicitante = solicitante
        self.status = "Aberto"

    def __str__(self):
        return f"ID: {self.id} | Título: {self.titulo} | Status: {self.status} | Solicitante: {self.solicitante}"


class SistemaChamados:
    def __init__(self):
        self.chamados = []

    def criar_chamado(self, titulo, descricao, solicitante):
        chamado = Chamado(titulo, descricao, solicitante)
        self.chamados.append(chamado)
        print(f"\nChamado {chamado.id} criado com sucesso.")

    def listar_chamados(self):
        if not self.chamados:
            print("\nNenhum chamado encontrado.")
            return
        print("\nLista de Chamados:")
        for chamado in self.chamados:
            print(chamado)

    def atualizar_chamado(self, id_chamado, novo_status):
        for chamado in self.chamados:
            if chamado.id == id_chamado:
                chamado.status = novo_status
                print(f"\nChamado {id_chamado} atualizado para '{novo_status}'.")
                return
        print("\nChamado não encontrado.")

    def deletar_chamado(self, id_chamado):
        for chamado in self.chamados:
            if chamado.id == id_chamado:
                self.chamados.remove(chamado)
                print(f"\nChamado {id_chamado} removido com sucesso.")
                return
        print("\nChamado não encontrado.")

    def gerar_relatorio(self, status_filtrado=None):
        if not self.chamados:
            print("\nNenhum chamado registrado.")
            return

        print("\nRelatório de Chamados:")
        for chamado in self.chamados:
            if status_filtrado is None or chamado.status.lower() == status_filtrado.lower():
                print(f"ID: {chamado.id} | Título: {chamado.titulo} | Status: {chamado.status}")
        print("Fim do Relatório")


usuarios_cadastrados = []


def cadastrar_usuario():
    login = input("Novo login: ").strip()
    senha = input("Nova senha: ").strip()
    tipo = input("Tipo de usuário (admin/suporte): ").strip().lower()

    if tipo not in ["admin", "suporte"]:
        print("Tipo inválido. Usuário não criado.")
        return None

    for usuario in usuarios_cadastrados:
        if usuario.login == login:
            print("Login já existe.")
            return None

    novo_usuario = Usuario(login, senha, tipo)
    usuarios_cadastrados.append(novo_usuario)
    print("Usuário cadastrado com sucesso.")
    return novo_usuario


def autenticar():
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    for usuario in usuarios_cadastrados:
        if usuario.login == login and usuario.senha == senha:
            print(f"Acesso concedido como {usuario.tipo}.")
            return usuario
    print("Usuário ou senha inválidos.")
    return None


def menu_inicial():
    while True:
        print("\n==== Menu Inicial ====")
        print("1 - Login")
        print("2 - Cadastrar novo usuário")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            usuario = autenticar()
            if usuario:
                return usuario
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "0":
            print("Encerrando o sistema.")
            exit()
        else:
            print("Opção inválida.")


def menu(usuario, sistema):
    while True:
        print("\n==== MENU DE CHAMADOS ====")
        print("1 - Criar Chamado")
        print("2 - Listar Chamados")
        print("3 - Atualizar Chamado")
        if usuario.tipo == "admin":
            print("4 - Deletar Chamado")
            print("5 - Gerar Relatório")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            titulo = input("Título do chamado: ").strip()
            descricao = input("Descrição do chamado: ").strip()
            sistema.criar_chamado(titulo, descricao, usuario.login)

        elif opcao == "2":
            sistema.listar_chamados()

        elif opcao == "3":
            try:
                id_chamado = int(input("ID do chamado: "))
                novo_status = input("Novo status (Aberto / Em Andamento / Fechado): ").strip()
                sistema.atualizar_chamado(id_chamado, novo_status)
            except ValueError:
                print("ID inválido.")

        elif opcao == "4" and usuario.tipo == "admin":
            try:
                id_chamado = int(input("ID do chamado a deletar: "))
                sistema.deletar_chamado(id_chamado)
            except ValueError:
                print("ID inválido.")

        elif opcao == "5" and usuario.tipo == "admin":
            status = input("Filtrar por status (ou deixe em branco para todos): ").strip()
            sistema.gerar_relatorio(status if status else None)

        elif opcao == "0":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida ou não permitida.")


if __name__ == "__main__":
    sistema = SistemaChamados()
    print("\nBem-vindo à NeoCall – Sistema de Gestão de Chamados")
    usuario_logado = menu_inicial()
    menu(usuario_logado, sistema)
