#!/usr/bin/python
# Imports
import json, csv, pprint, os, sys, argparse
from xcrawler import crawl_web, compute_ranks, dump_dict2file
from utilities import set_log_level, xlog
from datetime import datetime

parser=argparse.ArgumentParser()
parser.add_argument('--depth','-d', help='maximum depth of graph', type=int, default=2)
parser.add_argument('--iter', '-i', help='total iterations for one seed url', type=int, default=100)
parser.add_argument('--log', '-l', help='log level(DEBUG/INFO) ', type=str, default='INFO')
'''
print(parser.format_help())
# usage:  xwrapper.py [-h] [--depth 2] [--iter 50] [--log debug]
'''

args=parser.parse_args()
scriptloglevel = str(args.log).upper().strip()


''' ------------------------------      log setUp      ------------------------------ '''
#----- 1 log file per run -\/
logfile = os.path.basename(__file__).split('.')[0]+'_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.log'
#----- 1 log file per day -\/
#logfile = os.path.basename(__file__).split('.')[0]+'_'+datetime.now().strftime("%Y%m%d")+'.log'
set_log_level(scriptloglevel, logfile)

if scriptloglevel == 'DEBUG' : print('debug mode - please check logfile - ./data/'+ logfile)

def log(msg, ilevel):
	''' info -> print also. else send to log file '''
	if scriptloglevel == 'DEBUG' :
		#print(msg)
		xlog(msg, scriptloglevel)
	elif scriptloglevel == 'INFO' and ilevel.upper().strip() == 'INFO' :
		print(msg)
		xlog(msg, scriptloglevel)	
	else :  None
''' --------------------------------------------------------------------------------- '''

log(' --- >>>>>> script starts <<<<<< --- ' , 'info')

log('--depth argument -> '+str(args.depth),'debug')
log('--iter argument -> ' +str(args.iter),'debug')
log('--log argument -> ' +str(args.log).upper().strip(),'debug')

''' #Testing
log('from log -> info 1','info')
log('from log -> debug 1','debug')
log('from log -> info 2','info')
exit()
'''

#safety: 
max_depth = min(2,args.depth)
max_iterations = min(100,args.iter)

log('max_depth -> '+str(max_depth),'info')
log('max_iterations -> '+str(max_iterations),'info')

#---------------------------------------------------------------Read url from config
#xFile = open(url.config')
xFile = open(os.path.join(os.getcwd(),'config','url.config'))
#print(xFile)
xReader = csv.reader(xFile)

#--------------------------------------------------------------start probing active URl's
for iRow in list(xReader) :

	urlid, urlActive, url = iRow[0], iRow[1], iRow[2]
	log('urlid-> '+urlid,'debug')
	log('urlActive-> '+urlActive,'debug')
	log('url-> '+url,'debug')
	
	if urlActive.upper() == 'Y' :
		log('Computing graph and index for - ' + urlid, 'info')
		graph, index = crawl_web(url, max_depth, max_iterations)
		dump_dict2file(graph,'graph_'+str(urlid)+'.datax')
		dump_dict2file(index,'index_'+str(urlid)+'.datax')
		log('Computing graph and index done for -'+ urlid, 'info')
		
		log('Computing rank for -'+urlid, 'info')
		ranks = compute_ranks(graph)
		dump_dict2file(ranks,'rank_'+str(urlid)+'.datax')
		log('Computing rank done for -' + urlid, 'info')

log(' --- >>>>>> script ends <<<<<< --- ' , 'info')
log('                                   ' , 'info')



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

