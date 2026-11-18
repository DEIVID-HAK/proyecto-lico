import urllib.request
import json

data = json.dumps({
    'sku':'TEST2',
    'name':'TEST2',
    'category':'TEST',
    'alcohol_grade_abv':10,
    'volume_ml':500,
    'presentations':[{
        'name':'B',
        'barcode':'12345',
        'units_per_presentation':1,
        'cost':10,
        'retail_price':20,
        'wholesale_price':15
    }]
}).encode('utf-8')

req = urllib.request.Request('http://localhost:8000/api/products/', data=data, headers={'Content-Type': 'application/json'})

try:
    print(urllib.request.urlopen(req).read().decode('utf-8'))
except Exception as e:
    print(e.read().decode('utf-8'))
