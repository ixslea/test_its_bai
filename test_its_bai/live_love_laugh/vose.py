import random

class Vose:
    def __init__(self, plist):
        if not plist:
            raise ValueError("zero elements")

        self.items = [p[0] for p in plist]
        weights = [float(p[1]) for p in plist]
        
        if not any(weights):
            weights = [1.0] * len(weights)
        
        self.n = len(plist)
        self.Prob = [0.0] * self.n
        self.Alias = [0] * self.n
        
        self._build_alias_table(weights)
    
    def _build_alias_table(self, weights):
        total = sum(weights)
        scaled_weights = [w * self.n / total for w in weights]
        
        small = []
        large = []

        for i, sw in enumerate(scaled_weights):
            if sw < 1.0:
                small.append(i)
            else:
                large.append(i)
        
        while small and large:
            l = small.pop()
            g = large.pop()
            
            self.Prob[l] = scaled_weights[l]
            self.Alias[l] = g
            
            scaled_weights[g] = (scaled_weights[g] + scaled_weights[l]) - 1.0
            
            if scaled_weights[g] < 1.0:
                small.append(g)
            else:
                large.append(g)

        while large:
            g = large.pop()
            self.Prob[g] = 1.0
        
        while small:
            l = small.pop()
            self.Prob[l] = 1.0
    
    def get(self):
        if self.n == 0:
            return None
            
        i = random.randint(0, self.n - 1)
        if random.random() < self.Prob[i]:
            return self.items[i]
        else:
            return self.items[self.Alias[i]]