#!/bin/python3

import re
import os
import subprocess

subprocess.run("rm *.pdf", shell = True)
print("Deletion is done, remaining files:")
subprocess.run("ls .", shell = True)
subprocess.run("cd munkapad;pwd", shell = True)

def type_of_name(element):
    return re.split(r'_|\.', element)[0]

def number_of_name(element):
    return re.split(r'_|\.', element)[1]

# l = nq + r
def parser(lista,egesz):
    l = len(lista)
    n = l // egesz
    r = l - n * egesz
    # print(f'{l} = {n} * {egesz} + {r}')
    parsed_list = []
    # for i in range(n):
        # print([lista[j] for j in range(i * egesz , (i + 1) * egesz)])
    # print([lista[i] for i in range(n * egesz, n * egesz + r)])
    for i in range(n):
        parsed_list.append([lista[j] for j in range(i * egesz , (i + 1) * egesz)])
    parsed_list.append([lista[i] for i in range(n * egesz, n * egesz + r)])
    return parsed_list 

def name_type_number(lista):
    return [[i, type_of_name(i), number_of_name(i)] for i in lista]

def type_number(file_lista):
    types = []
    separated_file_list = name_type_number(file_lista)
    for i in separated_file_list:
        if i[1] not in types:
            types.append(i[1])
    # for i in types:
    #     print(i)
    type_number = dict.fromkeys(types, 0)
    for i in separated_file_list:
        type_number[i[1]] += 1
    return type_number

def pdfuniter_strings(file_lista,egesz):
    dict_of_type_number = type_number(file_lista)
    types = dict_of_type_number.keys()
    pdfuniter_strings = []
    for i in types:
        for j in parser(list(range(1,dict_of_type_number[i] + 1)),egesz):
            string = f"zsh -c 'pdfunite munkapad/{i}_{{{j[0]:04d}..{j[-1]:04d}}}.pdf {i}_{j[0]:04d}_{j[-1]:04d}.pdf'"
            pdfuniter_strings.append(string)
    return pdfuniter_strings

path = './munkapad/'

file_names = [file for file in os.listdir(path)]
# for i in file_names:
#     print(i)

# separated_file_names = name_type_number(file_names)
# for i in separated_file_names:
#     print(i)

types_of_files = type_number(file_names)
print(types_of_files)

pdfuniter_strings = pdfuniter_strings(file_names,40)
for i in pdfuniter_strings:
    print(i)

for i in pdfuniter_strings:
    subprocess.run(i, shell = True)
