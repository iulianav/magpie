from nltk.util import ngrams as nltk_ngrams
from anchor import get_anchors
from keyword_token import add_token


def generate_ngram_candidates(document, ontology):
    """
    Generate keyword candidates by building an ontology trie and performing
    a fuzzy match over it with ngrams extracted from the text.
    :param document - Document object
    :param ontology - Ontology object

    :return set of KeywordTokens
    """
    all_words = document.get_meaningful_words()
    ontology_dict = ontology.get_literal_uri_mapping()
    tokens = set()

    # 1-grams
    anchors = get_anchors(all_words, ontology_dict)
    # TODO remove the standalone ones
    tokens |= set(anchors)

    # 2-grams
    n = 2
    ngram_tokens = dict()
    for position, ngram in get_ngrams_around_anchors(n, all_words, anchors):
        # TODO potential filtering of ngrams e.g. for linguistic purposes
        form = " ".join(ngram)
        for hit in ontology.fuzzy_match(form):
            add_token(hit, ngram_tokens, position, ontology_dict, form=form)
    tokens |= set(ngram_tokens.values())

    # 3-grams
    # n = 3
    # concepts = ontology.get_nlength_concept_values(n)
    # for position, ngram in get_all_ngrams(n, all_words):
    #     ng_string = " ".join(ngram)
    #     best_hit = fuzz_process.extract(ng_string, concepts)
    #     if best_hit:
    #         print ng_string, best_hit

    # 4-grams
    # n = 4
    # concepts = ontology.get_nlength_concept_values(n)
    # for position, ngram in get_all_ngrams(n, all_words):
    #     ng_string = " ".join(ngram)
    #     best_hit = fuzz_process.extract(ng_string, concepts)
    #     if best_hit:
    #         print ng_string, best_hit

    return tokens


def get_all_ngrams(n, words):
    """ Generate all possible engrams from a text and enumerate them. """
    return enumerate(nltk_ngrams(words, n))  # not necessarily a list


def get_ngrams_around_anchors(n, words, anchors):
    """ Generate ngrams only around certain words (anchors). """
    all_ngrams = []
    for anchor in anchors:
        for i in anchor.get_all_occurrences():
            start_index = max(0, i - n + 1)
            piece = words[start_index: min(i + n, len(words))]
            ngrams = enumerate(nltk_ngrams(piece, n), start=start_index)
            all_ngrams.extend(ngrams)

    return all_ngrams
