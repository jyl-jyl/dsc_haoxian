import os.path
import csv
import sys

def gen_full_single(name):
    if_start = 0
    file = open(os.path.join('./benchmarks', name), 'r')
    count = 0
    set_fullviews = set()
    set_publicfuncs = set()
    while True:
        count += 1
        line = file.readline()
        if line.startswith('//') or line.startswith('.'):
            if_start = 1
        if if_start == 0:
            continue
        if line.startswith('.decl') or line.startswith('.public') or line.startswith('.violation'):
            phrase_1 = line.split(' ')[1]
            phrase_2 = phrase_1.split('(')[0].strip('*').strip('\n')
            phrase_2 = phrase_2.strip()
            if phrase_2.startswith('recv'):
                set_publicfuncs.add(phrase_2)
                set_publicfuncs.add(phrase_2.split('_')[1])
            set_fullviews.add(phrase_2)
        elif line.strip() != '' and line != '\n' and not line.startswith('//') and not line.startswith('\n'):
            print('line con2: ', line)
            head = line.split(':-')[0].split('(')[0]
            set_fullviews.add(head)
            bodies = line.split(':-')[1].split(', ')
            # print('bodies', bodies)
            for each in bodies:
                each.strip(' ')
                index_1 = each.find(': ')
                index_2 = each.find('(')
                if index_1 != index_2 and ":=" not in each:
                    body = each[index_1 + 1:index_2]
                    set_fullviews.add(body.strip())
        if not line:
            break
    # do not materialize constructor
    set_fullviews.remove('constructor')
    # do not materialize public function and function triggers
    set_fullviews = set_fullviews - set_publicfuncs
    file.close()
    # write file to csv
    contract_name = name.split('.')[0]
    filename = f"{contract_name}_full.csv"
    path = os.path.join('./full_csv', filename)
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(list(set_fullviews))


gen_full_single(sys.argv[1])
