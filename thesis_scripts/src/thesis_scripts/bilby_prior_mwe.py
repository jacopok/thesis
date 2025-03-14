from bilby.core.prior.dict import PriorDict
from bilby.core.prior import Uniform
from bilby.gw.prior import BNSPriorDict

p = PriorDict(
    {'a': Uniform(0, 2, name='a')}
)

print(p.cdf({'a': 0.5}))

p2 = BNSPriorDict()

sample = p2.sample()

print(sample)
print(p2.cdf(sample))