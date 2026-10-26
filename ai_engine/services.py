import re

COUNTRIES=[
"India","China","Pakistan","USA",
"Russia","Ukraine","Israel","Iran"
]

KEYWORDS={

"Defence":[
"army","military","missile",
"navy","air force","border"
],

"Cyber":[
"cyber","hacker","malware",
"ransomware","attack"
],

"Space":[
"satellite","space","rocket",
"launch","orbit"
]

}

THREAT_WORDS={

"war":30,
"attack":25,
"missile":20,
"conflict":20,
"strike":25,
"terror":30,
"cyber":15,
"drone":15

}


def detect_country(text):

    for c in COUNTRIES:

        if c.lower() in text.lower():
            return c

    return None


def detect_category(text):

    text=text.lower()

    for cat,words in KEYWORDS.items():

        for w in words:

            if w in text:
                return cat

    return "General"


def threat_score(text):

    score=0

    text=text.lower()

    for word,val in THREAT_WORDS.items():

        if word in text:
            score+=val

    if score>100:
        score=100

    return score


def generate_summary(text):

    return text[:300]