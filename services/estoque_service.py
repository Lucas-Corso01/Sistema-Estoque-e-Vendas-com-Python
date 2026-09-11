import os

from algoritmos.ordenacao import ordenar_produtos_por_id
from algoritmos.busca_binaria import buscar_produto_por_id
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from estruturas.fila import Fila
from estruturas.pilha import Pilha
from estruturas.lde import LDE
from estruturas.lse import LSE
from services.persistencia_service import PersistenciaService

class EstoqueService:
    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")

        self.clientes = LSE()
        self.produtos = LDE()
        self.vendas = Fila()
        self.historico = Pilha()
        self.persistencia = PersistenciaService(pasta_data)

        self.carregar_dados()

    def carregar_dados(self):
        for cliente in self.persistencia.carregar_clientes():
            if self.clientes.buscar(cliente.codigo) is None:
                self.clientes.inserir_fim(cliente)

        for produto in self.persistencia.carregar_produtos():
            if self.produtos.buscar(produto.codigo) is None:
                self.produtos.inserir_fim(produto)

        for venda in self.persistencia.carregar_vendas():
            self.vendas.enqueue(venda)

    def gerar_proximo_codigo_cliente(self):
        return self._gerar_proximo_codigo(self.clientes.listar())

    def gerar_proximo_codigo_produto(self):
        return self._gerar_proximo_codigo(self.produtos.listar())

    def gerar_proximo_codigo_venda(self):
        return self._gerar_proximo_codigo(self.vendas.listar())

    def _gerar_proximo_codigo(self, registros):
        maior_codigo = 0

        for registro in registros:
            if registro.codigo > maior_codigo:
                maior_codigo = registro.codigo

        return maior_codigo + 1

    def cadastrar_cliente(self, nome):
        codigo = self.gerar_proximo_codigo_cliente()
        cliente = Cliente(codigo, nome)
        self.clientes.inserir_fim(cliente)
        self.salvar_clientes()
        self.historico.push({
                "tipo": "cadastrar_cliente",
                "cliente": cliente
                })
        return cliente

    def listar_clientes(self):
        if self.clientes.is_empty():
            return []
        return self.clientes.listar()

    def buscar_cliente(self, codigo):
        if self.clientes.is_empty():
            return None
        return self.clientes.buscar(codigo)

    def remover_cliente(self, codigo):
        cliente = self.clientes.remover(codigo)

        if cliente:
            self.salvar_clientes()
            self.historico.push({
                "tipo": "remover_cliente",
                "cliente": cliente
            })

        return cliente

    def cadastrar_produto(self, nome, preco, quantidade):
        codigo = self.gerar_proximo_codigo_produto()
        produto = Produto(codigo, nome, preco, quantidade)
        self.produtos.inserir_fim(produto)
        self.salvar_produtos()
        self.historico.push({
        "tipo": "cadastrar_produto",
        "produto": produto
        })
        return produto

    def listar_produtos(self):
        if self.produtos.is_empty():
                    return []
        return self.produtos.listar()

    def listar_produtos_inverso(self):
        return self.produtos.listar_inverso()

    def listar_produtos_ordenados_por_id(self):
        if self.produtos.is_empty():
            return []
        produtos = ordenar_produtos_por_id(self.produtos.listar())
        return produtos

    def buscar_produto(self, codigo):
        if self.produtos.is_empty():
                    return None
        return self.produtos.buscar(codigo)

    def buscar_produto_binario(self, codigo):
        if self.produtos.is_empty():
                    return None
        produtos = ordenar_produtos_por_id(self.produtos.listar())
        return buscar_produto_por_id(produtos, codigo)

    def atualizar_estoque(self, codigo, nova_quantidade):
        produto = self.produtos.buscar(codigo)

        if produto:
            anterior = produto.quantidade
            produto.atualizar_estoque(nova_quantidade)
            self.salvar_produtos()

            self.historico.push({
                "tipo": "atualizar_estoque",
                "codigo": codigo,
                "anterior": anterior
            })

            return produto

        return None

    def remover_produto(self, codigo):
        produto = self.produtos.remover(codigo)

        if produto:
            self.salvar_produtos()
            self.historico.push({
                "tipo": "remover_produto",
                "produto": produto
            })

        return produto

    def realizar_venda_exemplo(self, codigo_cliente, itens_venda):
        if self.produtos.is_empty():
            return None

        cliente = self.clientes.buscar(codigo_cliente)

        if not cliente:
            return None

        itens = []

        for item in itens_venda:
            produto = self.produtos.buscar(item["codigo_produto"])
            quantidade = item["quantidade"]

            if not produto or quantidade <= 0:
                return None

            if produto.quantidade < quantidade:
                return None

            itens.append({
                "codigo_produto": produto.codigo,
                "quantidade": quantidade,
                "preco_unitario": produto.preco
            })

        if not itens:
            return None

        for item in itens:
            produto = self.produtos.buscar(item["codigo_produto"])
            produto.atualizar_estoque(
                produto.quantidade - item["quantidade"]
            )

        self.salvar_produtos()

        codigo_venda = self.gerar_proximo_codigo_venda()
        venda = Venda(codigo_venda, codigo_cliente, itens)

        self.vendas.enqueue(venda)
        self.salvar_vendas()

        self.historico.push({
            "tipo": "realizar_venda",
            "venda": venda
        })

        return venda

    
    def listar_vendas(self):
        if self.vendas.is_empty():
            return []
        return self.vendas.listar()

    def primeira_venda(self):
        if self.vendas.is_empty():
            return None

        return self.vendas.front()

    def valor_total_estoque(self):
        total = 0

        for produto in self.produtos.listar():
            total += produto.preco * produto.quantidade

        return total

    def valor_total_vendas(self):
        total = 0
        
        for venda in self.vendas.listar():
            total += venda.valor_total

        return total

    def clientes_e_valores_totais_gastos(self):
        resultado = []

        for cliente in self.clientes.listar():
            total = 0

            for venda in self.vendas.listar():
                if venda.codigo_cliente == cliente.codigo:
                    total += venda.valor_total

            resultado.append({
                "codigo_cliente": cliente.codigo,
                "nome": cliente.nome,
                "total_gasto": total
            })

        return resultado

    def cliente_que_mais_gastou(self):
        clientes = self.clientes_e_valores_totais_gastos()

        if not clientes:
            return None

        maior = clientes[0]

        for cliente in clientes:
            if cliente["total_gasto"] > maior["total_gasto"]:
                maior = cliente

        return maior

    def produto_mais_vendido(self):
        totais = {}

        for venda in self.vendas.listar():
            for item in venda.itens:
                codigo = item["codigo_produto"]
                totais[codigo] = totais.get(codigo, 0) + item["quantidade"]

        if not totais:
            return None

        for codigo in sorted(totais, key=totais.get, reverse=True):
            produto = self.produtos.buscar(codigo)
            if produto:
                return produto, totais[codigo]

        return None

    def desfazer_ultima_operacao(self):
        if self.historico.is_empty():
            return None

        operacao = self.historico.pop()
        tipo = operacao["tipo"]

        if tipo == "cadastrar_cliente":
            self.clientes.remover(operacao["cliente"].codigo)
            self.salvar_clientes()

        elif tipo == "remover_cliente":
            self.clientes.inserir_fim(operacao["cliente"])
            self.salvar_clientes()

        elif tipo == "cadastrar_produto":
            self.produtos.remover(operacao["produto"].codigo)
            self.salvar_produtos()

        elif tipo == "remover_produto":
            self.produtos.inserir_fim(operacao["produto"])
            self.salvar_produtos()

        elif tipo == "atualizar_estoque":
            produto = self.produtos.buscar(operacao["codigo"])
            produto.atualizar_estoque(operacao["anterior"])
            self.salvar_produtos()

        elif tipo == "realizar_venda":
            venda = operacao["venda"]

            for item in venda.itens:
                produto = self.produtos.buscar(item["codigo_produto"])
                produto.atualizar_estoque(
                    produto.quantidade + item["quantidade"]
                )

            vendas = [
                v for v in self.vendas.listar()
                if v.codigo != venda.codigo
            ]

            self.vendas = Fila()

            for v in vendas:
                self.vendas.enqueue(v)

            self.salvar_produtos()
            self.salvar_vendas()

        return True

    def salvar_clientes(self):
        self.persistencia.salvar_clientes(self.clientes.listar())

    def salvar_produtos(self):
        self.persistencia.salvar_produtos(self.produtos.listar())

    def salvar_vendas(self):
        self.persistencia.salvar_vendas(self.vendas.listar())