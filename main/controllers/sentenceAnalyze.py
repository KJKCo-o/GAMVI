from konlpy.tag import Komoran

tag_all = ['NNB', 'NNG', 'NNP', 'NP', 'VV', 'VA', 'MAG', 'MAJ']
tag_noun = ['NNB', 'NNG', 'NNP', 'NP']
tag_verb = ['VV']
tag_adj = ['VA']
tag_adv = ['MAG', 'MAJ']


def tokenizer(textData):
    kom = Komoran()
    tokenList = kom.pos(textData)
    validToken = []

    for token in tokenList:
        if token[1] in tag_all:  # 명사, 동사, 형용사, 부사인지 확인
            if token[1] in tag_noun:
                validToken.append((token[0], "명사"))
            elif token[1] in tag_verb:
                validToken.append((token[0], "동사"))
            elif token[1] in tag_adj:
                validToken.append((token[0], "형용사"))
            elif token[1] in tag_adv:
                validToken.append((token[0], "부사"))
    return validToken


def lemmatizer(validToken):
    lemmaList = []
    for token in validToken:
        if token[1] == "동사" or token[1] == "형용사":  # 명사, 동사, 형용사, 부사인지 확인
            lemmaList.append(token[0] + "다")
    return lemmaList
