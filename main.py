from services.estoque_service import EstoqueService

def ler_inteiro(mensagem):
    valor = input(mensagem)
    return int(valor)

def ler_float(mensagem):
    valor = input(mensagem).replace(",", ".")
    return float(valor)

def pausar():
    input("\nPressione ENTER para continuar...")

def imprimir_registros(registros, mensagem_vazia):
    if len(registros) == 0:
        print(mensagem_vazia)
        return

    for registro in registros:
        print(registro)

def mostrar_menu():
    print("\n╔══════════════════════════════════════════════╗")
    print("║          SISTEMA DE ESTOQUE E VENDAS         ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ CLIENTES                                     ║")
    print("║  1 - Cadastrar cliente                       ║")
    print("║  2 - Listar clientes                         ║")
    print("║  3 - Buscar cliente                          ║")
    print("║  4 - Remover cliente                         ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ PRODUTOS                                     ║")
    print("║  5 - Cadastrar produto                       ║")
    print("║  6 - Listar produtos                         ║")
    print("║  7 - Buscar produto                          ║")
    print("║  8 - Atualizar estoque                       ║")
    print("║  9 - Remover produto                         ║")
    print("║ 10 - Listar produtos em ordem inversa        ║")
    print("║ 11 - Listar produtos ordenados por ID        ║")
    print("║ 12 - Buscar produto por ID usando Busca      ║")
    print("║      Binária                                 ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ VENDAS                                       ║")
    print("║ 13 - Realizar venda simples de exemplo       ║")
    print("║ 14 - Visualizar fila de vendas               ║")
    print("║ 15 - Visualizar primeira venda da fila       ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ RELATÓRIOS                                   ║")
    print("║ 16 - Exibir valor total do estoque           ║")
    print("║ 17 - Exibir valor total das vendas           ║")
    print("║ 18 - Exibir clientes e valores totais gastos ║")
    print("║ 19 - Exibir cliente que mais gastou          ║")
    print("║ 20 - Exibir produto mais vendido             ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ SISTEMA                                      ║")
    print("║ 21 - Desfazer ultima operacao                ║")
    print("║  0 - Sair                                    ║")
    print("╚══════════════════════════════════════════════╝")


def executar_opcao(opcao, service):
    if opcao == 1:  
        nome = input("Digite o nome do cliente: ")
        cliente = service.cadastrar_cliente(nome)
        print(f"Cliente cadastrado com sucesso! Código: {cliente.codigo}, Nome: {cliente.nome}")
        

    elif opcao == 2:
        clientes = service.listar_clientes()
        imprimir_registros(clientes, "Nenhum cliente cadastrado.")

    elif opcao == 3:
        procurando = ler_inteiro("Digite o código do cliente que deseja buscar: ")
        cliente = service.buscar_cliente(procurando)
        if cliente:
            print(f"Cliente encontrado! Código: {cliente.codigo}, Nome: {cliente.nome}")
        else:
            print("Cliente não encontrado.")

    elif opcao == 4:
        codigo_removido = ler_inteiro("Digite o código do cliente que deseja remover: ")
        cliente_removido = service.remover_cliente(codigo_removido)
        if cliente_removido:
            print(f"Cliente removido com sucesso! Código: {cliente_removido.codigo}, Nome: {cliente_removido.nome}")
        else:
            print("Cliente não encontrado ou lista de clientes vazia.")

    elif opcao == 5:
        nome = input("Digite o nome do produto: ")
        preco = ler_float("Digite o preço do produto: ")
        quantidade = ler_inteiro("Digite a quantidade em estoque do produto: ")
        produto = service.cadastrar_produto(nome, preco, quantidade)
        print(f"Produto cadastrado com sucesso! Código: {produto.codigo}, Nome: {produto.nome}, Preço: {produto.preco}, Quantidade: {produto.quantidade}")
        
    elif opcao == 6:
        produtos = service.listar_produtos()
        imprimir_registros(produtos, "Nenhum produto cadastrado.")

    elif opcao == 7:
        procurando = ler_inteiro("Digite o código do Produto que deseja buscar: ")
        produto = service.buscar_produto(procurando)
        if produto:
            print(f"Produto encontrado! Código: {produto.codigo}, Nome: {produto.nome}, Preço: {produto.preco}, Quantidade: {produto.quantidade}")
        else:
            print("Produto não encontrado.")

    elif opcao == 8:
        quer_atualizar = input("Você deseja atualizar algum produto? (s/n): ")
        if quer_atualizar.lower() == 's':
            codigo_atualizar = ler_inteiro("Digite o código do produto que deseja atualizar: ")
            if codigo_atualizar <= 0:
                raise ValueError("O código do produto deve ser maior que zero.")
            nova_quantidade = ler_inteiro("Digite a nova quantidade em estoque: ")
            produto_atualizado = service.atualizar_estoque(codigo_atualizar, nova_quantidade)
            if produto_atualizado:
                print(f"Produto atualizado com sucesso! Código: {produto_atualizado.codigo}, Nome: {produto_atualizado.nome}, Preço: {produto_atualizado.preco}, Quantidade: {produto_atualizado.quantidade}")
            else:
                print("Produto não encontrado ou lista de produtos vazia.")
        else:
            print("Atualização de estoque cancelada.")

    elif opcao == 9:
        codigo_removido = ler_inteiro("Digite o código do produto que deseja remover:")
        produto_removido = service.remover_produto(codigo_removido)
        if produto_removido:
            print(f"Produto removido com sucesso! Código: {produto_removido.codigo}, Nome: {produto_removido.nome}, Preço: {produto_removido.preco}, Quantidade: {produto_removido.quantidade}")
        else:
            print("Produto não encontrado ou lista de produtos vazia.")

    elif opcao == 10:
        produtos_inverso = service.listar_produtos_inverso()
        imprimir_registros(produtos_inverso, "Nenhum produto cadastrado.")

    elif opcao == 11:
        lista_por_id = service.listar_produtos_ordenados_por_id()
        imprimir_registros(lista_por_id, "Nenhum produto cadastrado.")

    elif opcao == 12:
        produto_buscar = ler_inteiro("Digite o código do produto que você deseja buscar: ")
        produto_encontrado = service.buscar_produto_binario(produto_buscar)
        if produto_encontrado:
            print(f"Produto encontrado com sucesso! Código: {produto_encontrado.codigo}, Nome: {produto_encontrado.nome}, Preço: {produto_encontrado.preco}, Quantidade: {produto_encontrado.quantidade}")
        else:
            print("Produto não encontrado ou lista de produtos vazia.")


    elif opcao == 13:
        print("Realizando venda simples de exemplo...")
        cliente = ler_inteiro("Digite o código do cliente para a venda: ")
        if cliente <= 0:
            raise ValueError("O código do cliente deve ser maior que zero.")
        produto = ler_inteiro("Digite o código do produto para a venda: ")
        if produto <= 0:
            raise ValueError("O código do produto deve ser maior que zero.")
        quantidade = ler_inteiro("Digite a quantidade do produto para a venda: ")
        if quantidade <= 0:
            raise ValueError("A quantidade do produto deve ser maior que zero.")
        venda = service.realizar_venda_exemplo(cliente, produto, quantidade)
        if venda:
            print(f"Venda realizada com sucesso! Código da venda: {venda.codigo}, Código do cliente: {venda.codigo_cliente}, Itens: {venda.itens}, Valor total: R${venda.valor_total:.2f}")
        else:
            print("Venda não realizada. Verifique se o cliente e o produto existem e se há estoque suficiente.")

    elif opcao == 14:
        vendas = service.listar_vendas()
        imprimir_registros(vendas, "Nenhuma venda realizada.")

    elif opcao == 15:
        venda = service.primeira_venda()
        if venda:
            print(f"Primeira venda da fila: Código da venda: {venda.codigo}, Código do cliente: {venda.codigo_cliente}, Itens: {venda.itens}, Valor total: R${venda.valor_total:.2f}")
        else:
            print("Nenhuma venda realizada.")

    elif opcao == 16:
        valor_total_estoque = service.valor_total_estoque()
        print(f"Valor total do estoque: R${valor_total_estoque:.2f}")

    elif opcao == 17:
        valor_total_vendas = service.valor_total_vendas()
        print(f"Valor total das vendas: R$ {valor_total_vendas:.2f}")

    elif opcao == 18:
        clientes = service.clientes_e_valores_totais_gastos()

        if not clientes:
            print("Nenhum cliente encontrado.")
        else:
            for cliente in clientes:
                print(
                f"Cliente: {cliente['nome']} "
                f"(Código {cliente['codigo_cliente']}) - "
                f"Total gasto: R$ {cliente['total_gasto']:.2f}"
            )

        pausar()
        

    elif opcao == 19:
        cliente = service.cliente_que_mais_gastou()

        if cliente is None:
            print("Nenhum cliente encontrado.")
        else:
            print(
                f"Cliente que mais gastou: {cliente['nome']} "
                f"(Código {cliente['codigo_cliente']}) - "
                f"Total gasto: R$ {cliente['total_gasto']:.2f}"
            )

        pausar()

    elif opcao == 20:
        pass

    elif opcao == 21:
        pass

    else:
        print("Opcao invalida. Tente novamente.")

def main():
    service = EstoqueService()

    while True:
        mostrar_menu()

        try:
            opcao = ler_inteiro("Escolha uma opcao: ")

            if opcao < 0 or opcao > 21:
                raise ValueError("Opcao invalida. Tente novamente.")

            if opcao == 0:
                print("Sistema encerrado.")
                break

            executar_opcao(opcao, service)

        except ValueError as erro:
            print(f"Erro: {erro}")
        except IndexError as erro:
            print(f"Erro: {erro}")
        except NotImplementedError as erro:
            print(f"Funcionalidade para completar: {erro}")

        pausar()

if __name__ == "__main__":
    main()