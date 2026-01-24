from typing import Dict, Tuple, Set, List
import random

class Memoria:
    def __init__(self):
        self.visitadas = set()
        self.seguras = set()
        self.suspeitas_poco = set()
        self.suspeitas_wumpus = set()
        self.com_ouro = set()
        self.ouro_coletado = set()
        self.wumpus_confirmado = set()
        self.wumpus_morto = set()
        self.poco_confirmado = set()
        self.visitadas.add((0, 0))
        self.seguras.add((0, 0))
    
    def atualizar(self, pos, percepcao, tamanho):
        self.visitadas.add(pos)
        self.seguras.add(pos)
        
        if 'b' in percepcao:
            self.com_ouro.add(pos)
        
        self._inferir(pos, percepcao, tamanho)


    def confirmar_morte(self,pos,tipo):
        self.visitadas.add(pos)
        self.seguras.discard(pos)

        if tipo =="W":
            self.wumpus_confirmado.add(pos)
            self.seguras.discard(pos)
        else:
            self.poco_confirmado.add(pos)
            self.suspeitas_poco.add(pos)
            self.suspeitas_wumpus.discard    

    def _obter_vizinhos(self,pos,tamanho):
        linha, coluna = pos
        vizinhos = []
        if linha>0 :vizinhos.append((linha-1,coluna))
        if linha<tamanho-1:vizinhos.append((linha+1,coluna))
        if coluna > 0: vizinhos.append((linha,coluna-1))
        if coluna< tamanho-1:vizinhos.append((linha,coluna+1))
        return vizinhos

    
    def _inferir(self, pos, percepcao, tamanho):
       
        vizinhos = self._obter_vizinhos(pos,tamanho)
        
        if 'v' not in percepcao:
            for v in vizinhos:
                self.suspeitas_poco.discard(v)
                if v not in self.suspeitas_wumpus:
                    self.seguras.add(v)
        
        if 'f' not in percepcao:
            for v in vizinhos:
                self.suspeitas_wumpus.discard(v)
                if v not in self.suspeitas_poco:
                    self.seguras.add(v)
        
        if 'v' in percepcao:
            for v in vizinhos:
                if v not in self.seguras:
                    self.suspeitas_poco.add(v)
        
        if 'f' in percepcao:
            for v in vizinhos:
                if v not in self.seguras:
                    self.suspeitas_wumpus.add(v)
    
    def marcar_ouro_coletado(self, pos):
        self.ouro_coletado.add(pos)
        if pos in self.com_ouro:
            self.com_ouro.remove(pos)
    
    def marcar_wumpus_morto(self, pos):
        if pos in self.wumpus_confirmado:
            self.wumpus_confirmado.remove(pos)
        self.wumpus_morto.add(pos)
        self.seguras.add(pos)
       


    def get_seguras_nao_visitadas(self):
        return [s for s in self.seguras if s not in self.visitadas]
    
    def get_objetivos(self):
        objetivos = []
        for sala in self.com_ouro:
            if sala not in self.ouro_coletado:
                objetivos.append(sala)
        
        for sala in self.get_seguras_nao_visitadas():
            objetivos.append(sala)
        
        return objetivos
    
    def get_obstaculos(self):
        return list((self.suspeitas_poco | self.suspeitas_wumpus) - self.seguras)
    
    def calcular_risco(self, pos):
        risco = 0
        if pos in self.wumpus_morto:
            return 0
        if pos in self.wumpus_confirmado or pos in self.poco_confirmado:
            return 100
        if pos in self.suspeitas_wumpus:
            risco += 5
        if pos in self.suspeitas_poco:
            risco += 3
        if pos not in self.seguras:
            risco += 1
        return risco
    
    def get_melhor_direcao(self, pos_atual, direcoes, tamanho):
        if not direcoes:
            return 'CIMA'
        
        linha, coluna = pos_atual
        
        for direcao in direcoes:
            if direcao == 'CIMA':
                destino = (linha - 1, coluna)
            elif direcao == 'BAIXO':
                destino = (linha + 1, coluna)
            elif direcao == 'ESQUERDA':
                destino = (linha, coluna - 1)
            else:
                destino = (linha, coluna + 1)
            
            if not (0 <= destino[0] < tamanho and 0 <= destino[1] < tamanho):
                continue
            
            if destino in self.com_ouro:
                return direcao
        
        for direcao in direcoes:
            if direcao == 'CIMA':
                destino = (linha - 1, coluna)
            elif direcao == 'BAIXO':
                destino = (linha + 1, coluna)
            elif direcao == 'ESQUERDA':
                destino = (linha, coluna - 1)
            else:
                destino = (linha, coluna + 1)
            
            if not (0 <= destino[0] < tamanho and 0 <= destino[1] < tamanho):
                continue
            
            if destino in self.seguras and destino not in self.visitadas:
                return direcao
        
        for direcao in direcoes:
            if direcao == 'CIMA':
                destino = (linha - 1, coluna)
            elif direcao == 'BAIXO':
                destino = (linha + 1, coluna)
            elif direcao == 'ESQUERDA':
                destino = (linha, coluna - 1)
            else:
                destino = (linha, coluna + 1)
            
            if not (0 <= destino[0] < tamanho and 0 <= destino[1] < tamanho):
                continue
            
            if destino in self.seguras:
                return direcao
        
        direcoes_validas = []
        for direcao in direcoes:
            if direcao == 'CIMA':
                destino = (linha - 1, coluna)
            elif direcao == 'BAIXO':
                destino = (linha + 1, coluna)
            elif direcao == 'ESQUERDA':
                destino = (linha, coluna - 1)
            else:
                destino = (linha, coluna + 1)
            
            if not (0 <= destino[0] < tamanho and 0 <= destino[1] < tamanho):
                continue
            
            if destino not in self.suspeitas_wumpus and destino not in self.suspeitas_poco:
                direcoes_validas.append(direcao)
        
        if direcoes_validas:
            return random.choice(direcoes_validas)
        
        return random.choice(direcoes)
    
    def reset(self):
        self.__init__()
    
    def __str__(self):
        if not self.visitadas:
            return "Memória vazia"
        
        linhas = [pos[0] for pos in self.visitadas]
        colunas = [pos[1] for pos in self.visitadas]
        
        min_linha = min(linhas)
        max_linha = max(linhas)
        min_coluna = min(colunas)
        max_coluna = max(colunas)
        
        resultado = []
        for i in range(min_linha, max_linha + 1):
            linha_str = []
            for j in range(min_coluna, max_coluna + 1):
                pos = (i, j)
                simbolo = '·'
                
                if pos in self.visitadas:
                    simbolo = 'V'
                
                if pos in self.seguras and pos not in self.visitadas:
                    simbolo = 'S'
                
                if pos in self.suspeitas_poco:
                    simbolo = '!'
                
                if pos in self.suspeitas_wumpus:
                    simbolo = '?'
                
                if pos in self.com_ouro:
                    simbolo = 'O'
                
                if pos == (0, 0):
                    simbolo = 'I'
                
                linha_str.append(simbolo)
            
            resultado.append(' '.join(linha_str))
        
        resultado.append("")
        resultado.append(f"Visitadas: {len(self.visitadas)}")
        resultado.append(f"Seguras: {len(self.seguras)}")
        resultado.append(f"Suspeitas Poço: {len(self.suspeitas_poco)}")
        resultado.append(f"Suspeitas Wumpus: {len(self.suspeitas_wumpus)}")
        resultado.append(f"Ouro: {len(self.com_ouro)}")
        
        return '\n'.join(resultado)