from dataclasses import dataclass, field, astuple

@dataclass
class Data:
    n: int = field(init=False) # number of towns (number of nodes)
    m: int = field(init=False) # number of roads connecting the towns (number of edges)
    p: int = field(init=False) # number of different kinds of monsters
    k: int = field(init=False) # number of blacksmiths

    K: list = field(init=False, default_factory=list) # list of bit masks, that represents swords that can be obtained in every town
    G: list = field(init=False, default_factory=list) # weighted graph that represents towns and monsters on the roads
    
    def read_data(self, file):
        try:
            self.n, self.m, self.p, self.k = [int(x) for x in file.readline().split()]
            self.K = [0] * (self.n + 1)
            self.G = [[] for i in range((self.n + 1))]
        except Exception as e:
            print(e)
        else:
            # reading data for blacksmiths in every town
            for i in range(self.k):
                values = [int(x) for x in file.readline().split()]
                w, q = values[:2]
                bit_mask = self.K[w] # swords that can be already obtained in w-th town
                for j in values[2:]:
                    bit_mask |= (1 << j)

                self.K[w] = bit_mask

            # reading data for edges with weights and monsters on the roads
            for i in range(self.m):
                values = [int(x) for x in file.readline().split()]
                v, w, t, s = values[:4]
                bit_mask = 0 # kinds of monsters 
                for j in values[4:]:
                    bit_mask |= (1 << j)
                
                self.G[v].append((w, t, bit_mask))
                self.G[w].append((v, t, bit_mask))

    def __iter__(self):
        return iter(astuple(self))