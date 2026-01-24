from queue import PriorityQueue

def __h_score(posicao_inicial, posicao_final):
    distancia_x = abs(posicao_inicial[0] - posicao_final[0])
    distancia_y = abs(posicao_inicial[1] - posicao_final[1])    
    return distancia_x + distancia_y

def expandir_vizinhos(posicao_atual,cenario,):
    vizinhos = []
    linha, coluna = posicao_atual
    tamanho = cenario.tamanho
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dl,dc in movimentos:
        nova_linha,nova_coluna = linha + dl,coluna + dc
        
        if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
            vizinhos.append((nova_linha,nova_coluna))
    return vizinhos

def a_estrela(inicio, destino, cenario, obstaculos=None):
    if obstaculos is None:
        obstaculos = []

    
    inicio_tupla = tuple(inicio) if isinstance(inicio, list) else inicio
    destino_tupla = tuple(destino) if isinstance(destino, list) else destino
    
    fila_aberta = PriorityQueue()
    fila_aberta.put((0, inicio_tupla))
    custos_g = {inicio_tupla: 0}
    custos_f = {inicio_tupla: __h_score(inicio_tupla, destino_tupla)}
    predecessores = {inicio_tupla: None}

    while not fila_aberta.empty():
        _, posicao_atual = fila_aberta.get()

        if posicao_atual == destino_tupla:
            caminho = []
            while posicao_atual is not None:
                caminho.append(list(posicao_atual)) 
                posicao_atual = predecessores[posicao_atual]
            return caminho[::-1]

        for vizinho in expandir_vizinhos(posicao_atual, cenario):
            vizinho_tupla = tuple(vizinho) if isinstance(vizinho, list) else vizinho
            
            if vizinho in obstaculos:
                continue

            custo_g_temp = custos_g[posicao_atual] + 1

            if vizinho_tupla not in custos_g or custo_g_temp < custos_g[vizinho_tupla]:
                predecessores[vizinho_tupla] = posicao_atual
                custos_g[vizinho_tupla] = custo_g_temp
                custos_f[vizinho_tupla] = custo_g_temp + __h_score(vizinho_tupla, destino_tupla)
                fila_aberta.put((custos_f[vizinho_tupla], vizinho_tupla))

    return None
def converter_direcao(posicao_atual, proxima_posicao):
    linha_atual, coluna_atual = posicao_atual
    linha_proxima, coluna_proxima = proxima_posicao

    if linha_proxima < linha_atual:
        return 'CIMA'
    elif linha_proxima > linha_atual:
        return 'BAIXO'
    elif coluna_proxima < coluna_atual:
        return 'ESQUERDA'
    elif coluna_proxima > coluna_atual:
        return 'DIREITA'
    return 'CIMA'