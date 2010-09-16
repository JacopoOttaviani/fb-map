#!/usr/bin/env python
# encoding: utf-8
"""
f.pj

Created bj Jacopo on 2010-09-13.
"""

import sys
import os
import time
import facebook
import networkx as nx
import pickle
import threading
import time
import Queue

class usefulData():
	def __init__(self):
		"""
		if os.path.exists('last.log') and os.path.exists('graph.pickle'):
			f = open('last.log','r')
			self.i = int(f.readline().strip())
			self.G = nx.read_gpickle('graph.pickle')
			f.close()
		
		else:
		"""
		self.fbs = open('api.txt').readlines()
		self.fb = facebook.Facebook(self.fbs[0].strip(), self.fbs[1].strip())

		self.i = 0
		self.G = nx.Graph()
		self.friends = []
		self.names={}
		self.workQueue = Queue.Queue(0)
		
	def fillStaticData(self):
		friends_name = []
		a = False
		while ( a != True ):
			try:
				self.fbLogin()
				a = True
			except Exception as inst:
				print type(inst)     # the exception instance
				print inst.args      # arguments stored in .args
				print inst           # __str__ allows args to printed directly
				print 'Facebook Error, trying to refresh connection...'
				continue
			
		info = self.fb.users.getInfo([self.fb.uid], ['name'])[0]


		self.friends = self.fb.friends.get()
		friends_name = self.fb.users.getInfo(self.friends, ['name', 'uid'])
		
		# filling the friends uid:name dictionary
		u=0
		for friend in friends_name:
			#print friend['name'], ' -> ' , friend['uid']
			self.names[friend['uid']] = friend['name']
			self.G.add_node(friend['uid'])
			self.G.node[friend['uid']]['name'] = self.names[friend['uid']]
			print u, self.G.node[friend['uid']]['name'], self.names[friend['uid']]
			u=u+1
		j=0
		for i in self.G.nodes():
			print j,self.G.node[i]['name']
			j=j+1
		# filling the working queue
		for a in self.friends:
			self.workQueue.put(a)
		
		# filling the working Queue (from where threads suck new friends to check)
		self.workQueue = Queue.Queue(len(self.friends))
		for i in self.friends:
			self.workQueue.put(i)

	def fbLogin(self):

		# Get api_key and secret_key from a file
		self.fbs = open('api.txt').readlines()
		self.fb = facebook.Facebook(self.fbs[0].strip(), self.fbs[1].strip())

		self.fb.auth.createToken()
		# Show login window
		self.fb.login()
		"""
		# Login to the window, then press enter
		print 'After logging in, press enter...'
		raw_input()
		"""
		self.fb.auth.getSession()


class fbMapper(threading.Thread):
	
	def __init__(self, y=9):
		threading.Thread.__init__(self)
		self.threadID = y
		self.j = 0
	
	def run(self):
		print 'starting thread ',self.threadID,'...'
		self.go()
		
		
	def go(self):
		try:
			data.fbLogin()
		except facebook.FacebookError as inst:
			print type(inst)     # the exception instance
			print inst.args      # arguments stored in .args
			print inst           # __str__ allows args to printed directly
			print 'Facebook Error, trying to refresh connection...'
			data.fbLogin()
		

		while not data.workQueue.empty():			
			queueLock.acquire()
			currentFriend = data.workQueue.get() 
			queueLock.release()
			print data.workQueue.qsize(),' -- Thread #',self.threadID,'is checking',currentFriend
			
			try:
				#a = self.fb.friends.areFriends([self.friends[self.i]]*len(self.friends), [self.friends])
				a = data.fb.friends.areFriends([currentFriend]*len(data.friends), [data.friends])
				flag = True
			except Exception as inst:
				print type(inst)
				print inst.args
				print inst 
				print 'Uh, continuing.'
				continue
			
			for l in a:
				try:
					if l[u'are_friends'] == True:
						#print data.G[l[u'uid1']]['name'], 'is friend of ', data.G[l[u'uid2']]['name']
						graphLock.acquire()
						data.G.add_edge(l[u'uid1'],l[u'uid2'])
						graphLock.release()
					else:
						ab = True
						#print data.G[l[u'uid1']]['name'], 'is not friend of ', data.G[l[u'uid2']]['name']
				
				except facebook.FacebookError as inst:
					print type(inst)     # the exception instance
					print inst.args      # arguments stored in .args
					print inst           # __str__ allows args to printed directly
					print 'Facebook Error, trying to refresh connection...'
					self.data.fbLogin()
					flag = False
					continue
			
				except Exception as inst:
					print type(inst)
					print inst.args
					print inst 
					print 'Uh, continuing.'
					flag = False
					continue
		print 'Thread #',self.threadID,'should now die.'
		# writing last i
		"""
		f = open ('last.log', 'w')
		f.write(str(self.i)+'\n')
		f.close()
		
		"""

def nx2viz(network):
	print 'writing dot file...'
	f = open('graph.dot','w')
	f.write('graph mutual_friends {\n')
	for e in network.edges():
		f.write(('\t\"'+network.node[e[0]]['name']+'\"--\"'+network.node[e[1]]['name']+'\";\n').encode('utf-8'))
	f.write('}\n')
	f.close()
	
if __name__ == '__main__':

	G = nx.read_gpickle('graph.pickle')
	#print G.adj
	j=0
	for i in G.nodes():
		print j,G.node[i]['name']
		j=j+1
	for e in G.edges():
		print G.node[e[0]]['name'], '---' , G.node[e[1]]['name']
	nx2viz(G)
	"""
	queueLock = threading.Lock()
	graphLock = threading.Lock()
	data = usefulData()
	data.fillStaticData()
	threads=[]
	for i in range(3):
		threads.append(fbMapper(y=i))
	
	for t in threads:
		t.start()
		print('sleeping 3 secs...')
		time.sleep(3)
	
	# Wait for all threads to complete
	for t in threads:
	    t.join()

	print 'Now pickling...'
	nx.write_gpickle(data.G,'graph.pickle')

	nx2viz(data.G)
	"""
	
