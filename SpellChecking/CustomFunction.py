import re
from collections import Counter


# =============================================================================
# Specll check
# =============================================================================
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('D:/Projects/Warranty/Data/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


correction('C/S.')

# =============================================================================
#  Word Seperation  using viterby seperation
# =============================================================================


def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = Counter(words(open('D:/Projects/Warranty/Data/big.txt').read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))



x = "stayed in sami location. checkedfor stas cases and tsb's and found none, would suggest replacing the head restretainers"


for item in x:
    print(viterbi_segment('checkedfor'))
    #print(correction(item))





# =============================================================================
# Using WordNinja package
# =============================================================================


import wordninja



x = " CUST STATES THE PASSENGER SIDE SECOND ROW HEADREST IS RATTLING PERFORM MULTIPOINT VEHICLE INSPECTION & ALIGNMENT QUICK CHECK. REPLACE PASSENGER 2ND ROW HEADREST RECEPTICALS. 8094 verified the customers concern, triedto swap the left and right second row seathead rests and the noise didn't follow thehead rest. stayed in same location. checkedfor star cases and tsb's and found none,would suggest replacing the head restretainers. #43 02/21/14 REMOVED AND REPLACEDTHE 2ND ROW SEAT HEAD REST RETAINERS,VERIFIED REPAIR #43 02/28/14 Guide/sleeve, headrest - Replace Rear seat-One seat-One or all (1 - Semi-Skilled) GUIDE/SLEEVE, HEADREST-Replace (B) PERFORM MULTIPOINT VEHICLE INSPECTION & ALIGNMENT QUICK CHECK. "


y = wordninja.split('c/s')

wordninja





from nltk.corpus import words


'remval' in words.words()



















