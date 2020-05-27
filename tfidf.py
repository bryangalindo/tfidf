import math
import os
import string

tfidf_master_list = []


def sort_dict(_dict):
    return {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1], reverse=True)}


def print_dict(_dict):
    for k, v in _dict.items():
        print("{}\t{}\n".format(k, v))


def update_words_master_list(document, i):
    with open('docs/{}'.format(document),  mode='r', encoding='utf-8-sig') as f:
        for line in f:
            for word in line.split():
                clean_word = (word.translate(str.maketrans('', '', string.punctuation))).lower()
                try:
                    if tfidf_master_list[i]['words'][clean_word]:
                        tfidf_master_list[i]['words'][clean_word]['count'] += 1
                except KeyError:
                    new_word_dict = {
                        clean_word: {
                            'count': 1,
                            'term_frequency': 0,
                            'inverse_document_frequency': 0
                        }
                    }
                    tfidf_master_list[i]['words'].update(new_word_dict)


def calculate_all_word_counts():
    directory = 'docs/'
    for i, file in enumerate(os.listdir(directory)):
        tfidf_master_list.append(
            {
                'document_name': file,
                'words': {}
            }
        )
        update_words_master_list(file, i)


def calculate_all_term_frequencies():
    for i, document in enumerate(tfidf_master_list):
        total_words = len(document['words'])
        for k, v in document['words'].items():
            term_frequency = v['count'] / total_words
            tfidf_master_list[i]['words'][k]['term_frequency'] = term_frequency


calculate_all_term_frequencies()


def get_document_occurrences_count(word, current_doc_index):
    document_occurences_count = 1
    word = word.replace('\ufeff', '')
    for i, document in enumerate(tfidf_master_list):
        if i == current_doc_index:
            pass
        else:
            try:
                if tfidf_master_list[i]['words'][word]:
                    document_occurences_count += 1
            except KeyError:
                pass

    return document_occurences_count


def calculate_inverse_document_frequency():
    total_documents = len(tfidf_master_list)

    for i, document in enumerate(tfidf_master_list):
        for k, v in document['words'].items():
            document_occurences = get_document_occurrences_count(k, i)
            inverse_document_frequency = math.log10(total_documents / document_occurences)
            v['inverse_document_frequency'] = inverse_document_frequency


def create_tfidf_list():
    calculate_all_word_counts()
    calculate_all_term_frequencies()
    calculate_inverse_document_frequency()
    return tfidf_master_list

create_tfidf_list()
print('g')
