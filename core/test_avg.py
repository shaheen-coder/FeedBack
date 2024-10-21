import random
def b(): return random.randint(1,5)
a = 'cat'
datas = [
    {f'{a}_{i}':b() for i in range(11)},
    {f'{a}_{i}':b() for i in range(11)},
    {f'{a}_{i}':b() for i in range(11)}
]
print(f'data : {datas}')
sum_cat = {}
for data in datas:
    for key,value in data.items():
        try : sum_cat[key] += value
        except Exception as e : sum_cat[key] = value
print(f'sum data : {sum_cat}') 