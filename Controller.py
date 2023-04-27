from Models import *
from DAO import *
from datetime import datetime

class ControllerCategoria:
    def cadastraCategoria(self, novaCategoria):
        existe = False

        x = DaoCategoria.ler()

        for i in x:
            if i.categoria == novaCategoria:
                existe = True
        
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('A categoria que você está tentando cadastra já existe!')

    def removerCategoria(self, deleteCategoria):

        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == deleteCategoria, x))
        
        if len(cat) <= 0:
            print('A categoria que deseja remover não existe!')
        else:
            for i in range(len(x)):
                if x[i].categoria == deleteCategoria:
                    del x[i]
                    break
            print('Categoria removida com sucesso!')
        
            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

        estoque = DaoEstoque.ler()
        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, 'Sem categoria'), x.quantidade) if(x.produto.categoria == deleteCategoria) else(x), estoque))

        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + '|' 
                           + i.produto.preco + '|' 
                           + i.produto.categoria + '|'
                           + str(i.quantidade))
                arq.writelines('\n')              

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if(x.categoria == categoriaAlterar) else(x), x))
                print('Categoria alterada com sucesso!')
                estoque = DaoEstoque.ler()
                estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaAlterada), x.quantidade) if(x.produto.categoria == categoriaAlterar) else(x), estoque))

                with open('estoque.txt', 'w') as arq:
                    for i in estoque:
                        arq.writelines(i.produto.nome + '|' 
                                + i.produto.preco + '|' 
                                + i.produto.categoria + '|'
                                + str(i.quantidade))
                        arq.writelines('\n') 
            else:
                print('A categoria que deseja alterar já existe')
        else:
            print('Categoria não existe!')
        
        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Não existe nunhuma categoria cadastrada no sistema')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')

class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produtos = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produtos, quantidade)
                print('Produto cadastrado com sucesso!')
            else:
                print('Produto já existe em estoque.')
        else:
            print('Categoria não existe.')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('Produto removido com sucesso!')
        else:
            print('Produto inexistente.')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + '|' 
                           + i.produto.preco + '|' 
                           + i.produto.categoria + '|'
                           + str(i.quantidade))
                arq.writelines('\n')
                
    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == novaCategoria, y))

        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                produto = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(produto) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), x))
                    print('Produto alterado com sucesso')
                else:
                    print('Este produto já existe!')
            else:
                print('Produto não existe.')
            
            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + '|' 
                                    + i.produto.preco + '|' 
                                    + i.produto.categoria + '|'
                                    + str(i.quantidade))
                    arq.writelines('\n')
        else:
            print('A categoria fornecida não existe.')

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()

        if len(estoque) == 0:
            print('Estoque vazio')
        else:
            print('=================================Produtos================================')
            for i in estoque:
                print(f'Nome: {i.produto.nome} | Preço: R$: {i.produto.preco} reais | Categoria: {i.produto.categoria} | Quantidade: {i.quantidade}')
            print('-------------------------------------------------------------------------')

class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)

                        DaoVenda.salvar(vendido)
            temp.append(Estoque(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade))

        arq = open('estoque.txt', 'w')
        arq.write("")

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i.produto.nome + '|' 
                                + i.produto.preco + '|'
                                + i.produto.categoria + '|' 
                                + str(i.quantidade))
                arq.writelines('\n')
            
        if existe == False:
            print('Produto não existe')
            return None
        elif not quantidade:
            print('A quantidade vendida não contem em estoque')
            return None
        else:
            print('Venda realizada com sucesso')
            return valorCompra
            
    def relatorioDeVenda(self):
        vendas = DaoVenda.ler()
        produtos = []

        
        for i in vendas:
            nome = i.itensvendido.nome
            quantidade = i.quantidade_vendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)} 
                                    if(x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)
        
        print('Esses são os produto mais vendidos')
        a = 1
        for i in ordenado:
            print(f'==========Produto [{a}] ==========')
            print(f'Produto: {i["produto"]} | Quantidade: {i["quantidade"]}')
            a += 1

    def mostrarVendas(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino, '%d/%m/%Y')

        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y') >= dataInicio1 
                                         and datetime.strptime(x.data, '%d/%m/%Y') <= dataTermino1, vendas))
        count = 1
        total = 0

        for i in vendasSelecionadas:
            print(f'==============================================Venda [{count}]==============================================')
            print(f'Nome: {i.itensvendido.nome} | Categoria: {i.itensvendido.categoria} | Data: {i.data} | Quantidade: {i.quantidade_vendida} | Cliente: {i.comprador} | Vendedor: {i.vendedor}')
            total += int(i.itensvendido.preco) * int(i.quantidade_vendida)
            count += 1
        print(f'Total vendido: R$: {total:.2f}')

class ControllerFornecedor:
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        y = DaoCategoria.ler()

        listCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listTelefone = list(filter(lambda x: x.telefone == telefone, x))
        listCategoria = list(filter(lambda y: y.categoria == categoria, y))

        if len(listCategoria) == 0:
            print('Categoria não existe')
            return None
        elif len(listCnpj) > 0:
            print('Cnpj já existe')
            return None
        elif len(listTelefone) > 0:
            print('Telefone já existe')
            return None
        else:
            if len(cnpj) == 14 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
                print('Fornecedor cadastrado com sucesso!')
            else:
                print('Digite um cnpj ou telefone válido')

    def altararFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novaCategoria):

        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            est = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len(est) == 0:
                x  = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novaCategoria) if(x.nome == nomeAlterar) else(x), x))
            else:
                print('Cnpj já existe')
        else:
            print('Fornecedor não existe')

        with open('fornecedor.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + '|' + i.cnpj + '|' + i.telefone + '|' + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor alterado com sucesso')

    def removerFornecedor(self, nome):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('Fornecedor não existe')
            return None
        
        with open('fornecedor.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + '|' + i.cnpj + '|' + i.telefone + '|' + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor removido com sucesso!')

    def mostrarFornecedores(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) == 0:
            print('Lista de fornecedores vazia')

        for i in fornecedores:
            print('================================Fornecedores================================')
            print(f'Categoria fornecida: {i.categoria} | Nome: {i.nome} | Telefone: {i.telefone} | Cnpj: {i.cnpj}')

class ControllerCliente:
    def casdastrarCliente(self, nome, telefone, cpf, email, endereco):
        x = DaoPessoa.ler()

        listCpf = list(filter(lambda x: x.cpf == cpf, x))
        listTelefone = list(filter(lambda x: x.telefone == telefone, x))
        listEmail = list(filter(lambda x: x.email == email, x))

        if len(listEmail) > 0:
            print('Email já existe')
            return None
        elif len(listCpf) > 0:
            print('Cpf já existe')
            return None
        elif len(listTelefone) > 0:
            print('Telefone já existe')
            return None
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso!')
            else:
                print('Digite um cpf ou telefone válido')
    
    def alterarCliente(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoPessoa.ler()

        listTelefone = list(filter(lambda x: x.telefone == novoTelefone, x))
        listCpf = list(filter(lambda x: x.cpf == novoCpf, x))
        listEmail = list(filter(lambda x: x.email == novoEmail, x))
        pessoa = list(filter(lambda x: x.nome == nomeAlterar, x))

        if len(pessoa) == 0:
            print('Cliente não existe')
            return None
        elif len(listEmail) > 0:
            print('Email já existe')
            return None
        elif len(listCpf) > 0:
            print('Cpf já existe')
            return None
        elif len(listTelefone) > 0:
            print('Telefone já existe')
            return None
        else:
            x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if(x.nome == nomeAlterar) else(x), x))

        with open('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')
            print('Cliente alterado com sucesso')
        
    def removerCliente(self, email):
        x = DaoPessoa.ler()

        pessoa = list(filter(lambda x: x.email == email, x))

        if len(pessoa) > 0:
            for i in range(len(x)):
                if x[i].email == email:
                    del x[i]
                    break
        else:
            print('Cliente não existe')
            return None
        
        with open('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')
            print('Cliente deletado com sucesso')
    
    def mostrarCliente(self):
        cliente = DaoPessoa.ler()

        if len(cliente) == 0:
            print('Nenhum cliente no sistema')
        else:
            for i in cliente:
                print('================================================Cliente===============================================')
                print(f'Nome: {i.nome} | Telefone: {i.telefone} | Endereço: {i.endereco} | Email: {i.email} | Cpf: {i.cpf}')

class ControllerFuncionario:
    def cadastrarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        x = DaoFuncionario.ler()

        listCpf = list(filter(lambda x: x.cpf == cpf, x))
        listClt = list(filter(lambda x: x.clt == clt, x))
        listTelefone = list(filter(lambda x: x.telefone == telefone, x))
        listEmail = list(filter(lambda x: x.email == email, x))

        if len(listClt) > 0:
            print('Clt já existe')
            return None
        elif len(listCpf) > 0:
            print('Cpf já existe')
            return None
        elif len(listTelefone) > 0:
            print('Telefone já existe')
            return None
        elif len(listEmail) > 0:
            print('Email já existe')
            return None
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoFuncionario.salvar(Funcionario(clt, nome, telefone, cpf, email, endereco))
                print('Funcionário cadastrado com sucess!')
            else:
                print('Digite um cpf ou telefone válido')

    def alterarFuncionario(self, emailAlterar, novoClt, novoEmail, novoTelefone, novoCpf, novoNome, novoEndereco):
        x = DaoFuncionario.ler()

        listEmail = list(filter(lambda x: x.email == emailAlterar, x))

        if len(listEmail) > 0:
            x = list(map(lambda x: Funcionario(novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if(x.email == emailAlterar) else(x), x))
        else:
            print('Email não existe')
            return None
        
        with open('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt + '|' + i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')
            print('Funcionario alterado com sucesso!')

    def removerFuncionario(self, email):
        x = DaoFuncionario.ler()

        funcionario = list(filter(lambda x: x.email == email, x))
        if len(funcionario) > 0:
            for i in range(len(x)):
                if x[i].email == email:
                    del x[i]
                    break
        else:
            print('Funcionario não existe.')
            return None

        with open('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt + '|' + i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')
            print('Funcionario removido com sucesso!')
        
    def mostrarFuncionarios(self):
        funcionario = DaoFuncionario.ler()

        if len(funcionario) == 0:
            print('Lista de funcionairos vazia')
        else:
            for i in funcionario:
                print('================================================Funcionarios===============================================')
                print(f'Clt: {i.clt} | Nome: {i.nome} | Telefone: {i.telefone} | Endereço: {i.endereco} | Email: {i.email} | Cpf: {i.cpf}')
