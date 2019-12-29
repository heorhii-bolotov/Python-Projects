import requests
from decimal import Decimal
from W2T2 import convert


correct = Decimal('3754.8057')
result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
if result == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result, correct))
