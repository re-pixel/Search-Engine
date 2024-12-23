import pymupdf
import pickle
from trie import Trie
from graph import Graph

YELLOW = "\033[33m"
RESET = "\033[0m"
ITALIC = "\033[3m"

pdf_path = "Data Structures and Algorithms in Python.pdf"

def serialize(object, filename):
    with open(filename, 'wb') as file:
        pickle.dump(object, file)

def deserialize(filename):
    with open(filename, 'rb') as file:
        object = pickle.load(file)
    return object

text = deserialize("serialized/text.pkl")
trie = deserialize("serialized/trie.pkl")
graph = deserialize("serialized/graph.pkl")

document = pymupdf.open(pdf_path)

def extract_text_from_pdf(pdf_path):
    all_text = []
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = [token[4] for token in page.get_text("words")]
        all_text.append(text)
    serialize(all_text, "serialized/text.pkl")
    return all_text

def create_pdf(filename, results):
    doc = pymupdf.open()
    for result in results:
        doc.insert_pdf(document, from_page=result[0], to_page=result[0])

    doc.save(filename)

    doc.close()

references = {}

punctuation = (',', '.', '!', '?', ':', ';')

def generate_trie(pages):
    trie = Trie()
    for i in range(len(pages)):
        for j in range(len(pages[i])):
            if not pages[i][j]:
                continue

            if pages[i][j] == 'page' and pages[i][j+1][0].isdigit():
                tmp = 1
                while tmp < len(pages[i][j+1]) and pages[i][j+1][tmp].isdigit():
                    tmp += 1
                page_number = int(pages[i][j+1][:tmp])
                if i not in references:
                    references[i] = [page_number+21]
                else:
                    references[i].append(page_number+21)


            if pages[i][j][-1] == '-':
                word = pages[i][j][:-1] + pages[i][j+1] if j < len(pages[i]) - 1 else pages[i][j][:-1] + pages[i+1][0]
            else:
                word = pages[i][j]

            trie.insert(word, i, j)
    serialize(trie, "serialized/trie.pkl")
    return trie

def generate_graph(references):
    graph = Graph()
    for reference in references:
        for referenced in references[reference]:
            graph.add(reference, referenced)
    serialize(graph, "serialized/graph.pkl")
    return graph
    
def intersection(selected_pages1, selected_pages2):
    if not selected_pages1 or not selected_pages2:
        return {}
    selected_page_numbers = set(selected_pages1) & set(selected_pages2)
    result = {}
    for page_number in selected_page_numbers:
        if page_number in result:
            result[page_number] += [selected_pages1[page_number]] + [selected_pages2[page_number]]
        else:
            result[page_number] = selected_pages1[page_number] + selected_pages2[page_number]

    return result
    
def union(selected_pages1, selected_pages2):
    if not selected_pages1:
        return selected_pages2
    if not selected_pages2:
        return selected_pages1
    for page_number in selected_pages2:
        if page_number in selected_pages1:
            selected_pages1[page_number] += selected_pages2[page_number]
        else:
            selected_pages1[page_number] = selected_pages2[page_number]
    
    return selected_pages1

def difference(wanted, not_wanted):
    if not wanted:
        return {}
    if not not_wanted:
        return wanted
    for page_number in not_wanted:
        if page_number in wanted:
            del wanted[page_number]

    return wanted

def parse_query(query):
    brackets = []
    for i in range(len(query)):
        if query[i] in ('(', ')'):
            brackets.append(i)

    parsed_query = []
    if not brackets:
        parsed_query = query.split(' ')
    else:
        if brackets[0] != 0:
            parsed_query += query[:brackets[0]-1].split(' ')

        for i in range(0, len(brackets)):
            if not i % 2:
                parsed_query.append(query[brackets[i]:brackets[i+1]+1])
            elif i != len(brackets)-1:
                parsed_query += query[brackets[i]+2:brackets[i+1]-1].split(' ')
        
        if brackets[-1] != len(query) - 1:
            parsed_query += query[brackets[i]+2:].split(' ')

    return parsed_query

def get_selected_pages(query):
    query = parse_query(query)
    i = 0
    result = trie.search(query[0]) if '(' != query[0][0] else get_selected_pages(query[0][1:-1])
    while i < len(query) - 2:
        tmp = trie.search(query[i+2]) if '(' != query[i+2][0] else get_selected_pages(query[i+2][1:-1])
        result = combine_results(result, query[i+1], tmp)
        i += 2

    return result

# def get_phrase_pages(phrase):
#     length = len(phrase.split())
#     candidates = get_selected_pages(" AND ".join(phrase.split()))
#     result = {}
#     for page in candidates:
#         sequences = []
#         tmp = candidates[page].sorted()
#         for i in range(len(tmp)-length):
#             flag = False
#             for j in range(i, i+length):
#                 if 

def combine_results(result1, operand, result2):
    if operand == 'AND':
        return intersection(result1, result2)
    elif operand == 'OR':
        return union(result1, result2)
    elif operand == 'NOT':
        return difference(result1, result2)

def rate_pages(selected_pages):
    if not selected_pages:
        return False
    page_rating = []

    for page in selected_pages:
        rating = len(selected_pages[page]) + graph.get_number_of_references_to(page)
        string = ''
        
        for occurrence in selected_pages[page]:
            line = text[page][(occurrence-4):occurrence]
            presigns, word, postsigns = '', text[page][occurrence], ''
            if not word[-1].isalnum():
                post = -1
                while not word[post-1].isalnum():
                    post -= 1
                word, postsigns = word[:post], word[post:]

            if not word[0].isalnum():
                pre = 1
                while not word[pre].isalnum():
                    pre += 1
                word, presigns = word[pre:], word[:pre]

            line += [f'{presigns}{YELLOW}{word}{RESET}{postsigns}']
            line += text[page][(occurrence+1):(occurrence+5)]
            string += '...' + ' '.join(line) + '...\n'

        if graph.get_references_to(page):
            for reference_page in graph.get_references_to(page):
                if reference_page in selected_pages:
                    rating += 0.5 * len(selected_pages[reference_page])
        
        page_rating.append((page, rating, string))
    return page_rating

def print_results(page_rating):
    if not page_rating:
        print("No results")
        return
    page_rating.sort(key=lambda x:-x[1])

    create_pdf("search_results.pdf", page_rating[:10]) if len(page_rating) >= 10 else create_pdf("search_results.pdf", page_rating)

    i = 0
    while i < len(page_rating):
        for j in range(10):
            if i+j >= len(page_rating):
                break
            print(f"{i+j+1}. page {page_rating[i+j][0]}: {page_rating[i+j][2]} {page_rating[i+j][1]}")
        i += 10
        if i >= len(page_rating):
            break
        q = input("Pritisnite Enter za sledecih 10 rezultata ili x za kraj pretrage: ")
        if q == 'x':
            break

def menu():
    query = input("Pretrazite pdf dokument: ")
    if not query:
        exit()

    if query[-1] == '*':

        options = trie.autocomplete(query[:-1])
        i = 0
        for option in options[:3]:
            print(f'{i+1}. {option[0]}')
            i += 1
        
        chosen = int(input("Izaberite opciju: "))
        pages = get_selected_pages(options[chosen-1][0])
        page_rating = rate_pages(pages)
        print_results(page_rating)

    else:
        splitted_query = query.split()
        if len(splitted_query) > 1 and 'AND' not in splitted_query and 'OR' not in splitted_query and 'NOT' not in splitted_query:
            query = " OR ".join(splitted_query)

        pages = get_selected_pages(query)
        page_rating = rate_pages(pages)
        print_results(page_rating)

        if ' ' not in query and (not page_rating or len(page_rating) < 3):
            alternative = trie.find_similar_query(query)
            reply = input(f"Did you mean {ITALIC}{alternative}{RESET}? ")
            if reply == 'yes':
                pages = get_selected_pages(alternative)
                page_rating = rate_pages(pages)
                print_results(page_rating)

while True:
    menu()