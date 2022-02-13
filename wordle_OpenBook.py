import random
def random_search(word_pool):
    return word_pool[random.randrange(len(word_pool))]

def get_gygCodeFromIO(target_word_length):
    input_checker = True
    while input_checker:
        input_checker = False
        guess_result = input()
        if "x" in guess_result:
            return False
        if len(guess_result) != target_word_length:
            print("Invalid input (shorter/longer than length of target word)")
            input_checker = True
            continue
        for input_char in guess_result:
            tmp = int()
            try:
                tmp = int(input_char)
            except:
                print("Invalid input (Only can input number)")
                input_checker = True
                break
            if tmp > 2:
                print("Invalid input (Cannot be greater than 2)")
                input_checker = True
                break
    return guess_result

def word_pool_filter(word_pool, guess_word_result):
    for word_index,letter_result_pair in enumerate(guess_word_result): # (letter, result)
        letter = letter_result_pair[0]
        color = letter_result_pair[1]
        print(f"word_index: {word_index}, letter: {letter}, color: {color}")
        if color == "0": # for gray one
            for index,word in enumerate(word_pool.copy()):
                if letter in word:
                    word_pool.remove(word)
        elif color == "2": # for green one
            for index,word in enumerate(word_pool.copy()):
                if word[word_index] != letter: # if the letter of the position different from the letter we got:
                    print("remove")
                    word_pool.remove(word) # remove the word
        elif color == "1":
            for index, word in enumerate(word_pool.copy()):
                if letter not in word or word[word_index] == letter :
                    word_pool.remove(word)

    return word_pool
if __name__ == "__main__":
    target_word_length = int()
    try:
        target_word_length = int(input("Input the word length: "))
    except:
        raise BaseException("Not a valid number.")
    word_pool = list()
    with open(f"./dictionary_{target_word_length}", 'r') as f:
        word_pool = f.read().split(",")
    total_word_pool_len = len(word_pool)
    while len(word_pool) > 0:
        print(f"There are {len(word_pool)} possible words.")
        random.seed()
        guess_word = str()
        if len(word_pool) == total_word_pool_len:
            guess_word = random_search(word_pool)
            print(f'***** I recommend this word: "{guess_word}" for you. *****\n\n\n')
        else:
            guess_word = random_search(word_pool)
            print(f'***** I recommend this word: "{guess_word}" for you. *****\n\n\n')
        print("Now, please tell me what happend \n(gray: 0, yellow: 1, green: 2. EX: 01012 for gray, yellow, gray, yellow, green on wordle. xxxxx for not valid word):")
        guess_result = get_gygCodeFromIO(target_word_length)
        if not guess_result:
            continue
        guess_word_result = list()
        for index, value in enumerate(guess_word):
            guess_word_result.append((value, guess_result[index])) # put the letter and the result together
        print(guess_word_result)
        word_pool = word_pool_filter(word_pool, guess_word_result)
        if len(word_pool) == 1:
            print(f"The answer is {word_pool[0]}. You're welcome.")
            break
