def count_rows_and_words(filename):
    row_counter = 0
    word_counter = 0
    with open(filename, mode="r", encoding="utf-8") as file:
        for line in file:
            row_counter += 1
            word_counter += len(line.split())
    
    return (row_counter, word_counter)

def compute_word_frequencies(filename):
    word_counter = dict()
    with open(filename, mode="r", encoding="utf-8") as file:
        for line in file:
            for word in line.split():
                if word.strip() == "":
                    continue
                
                if word in word_counter:
                    word_counter[word] += 1
                else:
                    word_counter[word] = 1

    return word_counter
            

if __name__ == '__main__':
    r= count_rows_and_words('example.txt')
    c= compute_word_frequencies('example2.txt')
    print(r)
    print(c)
