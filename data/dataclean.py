import json
import numpy as np

pathsec = "/Users/cosmonana/Projects/Lifetask/ChinesePoemTranslator/data/poetry-master/data/aio/LCPoetry"

translatecount = 0

transes = []
paratranses = []
norm = 0
for i in range(8):
    path = pathsec+str(i+1)+".json"
    f = open(path)
    data = json.load(f)
    for d in data:
        if 'fanyi' in d:
            trans = {"id":translatecount, "translation": {"ancient":d['content'], "modern":d['fanyi']}}
            transes.append(trans)
            translatecount += 1

            ancient = d['content'].splitlines()
            modern = d['fanyi'].splitlines()
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

print("Examples of extracted pairs:")
print([paratranses[i] for i in np.random.choice(norm, 3)])


with open('poempretranslate.json', 'w', encoding='utf8') as t:
    s = json.dumps(transes, ensure_ascii=False, indent=2)
    t.write(f"{s}\n")

countpairs = 0
pairforwards = []
pairbackwards = []
odds = 0
for pairs in paratranses:
    if "注释" in [p[1] for p in pairs]:
        print(odds, pairs)
        odds += 1
        continue
    for p in pairs:
        pforward = {"id":countpairs, "translation": {"modern":p[1], "ancient":p[0]}}
        pbackward = {"id":countpairs, "translation": {"ancient":p[0], "modern":p[1]}}
        pairforwards.append(pforward)
        pairbackwards.append(pbackward)
        countpairs += 1

with open('poemtranslate_md_an.json', 'w', encoding='utf8') as t:
    s = json.dumps(pairforwards, ensure_ascii=False, indent=2)
    t.write(f"{s}\n")
with open('poemtranslate_an_md.json', 'w', encoding='utf8') as t:
    s = json.dumps(pairbackwards, ensure_ascii=False, indent=2)
    t.write(f"{s}\n")
print("Number of total sentence pairs: ", countpairs)
print("Number of odds: ", odds)
