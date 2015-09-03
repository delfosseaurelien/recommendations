from math import sqrt
from data import critics


def mean(dict):
    """ Compute dot product
    Args:
        a (dictionary): first dictionary of record to value
    Returns:
        mean: mean of the dictionnary
    """
    return sum(dict.values()) / float(len(dict))


def similarity(prefs, person1, person2):
    """ Compute how similar two movie critics are in their tastes,
    based on their critics.
    You do this by comparing each person with every other person
    and calculating a similarity score.

    :param prefs: dict - critics as defined in data.py
    :param person1: str - movie critic's name
    :param person2: str - movie critic's name

    :return: float - similarity score
    """

    common_viewed = list(set(prefs[person1].keys()).intersection(prefs[person2].keys()))

    if len(common_viewed) > 0:
        a = {key: prefs[person1][key] for key in common_viewed}
        b = {key: prefs[person2][key] for key in common_viewed}
        mean_a, mean_b = mean(a), mean(b)

        num = sum(p * q for p, q in zip([i - mean_a for i in a.values()], [j - mean_b for j in b.values()]))
        den = sqrt((sum([(i - mean_a) ** 2 for i in a.values()]) * sum([(i - mean_b) ** 2 for i in b.values()])))

        return num / float(den)
    else:
        return 0


def top_matches(prefs, person, n=5):
    """ Rank movie critics matches for `person` from `perfs`.

    :param prefs: dict - critics as defined in data.py
    :param person: str - movie critic's name to compare others to
    :param n: int - number of movie critics to rank

    :return: list[tuple(float, str)] - ranking of (score, critic's name)
    """
    scores = [(similarity(prefs, person, others), others)
              for others in prefs if others != person]

    scores.sort()
    scores.reverse()

    return scores[0:n]


def get_recommendations(prefs, person):
    """ Recommend movies to `person` matching others' ratings with his.

    :param prefs: dict - critics as defined in data.py
    :param person: str - movie critic's name to advise

    :return: list[tuple(float, str)] - ranking of (score, film's title)
    """
    totals = {}
    simSums = {}

    for others in prefs:
        if others == person:
            continue
        sim = similarity(prefs, person, others)

        if sim <= 0:
            continue
        for movie in critics[others]:
            #Only non rated movies are recommended
            if movie not in prefs[person] or prefs[person][movie] == 0:
                totals.setdefault(movie, 0), simSums.setdefault(movie, 0)
                #similarity ponderation
                totals[movie] += prefs[others][movie] * sim
                simSums[movie] += sim

    # Normalization
    rankings = [(total / simSums[movie], movie) for movie, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

