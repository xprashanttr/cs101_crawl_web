import logging, os

def xlog(msg, loglevel):
	#logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	if   loglevel.upper().strip() == 'DEBUG': 
		logging.debug(msg)
	elif loglevel.upper().strip() == 'INFO' : 
		logging.info(msg)
	elif loglevel.upper().strip() == 'WARNING' : 
		logging.warning(msg)
	elif loglevel.upper().strip() == 'ERROR' : 
		logging.error(msg)
	elif loglevel.upper().strip() == 'CRITICAL' : 
		logging.critical(msg)
	else : None

def set_log_level(scriptloglevel, logfile):
#Set Log Level 
	if   scriptloglevel == 'DEBUG' : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
	elif scriptloglevel == 'INFO' : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	elif scriptloglevel == 'WARNING' : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
	elif scriptloglevel == 'ERROR' : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
	elif scriptloglevel == 'CRITICAL' : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')
	#elif scriptloglevel == 'DISABLE' : 
	else : logging.basicConfig(filename = os.path.join(os.getcwd(),'data',logfile),level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

