import re
from bs4 import BeautifulSoup
from collections import defaultdict, deque, OrderedDict
import os


"""
    start: Stone_Age
    end: Python_(programming_language)
    chain: start -> Brain -> Artificial_intelligence -> end
    
    FIND: <div id="bodyContent">
        - Количество картинок (img) с шириной (width) не меньше 200. Например: <img width="200"
        
        - Количество заголовков (h1, h2, h3, h4, h5, h6), первая буква текста внутри которых соответствует
          заглавной букве E, T или C. Например: <h1>End</h1> или <h5><span>Contents</span></h5>
          
        - Длину максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
          Например: <p><span><a></a></span>, <a></a>, <a></a></p> - тут 2 ссылки подряд, т.к. закрывающийся span прерывает
          последовательность. <p><a><span></span></a>, <a></a>, <a></a></p> - а тут 3 ссылки подяд, т.к. span находится 
          внутри ссылки, а не между ссылками.
          
        - Количество списков (ul, ol), не вложенных в другие списки. Например: <ol><li></li></ol>, 
          <ul><li><ol><li></li></ol></li></ul> - два не вложенных списка (и один вложенный)  
        
    path: /Users/macair/Python Projects/CourseraP3/wiki
    
    result:
        return {
        'Stone_Age': [13, 10, 12, 40],
        'Brain': [19, 5, 25, 11],
        'Artificial_intelligence': [8, 19, 13, 198],
        'Python_(programming_language)': [2, 5, 17, 41]
        } 
"""


def bfs(start, end, tree):
    visited, queue = defaultdict(list), deque([start])
    visited[start]
    while queue:
        vertex = queue.popleft()
        for neighbour in tree.get(vertex, set()):
            if neighbour == end:
                visited[neighbour].append(vertex)
                queue.clear()
                break

            elif neighbour not in visited:
                visited[neighbour].append(vertex)
                queue.append(neighbour)

    if len(tree) == len(visited):
        return visited
    return bfs(end, start, visited)


def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    files = OrderedDict.fromkeys(os.listdir(path))
    for file in files.keys():
        with open(os.path.join(path, file), "r") as f:
            files[file] = set(link_re.findall(f.read()))
    return bfs(start, end, files)


def build_bridge(start, end, path):
    return build_tree(start, end, path).keys()


def parse(start, end, path):

    def find_link_chain(soup, name):
        """
        :param soup:
        :return: max_chain[0]
            max chain of links with tag <a></a>
        """
        li = soup.find(name)
        chain = [li, ] if li else []
        max_chain = []
        while li:
            nli = li.findNextSibling()
            if nli:
                li = nli
                if nli.name == name:
                    chain.append(li)
                else:
                    if len(max_chain) > 1:
                        max_chain = [max(max_chain, key=len), ]

                    max_chain.append(chain)
                    chain = []
            else:
                li = li.find_next(name)
                max_chain.append(chain)
                chain = [li, ]

        return max_chain[0]

    bridge = build_bridge(start, end, path)
    results = OrderedDict.fromkeys(bridge)

    for file in bridge:
        with open(os.path.join(path, file), "r") as data:
            soup = BeautifulSoup(data, "html.parser")
            body = soup.find(id="bodyContent")

            imgs = len(body.find_all("img", width=lambda x: int(x or 0) >= 200))
            headers = len(re.findall(r"<h[1-6].*>([CET].+?)<\/", str(body)))
            links = len(find_link_chain(body, name="a"))
            lists = len([tag for tag in body.find_all(["ul", "ol"]) if not tag.find_parents(["ul", "ol"])])

            results[file] = [imgs, headers, links, lists]

    return results
