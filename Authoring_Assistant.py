def print_menu(text):
    print()
    print('MENU')
    print('c - Number of non-whitespace characters')
    print('w - Number of words')
    print('f - Fix capitalization')
    print('r - Replace punctuation')
    print('s - Shorten spaces')
    print('q - Quit')
    print()
    choice = input('Choose an option:\n')
    while choice not in ['c','w','f','r','s','q']:
        choice = input('Choose an option:\n')
    if choice == 'q':
        return choice, text
    print()
    if choice == 'c':
        print('Number of non-whitespace characters:', get_num_of_non_WS_characters(text))
    elif choice == 'w':
        print('Number of words:', get_num_of_words(text))
    elif choice == 'f':
        fixed = fix_capitalization(text)
        print('Number of letters capitalized:', fixed[1])
        print('Edited text:', fixed[0])
    elif choice == 'r':
        print('Edited text:', replace_punctuation(text))
    elif choice == 's':
        print('Edited text:', shorten_space(text))

    return choice, text

def get_num_of_non_WS_characters(text):
    num = 0
    for char in text:
        if char != ' ':
            num += 1
    return num

def get_num_of_words(text):
    num_words = 1
    for char_index, character in enumerate(text):
        if char_index != 0 and character != ' ' and text[char_index - 1] == ' ':
            num_words += 1
    return num_words

def fix_capitalization(text):
    end_sentence = ['.', '!', '?']
    fixed = ''
    num_fixed = 0
    capitalize_next = True
    for character in text:
        if character in end_sentence:
            capitalize_next = True
            fixed += character
        elif character != ' ':
            if capitalize_next:
                fixed += str.upper(character)
                if character.islower():
                    num_fixed += 1
                capitalize_next = False
            else:
                fixed += character
        else:
            fixed += character
    return fixed, num_fixed

def replace_punctuation(text, exclamation_count=0, semicolon_count=0):
    fixed = ''
    for character in text:
        if character == '!':
            fixed += '.'
            exclamation_count += 1
        elif character == ';':
            fixed += ','
            semicolon_count += 1
        else:
            fixed += character
    print('Punctuation replaced')
    print('exclamation_count:', exclamation_count)
    print('semicolon_count:', semicolon_count)
    return fixed

def shorten_space(text):
    fixed = ''
    for char_index in range(len(text)):
        if char_index == len(text) - 1 or text[char_index] != ' ' or text[char_index + 1] != ' ':
            fixed += text[char_index]
    return fixed

if __name__ == '__main__':
    text = input('Enter a sample text:\n')
    print()
    print('You entered:', text)

    running = True
    while running:
        if print_menu(text)[0] == 'q':
            running = False


