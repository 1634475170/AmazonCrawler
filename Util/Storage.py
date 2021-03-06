# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys ,xlrd,time ,datetime,multiprocessing ,os
from decimal import getcontext, Decimal   
from keySearch import getTitle,getTcumb
sys.path.append('../')
from GetConfig import GetConfig
from db.mysql import db_mysql
from LogHandler import LogHandler
from ReadXlsx import FileOperation

convert=LogHandler("con")
class insertEx(object):
	"""docstring for insert"""
	def __init__(self):
		super(insert, self).__init__()
		self.cl=FileOperation()
		self.bea=self.cl.read()
		self.keWord=self.cl.readkey()
		self.db =db_mysql()
	def beaInsert(self):
		thread_list=[]
		for mold in self.bea:
			pw = multiprocessing.Process(target=self.beay, args=(mold,))
			thread_list.append(pw)
		for x in thread_list:
			time.sleep(3)
			x.start()

	def beay(self ,mold):
		cf=mold[6]
		if mold[6]=='-':
			cf=0
		if mold[5]=='-':
			mold[5]=0

		try:
			tim= xlrd.xldate.xldate_as_datetime(mold[11], 0)
			sql= "INSERT INTO beauty	VALUES ('%s', '%d', '%s', '%d', '%d','%d','%d','%d','%d','%d','%s','%d' )" % \
					(mold[0].replace("'",""), int (mold[1]), getTitle(mold[0]).replace("'",""), int(mold[3]),int(mold[4]),float (mold[5]),int(cf),float(mold[7]),int(mold[9]),int(mold[10]), str(tim),int(mold[12]))
			self.db.execute(sql)
		except Exception as e:
			convert.info(mold[6])

	def keyInsert(self):
		thread_list=[]
		for mold in self.keWord:
			pw = multiprocessing. Process(target=self.cf, args=(mold,))
			thread_list.append(pw)
		for x in thread_list:
			time.sleep(2)
			x.start()
	def cf(self, mold):
		
		tr=getTcumb(mold[0])
		if mold[7]=='':
			mold[7]=0
		sc= "('%s', '%f', '%f', '%f', '%f','%f','%f','%f','%f','%f','%f','%f', '%f','%f')" % \
				(mold[0].replace("'",""), int (mold[1]), int(mold[2]), int(mold[3]),
							int(mold[4]),
							mold[5],mold[6], todem (mold[7]), mold[7], mold[9],
							 todem(mold[10]), todem(mold[11]),
							 int(tr[0]),int(tr[1]))
		sql= "INSERT INTO SearchWords  VALUES "+sc
		self.db.execute(sql)

def todem(umg):
	return  Decimal(umg).quantize(Decimal('0.00'))  


class insertDB(object):
	"""docstring for insertDB"""
	def __init__(self,):
		super(insertDB, self).__init__()
		self.cl=FileOperation()
		self.bea=self.cl.read()
		self.keWord=self.cl.readkey()
		self.db =db_mysql()
	def asinInsert(self):
		thread_list=[]
		for mold in self.asin:
			pw = multiprocessing.Process(target=self.asin, args=(mold,))
			thread_list.append(pw)
		for x in thread_list:
			time.sleep(6)
			x.start()
class insertType(object):
	"""docstring for insertType"""
	def __init__(self,):
		super(insertType, self).__init__()
		self.path= GetConfig().fi_path
		self.db =db_mysql()

	def asinType(self):
		sql,asinType, lis='',[], os.listdir(self.path+'/asins')
		for x in lis:
			asinType.append(x.replace(' ','').replace('.xlsx','').replace('ASIN',''))
		sql="INSERT INTO asinType SET "
		for ca in asinType:
			self.db.execute(sql+"  idasinType=0,AsinType='"+ca+"';")
	def movertype(self):
		filepath,lis ,sql=os.listdir(self.path+'/mover'),[],"INSERT INTO moverType SET "
		for x in filepath:
			lis+= FileOperation(self.path+'/mover/'+x).getSheets()
		for cs in lis:
			print cs.encode("utf8")
			self.db.execute(sql+" TypeId=0, moverTypecol='"+cs+"'")

	def SearchTermType(self):
		filepath,lis ,sql=os.listdir(self.path+'/search term'),[],"INSERT INTO SearchTermType SET "	
		for x in filepath:
			lis+= FileOperation(self.path+'/search term/'+x).getSheets()
		for cs in lis:
			print cs.encode("utf8")
			self.db.execute(sql+" typeId=0, Type='"+cs+"'")
if __name__ == '__main__':	
	sc=insertType()
	sc.SearchTermType()
# ('%s', '%f', '%f', '%f', '%f','%f','%f','%f','%f','%f','%f','%f', '%d','%d')" % \
# 					(mold[0], int (mold[1]), int(mold[2]), int(mold[3]),
# 						int(mold[4]),
# 						mold[5],mold[6], mold[7], mold[7], mold[9],
# 						 mold[10], mold[11],
# 						 int(tr[0]),int(tr[1]))
