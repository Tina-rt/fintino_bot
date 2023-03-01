import re

# l = [i for i in range(20)]
GREETINGS = ['bonjour', 'hey', 'salut', 'salama']
GREETINGS_REPLY = ["Bonjour, ceci est un bot messenger pour rechercher sur le web et sur youtube\n Syntaxe: \n - google: <mot cle>\n - video: <mot cle>"]

def isGreetings(query):
	query = query.lower()
	for g in GREETINGS:
		if len(re.findall(r'^'+g, query)) > 0:
			return True
	return False

# print(isGreetings('bonjour, ca va ?'))


def show(list_, page, n):
	i = (page-1)*n
	s = page*n
	return list_[i:s]

def extract_query(msg):
    express = r'(?<=:)(.+)'
    result = re.search(express, msg.lower())
    type_search = re.search(r'^(google|video|image|traduire)(?=:)', msg.lower().replace(' ', ''))
    
    if result is None and type_search is None:
        return {}
    else: return {
        'type': type_search.group(),
        'query': result.group()
    }

# print(show(l, 6))
