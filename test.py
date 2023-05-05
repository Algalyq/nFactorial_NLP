import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# список уже существующих имен
with open('names.txt', 'r') as f:
    names = f.read().splitlines()

# функция для получения списка биграмм из имён
def get_bigrams(name_list):
    bigrams = {}
    for name in name_list:
        # добавляем начальный и конечный символы, чтобы учесть биграммы в начале и конце имён
        name = '^' + name.lower() + '$'
        for i in range(len(name) - 1):
            bg = name[i:i+2]
            if bg in bigrams:
                bigrams[bg] += 1
            else:
                bigrams[bg] = 1
    
    return bigrams

def generate_name(probabilities):
    new_name = ""
# Выберите начальную биграмму случайным образом из всех возможных биграмм
    start_bigrams = [bg for bg in probabilities.keys() if bg.startswith("^")]
    if len(start_bigrams) > 0:
        start_bigram = random.choice(start_bigrams)
        new_name += start_bigram[1]  # добавьте второй символ биграммы к имени
        next_bigram = start_bigram[1:]  # cрез ^ с этой биграммы
        while not next_bigram.endswith("$"):  # продолжайте генерировать до конца имени
            possible_bigrams = [bg for bg in probabilities.keys() if bg.startswith(next_bigram[0])]
            weights = [probabilities[bg] for bg in possible_bigrams]
            next_bigram = random.choices(possible_bigrams, weights=weights)[0]
            new_name += next_bigram[1]  # добавьте второй символ биграммы к имени
            
                
    else:
        print("Error: no starting bigram found.")

    print("Generated name:", new_name[:-1])

def vis(probabilities):
    df = pd.DataFrame.from_dict(probabilities, orient='index', columns=['Probability'])
    df['First'] = [x[0] for x in df.index]
    df['Second'] = [x[1] for x in df.index]
    matrix = df.pivot("First", "Second", "Probability")

    # Рисуем тепловую карту
    sns.heatmap(matrix, cmap="YlGnBu")
    plt.show()

bigrams = get_bigrams(names)    
total_bigrams = sum(bigrams.values())
probabilities = {bg: count / total_bigrams for bg, count in bigrams.items()}
generate_name(probabilities)
vis(probabilities)