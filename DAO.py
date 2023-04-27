from Models import *

# Dao armazena no arquivo de texto (nosso banco de dados) e lê dele

class DaoCategoria:
    
    @classmethod
    def salvar(cls, categoria):
        with open('categoria.txt', 'a') as arq:
            arq.writelines(categoria)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('categoria.txt', 'r') as arq:
            cls.categoria = arq.readlines()
        
        cls.categoria = list(map(lambda x: x.replace('\n', ''), cls.categoria))
        
        cat = [Categoria(i) for i in cls.categoria]
        return cat

class DaoVenda:
    @classmethod
    def salvar(cls, venda: Venda):
        with open('venda.txt', 'a') as arq:
            arq.writelines(venda.itensvendido.nome + '|'
                            + venda.itensvendido.preco + '|'
                            + venda.itensvendido.categoria + '|'
                            + venda.vendedor + '|' + venda.comprador + '|' 
                            + str(venda.quantidade_vendida) + '|' + venda.data)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('venda.txt', 'r') as arq:
            cls.venda = arq.readlines()

        cls.venda = list(map(lambda x: x.replace('\n', ''), cls.venda))
        cls.venda = list(map(lambda x: x.split('|'), cls.venda))

        vend = [Venda(Produtos(i[1], i[2], i[3]), i[4], i[5], i[6], i[7] ) for i in cls.venda]
        return vend
    
class DaoEstoque:
    @classmethod
    def salvar(cls, produtos: Produtos, quantidade):
        with open('estoque.txt', 'a') as arq:
            arq.writelines(produtos.nome + '|' 
                           + produtos.preco + '|' 
                           + produtos.categoria + '|'
                           + str(quantidade))
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('estoque.txt', 'r') as arq:
            cls.estoque = arq.readlines()

        cls.estoque = list(map(lambda x: x.replace('\n', ''), cls.estoque))
        cls.estoque = list(map(lambda x: x.split('|'), cls.estoque))

        est = [Estoque(Produtos(i[0], i[1], i[2]), int(i[3])) for i in cls.estoque if len(cls.estoque) > 0]
        return est

class DaoFornecedor:
    @classmethod
    def salvar(cls, fornecedor: Fornecedor):
        with open('fornecedores.txt', 'a') as arq:
            arq.writelines(fornecedor.nome + '|' 
                           + fornecedor.cnpj + '|' 
                           + fornecedor.telefone + '|'
                           + fornecedor.categoria)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('fornecedores.txt', 'r') as arq:
            cls.fornecedores = arq.readlines()

        cls.fornecedores = list(map(lambda x: x.replace('\n', ''), cls.fornecedores))
        cls.fornecedores = list(map(lambda x: x.split('|'), cls.fornecedores))

        forn = [Fornecedor(i[0], i[1], i[2], i[3]) for i in cls.fornecedores]
        return forn
    
class DaoPessoa:
    @classmethod
    def salvar(cls, pessoas: Pessoa):
        with open('clientes.txt', 'a') as arq:
            arq.writelines(pessoas.nome + '|' 
                           + pessoas.telefone + '|' 
                           + pessoas.cpf + '|'
                           + pessoas.email + '|'
                           + pessoas.endereco)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('clientes.txt', 'r') as arq:
            cls.clientes = arq.readlines()

        cls.clientes = list(map(lambda x: x.replace('\n', ''), cls.clientes))
        cls.clientes = list(map(lambda x: x.split('|'), cls.clientes))

        cliente = [Pessoa(i[0], i[1], i[2], i[3], i[4]) for i in cls.clientes]
        return cliente
    
class DaoFuncionario:
    @classmethod
    def salvar(cls, funcionario: Funcionario):
        with open('funcionarios.txt', 'a') as arq:
            arq.writelines(funcionario.clt + '|' 
                           + funcionario.nome + '|' 
                           + funcionario.telefone + '|' 
                           + funcionario.cpf + '|'
                           + funcionario.email + '|'
                           + funcionario.endereco)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('funcionarios.txt', 'r') as arq:
            cls.funcionarios = arq.readlines()

        cls.funcionarios = list(map(lambda x: x.replace('\n', ''), cls.funcionarios))
        cls.funcionarios = list(map(lambda x: x.split('|'), cls.funcionarios))

        funcionario = [Funcionario(i[0], i[1], i[2], i[3], i[4], i[5]) for i in cls.funcionarios]
        return funcionario