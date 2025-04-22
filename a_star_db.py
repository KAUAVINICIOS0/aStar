"""
Gabriel Augusto Costeira da Silva Gonçalves RA:G766857
Kauã Vinícios Cruz Bezerra - G76JGG4
Marina da Silva Arruda de Moraes - F3573I8
"""


import pymysql
from pymysql import Error
import numpy as np

"""
METHOD FOR CONNECT TO DATABASE
"""
def get_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="Astar",
            password="Astar",
            database="db_AStar"
        )
        return connection
    except Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

"""
CLASS FOR CREATE VERTICE
"""
class Vertice:
    def __init__(self, id_city, name_city, distancia_objetivo):
        self.id = id_city
        self.rotulo = name_city
        self.visitado = False
        self.distancia_objetivo = distancia_objetivo
        self.adjacentes = []

    def adiciona_adjacente(self, adjacente):
        self.adjacentes.append(adjacente)

    def mostra_adjacentes(self):
        for i in self.adjacentes:
            print(i.vertice.rotulo, i.custo)

"""
CLASS FOR CREATE ADJACENT
"""
class Adjacente:
    def __init__(self, vertice, custo):
        self.vertice = vertice
        self.custo = custo
        self.distancia_aestrela = vertice.distancia_objetivo + self.custo

"""
CLASS FOR CREATE VECTOR ORDERED
"""
class VetorOrdenado:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.ultima_posicao = -1
        self.valores = np.empty(self.capacidade, dtype=object)

    def insere(self, adjacente):
        if self.ultima_posicao == self.capacidade - 1:
            print('Capacidade máxima atingida')
            return
        posicao = 0
        for i in range(self.ultima_posicao + 1):
            posicao = i
            if self.valores[i].distancia_aestrela > adjacente.distancia_aestrela:
                break
            if i == self.ultima_posicao:
                posicao = i + 1
        x = self.ultima_posicao
        while x >= posicao:
            self.valores[x + 1] = self.valores[x]
            x -= 1
        self.valores[posicao] = adjacente
        self.ultima_posicao += 1

    def imprime(self):
        if self.ultima_posicao == -1:
            print('O vetor está vazio')
        else:
            for i in range(self.ultima_posicao + 1):
                print(i, ' - ', self.valores[i].vertice.rotulo, ' - ',
                      self.valores[i].custo, ' - ',
                      self.valores[i].vertice.distancia_objetivo, ' - ',
                      self.valores[i].distancia_aestrela)

class AEstrela:
    def __init__(self, objetivo_id):
        self.objetivo_id = objetivo_id
        self.encontrado = False
        self.caminho = []
        self.custo_total = 0

    def buscar(self, atual):
        print('------------------')
        print('Atual: {}'.format(atual.rotulo))
        atual.visitado = True
        self.caminho.append(atual.rotulo)

        if atual.id == self.objetivo_id:
            self.encontrado = True
            print("Caminho encontrado:", " -> ".join(self.caminho))
            print(f"Custo total: {self.custo_total}")
            return True

        vetor_ordenado = VetorOrdenado(len(atual.adjacentes))
        for adjacente in atual.adjacentes:
            if not adjacente.vertice.visitado:
                vetor_ordenado.insere(adjacente)

        vetor_ordenado.imprime()

        if vetor_ordenado.ultima_posicao >= 0:
            proximo = vetor_ordenado.valores[0]
            self.custo_total += proximo.custo
            if self.buscar(proximo.vertice):
                return True
            self.custo_total -= proximo.custo

        self.caminho.pop()
        return False

def carregar_grafo(origem_id, destino_id):
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            # Busca todas as cidades
            cursor.execute("SELECT id_city, name_city FROM tb_city")
            cidades = cursor.fetchall()
            
            # Cria dicionário de vértices
            vertices = {}
            for cidade in cidades:
                # Calcula a distância em linha reta como heurística
                # Neste exemplo, usamos uma heurística simples baseada no ID
                # Quanto mais próximo do destino, menor a heurística
                heuristica = abs(cidade[0] - destino_id) * 10
                vertices[cidade[0]] = Vertice(cidade[0], cidade[1], heuristica)

            # Busca todas as distâncias
            cursor.execute("""
                SELECT fk_id_city_origin, fk_id_city_destination, distance 
                FROM tb_city_distance
            """)
            distancias = cursor.fetchall()

            # Adiciona adjacentes
            for origem, destino, distancia in distancias:
                if origem in vertices and destino in vertices:
                    vertices[origem].adiciona_adjacente(
                        Adjacente(vertices[destino], distancia)
                    )

            return vertices[origem_id] if origem_id in vertices else None

    except Error as err:
        print(f"Erro ao carregar grafo: {err}")
        return None
    finally:
        conn.close()

print("Cidades...") 
print("\n 1- Arad\n 2- Zerind\n 3- Oradea\n 4- Sibiu\n 5- Timisoara\n 6- Lugoj\n 7- Mehadia\n 8- Dobreta\n 9- Craiova\n 10- Rimnicu\n 11- Fagaras\n 12- Pitesti\n 13- Bucharest\n 14- Giurgiu\n") 


while True:
    origem_id = int(input("Digite a cidade de origem:"))
    destino_id = int(input("Digite a cidade de destino:"))

    if __name__ == "__main__":
        vertice_origem = carregar_grafo(origem_id, destino_id)
    if vertice_origem:
        busca = AEstrela(destino_id)
        if not busca.buscar(vertice_origem):
            print("Não foi possível encontrar um caminho até o destino")
    else:
        print("Não foi possível carregar o grafo") 


    question = input("Deseja continuar? (s/n):")
    if question == "n":
        break