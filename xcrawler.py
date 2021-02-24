###
### crawler.py
###
###

from bs4 import BeautifulSoup, SoupStrainer
import requests, httplib2, json, pprint, os



def get_page(url):
	try: page = requests.get(url)
	except: page = None
	if page: return page.text
	else: 
		print ("Error in requesting page html body: " + url)
		return None
	'''
	if url in cache:
		return cache[url]
	else:
		print ("Page not in cache: " + url)
		return None
	'''	

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(url):
	links = []
	
	try : reqs = requests.get(url)
	except : return links
	
	soup = BeautifulSoup(reqs.text, 'html.parser')
	#soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('a'):
		x = link.get('href')
		try:
			if x.startswith('https:') and 'linkedin' not in x.lower() and 'facebook' not in x.lower() and 'drive.google' not in x.lower() and 'comcast' not in x.lower(): 
				links.append(x)
				#print(x)
		except AttributeError: None 		
	return links

'''
def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links
'''



def add_page_to_index(index, url):
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')
	#Adding page title to index
	title = soup.find('title')
	try :
		#print(title.string)
		add_to_index(index, title.string, url)
	except : None
	#Find keywords in page and add to the index 
	#--to be done
'''
def add_page_to_index(index, url, content):
	words = content.split()
	for word in words:
		add_to_index(index, word, url)	
'''

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def crawl_web(seed, max_depth, max_iterations): # returns index, graph of inlinks
	tocrawl = set([seed])
	crawled = []
	graph = {}  # <url>, [list of pages it links to]
	index = {} 
	next_depth = []
	depth = 1
	i = 0
	#url = seed
	##---------------------------------------
	content = get_page(seed)
	#tocrawl = set(get_all_links(content))
	tocrawl = set(get_all_links(seed))
	graph[seed] = list(tocrawl)
	##---------------------------------------
	
	
	while tocrawl and depth <= max_depth and i <= max_iterations : 
		#print('----------------------------------------')
		#print('tocrawl -> ')
		#pprint.pprint(tocrawl)
		#print('next depth -> ')
		#pprint.pprint(next_depth)
		#print('----------------')
		
		url = tocrawl.pop() #-Handle This if duplicacy at graph level
		print('depth('+ str(depth) +')/iteration('+str(i)+')/ url - '+ url)
		
		if url not in crawled:
			content = get_page(url)
			'''
			add_page_to_index(index, url, content)
			outlinks = get_all_links(content)
			'''
			add_page_to_index(index, url)
			outlinks = get_all_links(url)
			
			if url not in graph.keys(): graph[url] = outlinks
			else: graph[url] = graph[url] + outlinks
			
			next_depth = next_depth + outlinks
			crawled.append(url)
			#tocrawl.update(next_depth)
		
		if not tocrawl :
			tocrawl, next_depth = next_depth, []
			depth = depth + 1
		i = i + 1 

	'''
	while True : ##Removing duplicacy of keys in graph
		xurl = tocrawl.pop()
		if url == xurl : continue
		else : 
			url = xurl
			break
	#url = tocrawl.pop() # changed page to url - clearer name
	'''
	#return index, graph
	return graph, index






def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def dump_dict2file(dict, file):
	with open(os.path.join(os.getcwd(),'data',file), 'a') as file: 
		file.write(json.dumps(dict))
		file.write('\n')	
    
cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

Prashant Added 
<a href="http://udacity.com/cs101x/urank/arsenic(21).html">this recipe</a>.
<a href="http://udacity.com/cs101x/urank/arsenic(22).html">this recipe</a>.

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""", 

'http://udacity.com/cs101x/urank/arsenic(21).html': """<a href="http://udacity.com/cs101x/urank/arsenic(211).html"></a>""", 
'http://udacity.com/cs101x/urank/arsenic(22).html': """<a href="http://udacity.com/cs101x/urank/arsenic(221).html"></a>""", 

'http://udacity.com/cs101x/urank/arsenic(211).html': """<a href="http://udacity.com/cs101x/urank/arsenic(2111).html"></a>
														<a href="http://udacity.com/cs101x/urank/arsenic(2112).html"></a>""", 

'http://udacity.com/cs101x/urank/arsenic(221).html': """<a href="http://udacity.com/cs101x/urank/arsenic(2211).html"></a>
														<a href="http://udacity.com/cs101x/urank/arsenic(2212).html"></a>""", 



}

