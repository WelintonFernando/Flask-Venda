import flask
from src.control.classe_conexao import Conexao


"""
host 177.190.74.69
porta 65004
usuario trabtpc
senha trabtpc
banco tpcXX

XX = 1, 2 , 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

"""

conexao = Conexao("tpc14", "trabtpc", "trabtpc", '177.190.74.69', 65004)
#conexao = Conexao("venda", "root", "ifsp", "localhost", 3306)
conexao.abrirConexao()

app = flask.Flask(__name__, template_folder="./src/view/", static_folder="./src/static/")

@app.route('/')
def menu():
    return flask.render_template('menu.html')

@app.route('/produtos')
def produtos():
    sql = "SELECT codproduto, nome, preco FROM Produto"
    produtos = conexao.retornar(sql)
    produtos = [{'codproduto': p[0], 'nome': p[1], 'preco': p[2]} for p in produtos]
    return flask.render_template('produtos.html', produtos=produtos)


@app.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    codigo = flask.request.form['codigo']
    sql = f"SELECT codproduto FROM Produto WHERE codproduto = {codigo}"
    resultado = conexao.retornar(sql)
    # se houver resultado, significa que o produto já existe, então vai alterar
    if resultado:
        nome = flask.request.form['nome']
        preco = flask.request.form['preco']
        sql = f"UPDATE Produto SET nome = '{nome}', preco = {preco} WHERE codproduto = {codigo}"
        conexao.executar(sql)
        return flask.redirect('/produtos')

    nome = flask.request.form['nome']
    preco = flask.request.form['preco']
    sql = f"INSERT INTO Produto (codproduto, nome, preco) VALUES ('{codigo}', '{nome}', {preco})"
    conexao.executar(sql)
    return flask.redirect('/produtos')

@app.route('/remover_produto/<int:codigo>')
def remover_produto(codigo):
    sql = f"DELETE FROM Produto WHERE codproduto = {codigo}"
    conexao.executar(sql)
    return flask.redirect('/produtos')

@app.route('/alterar_produto/<int:codigo>')
def alterar_produto(codigo):
    sql = f"SELECT codproduto, nome, preco FROM Produto WHERE codproduto = {codigo}"
    resultado = conexao.retornar(sql)
    resultado = {'codproduto': resultado[0][0], 'nome': resultado[0][1], 'preco': resultado[0][2]}

    sql = f"SELECT codproduto, nome, preco FROM Produto"
    produtos = conexao.retornar(sql)
    produtos = [{'codproduto': p[0], 'nome': p[1], 'preco': p[2]} for p in produtos]

    return flask.render_template('produtos.html', produtos=produtos, codigo=resultado['codproduto'], nome=resultado['nome'], preco=resultado['preco'])

@app.route('/pesquisar_produto', methods=['POST'])
def pesquisar_produto():
    nome = flask.request.form['termo']
    print(nome)
    sql = f"SELECT codproduto, nome, preco FROM Produto WHERE nome LIKE '%{nome}%'"
    produtos = conexao.retornar(sql)
    produtos = [{'codproduto': p[0], 'nome': p[1], 'preco': p[2]} for p in produtos]
    return flask.render_template('produtos.html', produtos=produtos)

@app.route('/clientes')
def clientes():
    sql = "SELECT codcliente, nome, endereco FROM Cliente"
    clientes = conexao.retornar(sql)
    if not clientes:
        return flask.render_template('clientes.html', clientes=[])
    clientes = [{'codcliente': c[0], 'nome': c[1], 'endereco': c[2]} for c in clientes]
    return flask.render_template('clientes.html', clientes=clientes)


@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    codigo = flask.request.form['codigo']
    print(f"codigo: {codigo}")
    sql = f"SELECT codcliente from Cliente where codcliente = {codigo}"
    resultado = conexao.retornar(sql)
    # se houver resultado, significa que o produto já existe, então vai alterar
    if resultado:
        nome = flask.request.form['nome']
        endereco = flask.request.form['endereco']
        sql = f"UPDATE Cliente SET nome = '{nome}', endereco = '{endereco}' WHERE codcliente = {codigo}"
        conexao.executar(sql)
        return flask.redirect('/clientes')

    nome = flask.request.form['nome']
    endereco = flask.request.form['endereco']

    sql = f"INSERT INTO Cliente (nome, endereco) VALUES ('{nome}', '{endereco}')"
    conexao.executar(sql)
    return flask.redirect('/clientes')

@app.route('/remover_cliente/<int:codigo>')
def remover_cliente(codigo):
    sql = f"DELETE FROM Cliente WHERE codcliente = {codigo}"
    conexao.executar(sql)
    return flask.redirect('/clientes')


@app.route('/alterar_cliente/<int:codigo>')
def alterar_cliente(codigo):
    sql = f"SELECT codcliente, nome, endereco FROM Cliente WHERE codcliente = {codigo}"
    resultado = conexao.retornar(sql)
    resultado = {'codcliente': resultado[0][0], 'nome': resultado[0][1], 'endereco': resultado[0][2]}

    sql = f"SELECT codcliente, nome, endereco FROM Cliente"
    clientes = conexao.retornar(sql)
    clientes = [{'codcliente': c[0], 'nome': c[1], 'endereco': c[2]} for c in clientes]

    return flask.render_template('clientes.html', clientes=clientes, codigo=resultado['codcliente'], nome=resultado['nome'], endereco=resultado['endereco'])

@app.route('/pesquisar_cliente', methods=['POST'])
def pesquisar_cliente():
    nome = flask.request.form['termo']
    sql = f"SELECT codcliente, nome, endereco FROM Cliente WHERE nome LIKE '%{nome}%'"
    clientes = conexao.retornar(sql)
    if not clientes:
        return flask.render_template('clientes.html', clientes=[])
    clientes = [{'codcliente': c[0], 'nome': c[1], 'endereco': c[2]} for c in clientes]
    return flask.render_template('clientes.html', clientes=clientes)


@app.route('/venda')
def venda():
    sql = "SELECT codproduto, nome, preco FROM Produto"
    produtos = conexao.retornar(sql)
    produtos = [{'codproduto': p[0], 'nome': p[1], 'preco': p[2]} for p in produtos]
    sql = "SELECT codcliente, nome, endereco FROM Cliente"
    clientes = conexao.retornar(sql)
    clientes = [{'codcliente': c[0], 'nome': c[1], 'endereco': c[2]} for c in clientes]
    return flask.render_template('venda.html', clientes=clientes, produtos=produtos)

@app.route('/busca_produto_venda', methods=['POST'])
def busca_produto_venda():
    sql = "SELECT codcliente, nome, endereco FROM Cliente"
    clientes = conexao.retornar(sql)
    clientes = [{'codcliente': c[0], 'nome': c[1], 'endereco': c[2]} for c in clientes]
    nome = flask.request.form['termo']
    sql = f"SELECT codproduto, nome, preco FROM Produto WHERE nome LIKE '%{nome}%'"
    produtos = conexao.retornar(sql)
    produtos = [{'codproduto': p[0], 'nome': p[1], 'preco': p[2]} for p in produtos]
    return flask.render_template('venda.html', clientes=clientes, produtos=produtos)

@app.route('/salvar_venda', methods=['POST'])
def salvar_venda():
    cliente = flask.request.form['cliente']
    produtos = flask.request.form.getlist('produtos[]')

    total = 0
    for item in produtos:
        codproduto, nome, preco, quantidade = item.split('|')
        print(f"codproduto: {codproduto}, nome: {nome}, preco: {preco}, quantidade: {quantidade}")
        preco = preco.replace(',', '.')
        quantidade = quantidade.replace(',', '.')

        preco = float(preco)
        quantidade = int(quantidade)

        total += preco * quantidade

    sql = (f"INSERT INTO venda (data, valor_total, codcliente) VALUES "
           f"(current_date, '{total}', {cliente})")
    print(sql)
    conexao.executar(sql)

    # Pega o id da venda que acabou de ser inserida
    sql = f"select codvenda from venda where codcliente = {cliente} order by codvenda desc limit 1"
    codvenda = conexao.retornar(sql)
    codvenda = codvenda[0][0]
    print(f"codvenda: {codvenda}")


    for item in produtos:
        codproduto, nome, preco, quantidade = item.split('|')
        sql = (f"INSERT INTO itemvenda (codvenda, codproduto, qtde, valor) VALUES "
               f"({codvenda}, {codproduto}, {quantidade}, {preco})")
        print(sql)
        conexao.executar(sql)

    return flask.redirect('/venda')

@app.route('/vendas')
def vendas():
    sql = "SELECT v.codvenda, v.codcliente, c.nome, v.data, v.valor_total FROM venda v JOIN cliente c ON v.codcliente = c.codcliente"
    vendas = conexao.retornar(sql)
    if not vendas:
        return flask.render_template('vendas.html', vendas=[])
    vendas = [{'codvenda': v[0], 'codcliente': v[1], 'nome': v[2], 'data': v[3], 'total': float(v[4])} for v in vendas]
    print(f"vendas: {vendas}")

    return flask.render_template("vendas.html", vendas=vendas)


@app.route('/visualizar_venda/<int:codvenda>')
def visualizar_venda(codvenda):
    sql = (f"SELECT i.codproduto, p.nome, i.qtde, i.valor "
           f"FROM itemvenda i JOIN produto p ON i.codproduto = p.codproduto "
           f"WHERE i.codvenda = {codvenda}")
    itens = conexao.retornar(sql)

    sql = "SELECT v.codvenda, v.codcliente, c.nome, v.data, v.valor_total FROM venda v JOIN cliente c ON v.codcliente = c.codcliente"
    vendas = conexao.retornar(sql)
    if not vendas:
        return flask.render_template('vendas.html', vendas=[])
    vendas = [{'codvenda': v[0], 'codcliente': v[1], 'nome': v[2], 'data': v[3], 'total': float(v[4])} for v in vendas]


    if not itens:
        return flask.render_template('vendas.html',vendas=vendas, itens=[])

    itens = [{'codproduto': i[0], 'nome': i[1], 'quantidade': i[2], 'preco': i[3]} for i in itens]
    print(f"itens: {itens}\nvendas: {vendas}")


    return flask.render_template('vendas.html', vendas=vendas, itens=itens)


@app.route('/pesquisar_venda', methods=['POST'])
def pesquisar_venda():
    termo = flask.request.form['termo']
    sql = (f"SELECT v.codvenda, v.codcliente, c.nome, v.data, v.valor_total "
           f"FROM venda v JOIN cliente c ON v.codcliente = c.codcliente "
           f"WHERE c.nome LIKE '%{termo}%'")
    vendas = conexao.retornar(sql)
    if not vendas:
        return flask.render_template('vendas.html', vendas=[])
    vendas = [{'codvenda': v[0], 'codcliente': v[1], 'nome': v[2], 'data': v[3], 'total': float(v[4])} for v in vendas]
    print(f"vendas: {vendas}")

    return flask.render_template("vendas.html", vendas=vendas)



if __name__ == '__main__':
    app.run(debug=True)