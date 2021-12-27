import datetime
from urllib.parse import quote
from urllib.request import urlopen
from json import loads
from itertools import groupby


def main():
    url = 'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles=%D0%93%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B8%D0%B9,_%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80_%D0%91%D0%BE%D1%80%D0%B8%D1%81%D0%BE%D0%B2%D0%B8%D1%87'
    stats = get_revision_statistics(url,'183903')
    print_stats_in_file(stats, ' Gradsky.txt')

    url = f'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles={quote("Бельмондо,_Жан-Поль")}'
    stats = get_revision_statistics(url,'192203')
    print_stats_in_file(stats, 'Belmondo.txt')


def get_revision_statistics(url, pageid):
    data = loads(urlopen(url).read().decode('utf8'))
    revisions = sorted(data['query']['pages'][pageid]['revisions'], key=get_date, reverse=True)
    groups = groupby(revisions, get_date)
    result = {}
    for i, g in groups:
        result[i] = list(g)
    return result


def print_stats_in_file(result, filename):
    with open(filename, 'w', encoding='utf8') as f:
        for k in result:
            print(k, len(result[k]), file=f)


def get_date(x):
    return datetime.datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()


if __name__ == '__main__':
    main()