import json
import csv
import numpy as np


# Valores, localidad, genero, edad, #month

total_total = 119530753
states = {}
states_keys = []
age_ranges = ['00-04','05-09','10-14','15-19','20-24','25-29',
    '30-34','35-39','40-44','45-49','50-54','55-59','60-64',
    '70-74','75']
states_list = {}

for i in range(32):
    key = "%02d" % (i + 1)
    for g in ('f','m'):
        for age_range in age_ranges:
            states_keys.append(key)
            states[key+'-'+g+'-'+age_range] = 0

with open('data.csv', 'rb') as file:
    spanreader = csv.reader(file, delimiter=',')
    for row in spanreader:
        state_key = row[0][0:2]
        arr_tmp = row[0].split(' ')
        if len(arr_tmp) > 1:
            state_name = arr_tmp[1]
        else:
            state_name = "unknow"

        age_range = row[1].split(' ')[0]
        is_valor = row[2] == 'Valor'
        total = row[3].replace(',','')
        male = row[4].replace(',','')
        female = row[5].replace(',','')

        states_list[state_key] = state_name

        if (state_key in states_keys) and is_valor and (age_range in age_ranges):
            states[state_key+'-f-'+age_range] = float(female) * 100 / total_total
            states[state_key+'-m-'+age_range] = float(male) * 100 / total_total

keys = []
probability = []
for s in states:
    keys.append(s)
    probability.append(states[s]/100)
err = 1 - sum(probability)
keys.append("err")
probability.append(err)


while True:
    result = np.random.choice(keys, p=probability)
    if result == "err":
        continue
    break


result = result.split("-")

print("Estado: " + states_list[result[0]])
if result[1] == 'f':
    print("Genero: femenino")
else:
    print("Genero: masculino")

if len(result) == 4:
    edad = np.random.randint(int(result[2]), int(result[3]))
else:
    edad = np.random.randint(int(result[2]), 80)

print("Edad: " + str(edad))