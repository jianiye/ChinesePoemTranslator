import json
import numpy as np
import re

pathsec = "/Users/cosmonana/Projects/Lifetask/ChinesePoemTranslator/data/poetry-master/data/aio/LCPoetry"

poemonly = True
translatecount = 0

paratranses = []
norm = 0
for i in range(8):
    path = pathsec+str(i+1)+".json"
    f = open(path)
    data = json.load(f)
    for d in data:
        if 'fanyi' in d:
            if len(d['content']) > 150:
                continue
            trans = {"id":translatecount, "translation": {"ancient":d['content'], "modern":d['fanyi']}}
            translatecount += 1

            # ancient = d['content'].split("。？！")
            # modern = d['fanyi'].split("。？！")
            ancient = re.findall('(?=\S)[^。？！\n]+(?<=\S)', d['content'])
            modern = re.findall('(?=\S)[^。？！\n]+(?<=\S)', d['fanyi'])

            for prompt in ["散译", "韵译", "译文一", "其一：", "其一", "白话译文"]:
                while prompt in modern:
                    k = modern.index(prompt)
                    modern[k] = "译文"
            ancient = list(filter(('').__ne__, ancient))
            modern = list(filter(('').__ne__, modern))
            if "译文" in modern:
                k = len(modern) - 1 - modern[::-1].index("译文")
                if len(modern[k+1]) > 5 and k + len(ancient) < len(modern):
                    norm += 1
                    paratranses.append([(a, modern[k+1+i]) for i, a in enumerate(ancient)])
                else:
                    continue
                    # print(modern[k:min(k+4, len(modern))])
                    # print(ancient)
                    # print('\n')

    print("Number of total Poems:", translatecount)
    print("Number of poems with translation:", norm)

print("Examples of extracted contents:")
print([paratranses[i] for i in np.random.choice(norm, 3)])

countpairs = 0
pairforwards = []
pairbackwards = []
odds = 0
for pairs in paratranses:
    for p in pairs:
        if "注释" in p[1]:
            #print(odds, pairs)
            odds += 1
            break
        if poemonly:
            if len(p[0]) != 15 and  len(p[0]) != 11: continue
        pforward = {"id":countpairs, "translation": {"modern":p[1], "ancient":p[0]}}
        pbackward = {"id":countpairs, "translation": {"ancient":p[0], "modern":p[1]}}
        pairforwards.append(pforward)
        pairbackwards.append(pbackward)
        countpairs += 1
if poemonly:
    with open('poemonly_sentence_translate_md_an.json', 'w', encoding='utf8') as t:
        s = json.dumps(pairforwards, ensure_ascii=False, indent=2)
        t.write(f"{s}\n")
    with open('poemonly_sentence_translate_an_md.json', 'w', encoding='utf8') as t:
        s = json.dumps(pairbackwards, ensure_ascii=False, indent=2)
        t.write(f"{s}\n")
else:
    with open('poem_sentence_translate_md_an.json', 'w', encoding='utf8') as t:
        s = json.dumps(pairforwards, ensure_ascii=False, indent=2)
        t.write(f"{s}\n")
    with open('poem_sentence_translate_an_md.json', 'w', encoding='utf8') as t:
        s = json.dumps(pairbackwards, ensure_ascii=False, indent=2)
        t.write(f"{s}\n")

print("Number of total sentence pairs: ", countpairs)
print("Number of odds: ", odds)
print("Examples of extracted sentence pairs:")
for i in np.random.choice(countpairs, 20):
    print(pairforwards[i]['translation'])
