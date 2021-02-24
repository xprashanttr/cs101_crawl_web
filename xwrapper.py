#!/usr/bin/python
# Imports
from xcrawler import crawl_web, compute_ranks, dump_dict2file
import json, csv, pprint, os, sys, argparse
# Program Variables
#max_depth = 2
#max_iterations = 300

parser=argparse.ArgumentParser()
parser.add_argument('--depth','-d', help='maximum depth of graph', type=int, default=2)
parser.add_argument('--iter', '-i', help='total iterations for one seed url', type=int, default=100)

'''
print(parser.format_help())
# usage:  xwrapper.py [-h] [--depth 2] [--iter 50]
'''

args=parser.parse_args()
print('--depth argument passed -> '+str(args.depth))
print('--iter argument passed -> ' +str(args.iter))

#safety: 
max_depth = min(2,args.depth)
max_iterations = min(100,args.iter)

print('max_depth -> '+str(max_depth))
print('max_iterations -> '+str(max_iterations))

#---------------------------------------------------------------Read url from config
#xFile = open(url.config')
xFile = open(os.path.join(os.getcwd(),'config','url.config'))
#print(xFile)
xReader = csv.reader(xFile)

#--------------------------------------------------------------start probing active URl's
for iRow in list(xReader) :
	#print('')
	urlid, urlActive, url = iRow[0], iRow[1], iRow[2]
	print('urlid-> '+urlid)
	print('urlActive-> '+urlActive)
	print('url-> '+url)
	print('')
	
	if urlActive.upper() == 'Y' :
		print('Computing graph and index for - ' + urlid)
		graph, index = crawl_web(url, max_depth, max_iterations)
		dump_dict2file(graph,'graph_'+str(urlid)+'.datax')
		dump_dict2file(index,'index_'+str(urlid)+'.datax')
		print('Computing graph and index done for -'+ urlid)
		
		print('Computing rank for -'+urlid)
		ranks = compute_ranks(graph)
		dump_dict2file(ranks,'rank_'+str(urlid)+'.datax')
		print('Computing rank done for -' + urlid)

exit()






#--Test URL
#url = 'http://udacity.com/cs101x/urank/index.html'
#url = 'http://udacity.com/cs101x/urank/arsenic.html'
print('Probing --> '+ url)

#Compute Graph
print('Computing graph and index')
graph, index = crawl_web(url, max_depth) #, max_iterations)
dump_dict2file(graph,'graph.datax')
dump_dict2file(index,'index.datax')
print('Computing graph and index - done')

#Compute Rank
print('Computing rank')
ranks = compute_ranks(graph)
dump_dict2file(ranks,'rank.datax')
print('Computing rank - done')

