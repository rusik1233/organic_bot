from dictionary import sort_trash_dic, ecological_word
def sort_trash(material):
    material = material.lower()
    if material in sort_trash_dic:
        recycling = sort_trash_dic[material].get('переработка', [])
        trash = sort_trash_dic[material].get('урна', [])
        # special case for electronics
        if material == 'электроника':
            recycling = sort_trash_dic[material].get('утилизация', [])

        return {
            'переработка': recycling,
            'урна': trash
        }
    else:
        return 'Материал не найден. Пожалуйста, проверьте ввод.'


def game_word(word):
    if not word:
        return False  # Handle empty string case
    var = word[-1]
    if var in ecological_word:

        return ecological_word[var], ecological_word[var][-1]

    else:
        return False

print(game_word('соса'))
print(game_word('лось'))
print(game_word('') )