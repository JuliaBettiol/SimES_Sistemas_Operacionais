# -*- coding: utf-8 -*-
"""
Módulo M1 — Cache de blocos.

Implementação das políticas LRU e FIFO, com suporte
a write-through e write-back.
"""

from collections import OrderedDict


class Cache:
    nome = "?"

    def __init__(self, capacidade, escrita="write-back"):
        if escrita not in ("write-through", "write-back"):
            raise ValueError(
                "escrita deve ser 'write-through' ou 'write-back'"
            )

        if capacidade <= 0:
            raise ValueError("capacidade deve ser positiva")

        self.capacidade = capacidade
        self.escrita = escrita

        # Cada bloco armazenado possui um indicador de modificação.
        self.blocos = OrderedDict()

    def ler(self, bloco):
        raise NotImplementedError

    def inserir(self, bloco):
        raise NotImplementedError

    def escrever(self, bloco):
        raise NotImplementedError

    def sincronizar(self):
        # Retorna os blocos sujos e os marca como limpos.
        pendentes = [
            bloco
            for bloco, sujo in self.blocos.items()
            if sujo
        ]

        for bloco in pendentes:
            self.blocos[bloco] = False

        return pendentes

    def sujos(self):
        return sum(self.blocos.values())

    def _inserir_bloco(self, bloco, sujo):
        # Atualiza o bloco caso ele já esteja na cache.
        if bloco in self.blocos:
            self.blocos[bloco] = sujo
            return []

        expulsos = []

        # Se estiver cheia, remove o bloco mais antigo
        # segundo a ordem mantida pela política.
        if len(self.blocos) >= self.capacidade:
            vitima, estava_sujo = self.blocos.popitem(last=False)

            if estava_sujo:
                expulsos.append(vitima)

        self.blocos[bloco] = sujo

        return expulsos


class CacheLRU(Cache):
    nome = "LRU"

    def ler(self, bloco):
        if bloco not in self.blocos:
            return False

        # O bloco acessado passa a ser o mais recente.
        self.blocos.move_to_end(bloco)
        return True

    def inserir(self, bloco):
        if bloco in self.blocos:
            self.blocos.move_to_end(bloco)
            return []

        return self._inserir_bloco(bloco, False)

    def escrever(self, bloco):
        # Em write-through, a escrita vai imediatamente ao disco.
        sujo = self.escrita == "write-back"

        if bloco in self.blocos:
            self.blocos[bloco] = sujo
            self.blocos.move_to_end(bloco)
            expulsos = []
        else:
            expulsos = self._inserir_bloco(bloco, sujo)

        if self.escrita == "write-through":
            expulsos.append(bloco)

        return expulsos


class CacheFIFO(Cache):
    nome = "FIFO"

    def ler(self, bloco):
        # Na FIFO, a leitura não altera a ordem.
        return bloco in self.blocos

    def inserir(self, bloco):
        if bloco in self.blocos:
            return []

        return self._inserir_bloco(bloco, False)

    def escrever(self, bloco):
        sujo = self.escrita == "write-back"

        if bloco in self.blocos:
            self.blocos[bloco] = sujo
            expulsos = []
        else:
            expulsos = self._inserir_bloco(bloco, sujo)

        if self.escrita == "write-through":
            expulsos.append(bloco)

        return expulsos


CACHES = {
    "LRU": CacheLRU,
    "FIFO": CacheFIFO
}


def criar_cache(nome, capacidade, escrita):
    try:
        return CACHES[nome](capacidade, escrita)
    except KeyError:
        raise ValueError("cache desconhecida: %s" % nome)