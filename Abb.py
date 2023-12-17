from collections import deque

class Node:
    def __init__(self, chave, posicao):
        self.chave = chave
        self.posicao = posicao
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    def __init__(self, iterator=None):
        self.raiz = None
        if iterator:
            for item in iterator:
                self.inserir(item)

    def copia_arvore(self, no):
        if not no:
            return None
        novo_no = Node(no.chave, no.posicao)
        novo_no.esquerda = self.copia_arvore(no.esquerda)
        novo_no.direita = self.copia_arvore(no.direita)
        return novo_no

    def inserir(self, chave, posicao):
        self.raiz = self.inserir_recursiva(self.raiz, chave, posicao)

    def inserir_recursiva(self, no, chave, posicao):
        if not no:
            return Node(chave, posicao)
        if chave < no.chave:
            no.esquerda = self.inserir_recursiva(no.esquerda, chave, posicao)
        elif chave > no.chave:
            no.direita = self.inserir_recursiva(no.direita, chave, posicao)
        return no

    def remover(self, chave):
        self.raiz = self.remocao_recursiva(self.raiz, chave)

    def remocao_recursiva(self, no, chave):
        if not no:
            return None

        if chave < no.chave:
            no.esquerda = self.remocao_recursiva(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self.remocao_recursiva(no.direita, chave)
        else:
            if not no.esquerda:
                return no.direita
            elif not no.direita:
                return no.esquerda

            no.chave = self._min_valor_no(no.direita).chave
            no.direita = self.remocao_recursiva(no.direita, no.chave)

        return no

    def _min_valor_no(self, no):
        while no.esquerda:
            no = no.esquerda
        return no

    def preordem(self):
        resultado = []
        self._preordem(self.raiz, resultado)
        return resultado

    def _preordem(self, raiz, resultado):
        if raiz:
            resultado.append(raiz.chave)
            self._preordem(raiz.esquerda, resultado)
            self._preordem(raiz.direita, resultado)

    def emordem(self):
        resultado = []
        self._emordem(self.raiz, resultado)
        return resultado

    def _emordem(self, raiz, resultado):
        if raiz:
            self._emordem(raiz.esquerda, resultado)
            resultado.append(raiz.chave)
            self._emordem(raiz.direita, resultado)

    def posordem(self):
        resultado = []
        self._posordem(self.raiz, resultado)
        return resultado

    def _posordem(self, raiz, resultado):
        if raiz:
            self._posordem(raiz.esquerda, resultado)
            self._posordem(raiz.direita, resultado)
            resultado.append(raiz.chave)

    def buscar_posicao(self, chave):
        return self._buscar_posicao(self.raiz, chave)

    def _buscar_posicao(self, no, chave):
        if not no:
            return None
        
        if chave == no.chave:
            return no.posicao
        
        if chave < no.chave:
            return self._buscar_posicao(no.esquerda, chave)

        return self._buscar_posicao(no.direita, chave)


class Registro:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class AcessoDadosABB:
    def __init__(self):
        self.arvore_indices = ArvoreBinariaBusca()

    def inserir_registro(self, registro, posicao):
        """Inserindo na ABB e escrevendo no arquivo de registros"""
        self.arvore_indices.inserir(registro.cpf, posicao)
        with open("arquivo_registros.txt", "a") as arquivo_registros:
            arquivo_registros.write(f"{registro.cpf},{registro.nome},{registro.data_nascimento}\n")

    def buscar_registro_por_chave(self, chave):
        posicao_registro = self.arvore_indices.buscar_posicao(chave)
        if posicao_registro is not None:
            with open("arquivo_registros.txt", "r") as arquivo_registros:
                arquivo_registros.seek(posicao_registro)
                registro = arquivo_registros.readline().strip().split(',')
                print("Registro Encontrado:")
                print(f"CPF: {registro[0]}")
                print(f"Nome: {registro[1]}")
                print(f"Data de Nascimento: {registro[2]}")
        else:
            print("Registro não encontrado.")

def criar_arquivo_registros_e_indice():
    """ Lista de registros (EDL)"""
    registros = [
        Registro("12345678901", "João", "08/11/2003"),
        Registro("98765432109", "Maria", "15/03/2002"),
        Registro("11223344556", "Carlos", "30/05/2005"),
      
    ]

    """ Criação ABB e arquivo de registros """
    acesso_dados = AcessoDadosABB()
    for i, registro in enumerate(registros):
        acesso_dados.inserir_registro(registro, i)

    """ Salvando a ABB em um arquivo de índice """
    with open("arquivo_indice.txt", "w") as arquivo_indice:
        """ Percurso em ordem para salvar na sequência ordenada das chaves"""
        def salvar_em_ordem(no):
            if no:
                salvar_em_ordem(no.esquerda)
                arquivo_indice.write(f"{no.chave},{no.posicao}\n")
                salvar_em_ordem(no.direita)

        salvar_em_ordem(acesso_dados.arvore_indices.raiz)
        
#ExemploFuncionament0:
criar_arquivo_registros_e_indice()
acesso_dados = AcessoDadosABB()
novo_registro = Registro("16376568743", "Sofia", "14/07/2004")
acesso_dados.inserir_registro(novo_registro, 3)

acesso_dados = AcessoDadosABB()
novo_registro1 = Registro("11111111111", "Matheus", "06/03/2004")
acesso_dados.inserir_registro(novo_registro1, 1)

chave_busca1= "11111111111"
acesso_dados.buscar_registro_por_chave(chave_busca1)
"Matheus 06/03/2004"

chave_busca1 = "55555555555"
acesso_dados.buscar_registro_por_chave(chave_busca2) 
"Registro não encontrado"

chave_remover = "11223344556"

