import sqlite3
import os
import pandas as pd
import time
import shutil

def clear():
    os.system('cls')

def createDatabase():
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def createDirectories():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.makedirs(os.getcwd()+'\\backups', exist_ok=True)
    os.makedirs(os.getcwd()+'\\data', exist_ok=True)
    os.makedirs(os.getcwd()+'\\exports', exist_ok=True)
    
def exportCSV():
    conn = sqlite3.connect('.\\data\\livraria.db')
    
    df = pd.read_sql_query('SELECT * FROM livros', conn)
    
    df.to_csv('.\\exports\\livros_exportados.csv', index=False)
    
    conn.close()
    
def importCSV():
    conn = sqlite3.connect('.\\data\\livraria.db')
    
    df = pd.read_csv('.\\exports\\livros_exportados.csv')
    df.drop('id', inplace=True, axis=1) 
    df.to_sql('livros', conn, if_exists='append', index=False)
    
    conn.close()
    
def createBkp():
    shutil.copyfile('.\\data\\livraria.db', f'.\\backups\\{str(int(time.time()))}.db')
    
def addBook():
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    
    title = input("Título: ")
    author = input("Autor: ")
    publish = int(input("Ano de publicação: "))
    price = float(input("Preço: "))
    
    c.execute('''
            INSERT INTO livros (titulo, autor, ano_publicacao, preco)
            VALUES (?, ?, ?, ?)
            ''', (title, author, publish, price))
    conn.commit()
    conn.close()
    createBkp()
    
def searchAuthor():
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    
    author = input("Autor: ")
    
    c.execute('SELECT * FROM livros where autor = ?', (author,))
    books = c.fetchall()
    for book in books:
        print(f"ID: {book[0]:<3}Título: {book[1]:<10}Autor: {book[2]:<10}Ano: {book[3]:<6}Preço: R${book[4]:<8}")
    
    conn.commit()
    conn.close()
    input("Aperte Enter para continuar...")
    
def allBooks():
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM livros')
    books = c.fetchall()
    for book in books:
        print(f"ID: {book[0]:<3}Título: {book[1]:<10}Autor: {book[2]:<10}Ano: {book[3]:<6}Preço: R${book[4]:<8}")
    
    conn.commit()
    conn.close()
    input("Aperte Enter para continuar...")
    
def updatePrice():
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    
    title = input("Título do livro para atualizar o preço: ")
    price = float(input("Novo preço: "))
    
    c.execute('''
        UPDATE livros SET preco = ? WHERE titulo = ?
    ''', (price, title))
    
    conn.commit()
    conn.close()
    createBkp()

def deleteBook():
    
    conn = sqlite3.connect('.\\data\\livraria.db')
    c = conn.cursor()
    
    title = input("Título do livro para remover: ")
    
    c.execute('''
        DELETE FROM livros WHERE titulo = ?
    ''', (title,))
    
    conn.commit()
    conn.close()
    createBkp()

# Menu principal
def menu():
    createDirectories()
    createDatabase()
    while True:
        clear()
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar por autor")
        print("6. Exportar para CSV")
        print("7. Importar de CSV")
        print("8. Criar backup do banco")
        print("9. Sair")
        op = input("Escolha uma opção: ")

        if op == '1':
            addBook()
        elif op == '2':
            allBooks()
        elif op == '3':
            updatePrice()
        elif op == '4':
            deleteBook()
        elif op == '5':
            searchAuthor()
        elif op == '6':
            exportCSV()
        elif op == '7':
            importCSV()
        elif op == '8':
            createBkp()
        elif op == '9':
            break
        else:
            print("Opção inválida!")

# Executar o menu
menu()