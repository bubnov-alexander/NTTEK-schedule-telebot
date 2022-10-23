from collections import Counter

f = open(f'data/homework/Сопровождение ИС.txt', 'r', encoding='UTF-8')
word_list = []
txt = f.read()
for word in txt.split():
    clear_word = ''
    for letter in word:
            if letter.isalpha():
                clear_word += letter.lower()
    word_list.append(clear_word)
for word in word_list:
    if word != 'задание':
        word_list.remove(word)
print(word_list)
    
text = Counter({word_list})
print(text)
if text > 1:
    print('пупу')
else:
    print('ljknfs')