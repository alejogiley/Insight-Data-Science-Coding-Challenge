#!/usr/bin/env python3

##
## Alejandro Gil Ley
## 04/01/2019
##
## Process Instacart products and orders data and calculate, 
## for each department, the number of times a product 
## was requested, number of times a product was requested 
## for the first time and a ratio of those two numbers.
##

import sys
import time

class Product_Record(object):
	''' This class keep track of products id info, 
	    and increments the number of orders and number
	    of first orders for each product_id.'''
	
	
	def __init__(self, prod_id, reordered):
		# prod_id: product_id record
		# reordered: flag indicating if 
		# the product has been ordered 
		# by this user at some point in 
		# the past. The field is 1 if 
		# the user has ordered it in the 
		# past and 0 if the user has not. 
		self.prod_id = prod_id
		# number of orders
		self.number_of_orders = 1
		# number of first orders
		if reordered == 0: 
			self.number_of_first_orders = 1
		else:
			self.number_of_first_orders = 0
	    
	def add_order(self, reordered):
		# increment the number of orders
		self.number_of_orders += 1
		if reordered == 0:
			self.number_of_first_orders += 1
	
#END class

def add_to_product_dict(prod_dict, prod_id, reordered):
	'''Checks if a product has been added to dictionary prod_dict,
	   if it has not beign added, it creates a new Product_Record 
	   and adds it to prod_dict. In case it has been added, then 
	   it increments the number of orders by one.'''
	
	if prod_dict.get(prod_id, None) is None:
		prod_dict[prod_id] = Product_Record(prod_id, reordered)
	else:
		prod_dict[prod_id].add_order(reordered)

#END function

class Department_Record(object):
	'''The purpose of this class is to record the deparment_id 
	   and product_id data from file products.csv. It saves a 
	   list of all products belonging to each department.'''
	
	def __init__(self, dept_id, prod_id):
		# dept_id: department_id record
		# prod_id: same as previous class
		self.dept_id = dept_id
		self.products = [prod_id]
	
	def add_product(self, prod_id):
		# Given a new product id 
		# append the new item to
		# this department's products list
		self.products.append(prod_id)

#END class

def add_to_department_dict(dept_dict, dept_id, prod_id):
	'''Checks if a deparment has been added to dictionary dept_dict.
	   If it has not been added, it creates a new Department_Record 
	   and adds it to dept_dict. In case it has been added, then 
           it includes the new product_id to the department record.'''
	
	if dept_dict.get(dept_id, None) is None:
		dept_dict[dept_id] = Department_Record(dept_id, prod_id)
	else:
		dept_dict[dept_id].add_product(prod_id)

#END function

def read_csv(fileopen):
	'''Read a csv file and save its content in a python dictionary structure.'''
	
	# create dictionaries to 
	# keep track of departments
	# and products
	dept_dict = {}
	prod_dict = {}
	
	# flag used to monitor which file
	# type is beign read at the moment
	reading_orders = False
	reading_departments = False
	
	# read first line
	# !!! file should contains header
	head = fileopen.readline()
	# set keys for dicc
	keys = head.replace("\n","").split(",")
	
	# Read each file line
	for line in fileopen:
		# separate line items by comma,
		# divide item by type, into digits 
		# or strings.
		digits = [int(item) for item in line.replace("\n","").split(",") if item.isdigit()]
		# !!! string records can contains internal commas
		string = [item for item in line.replace("\n","").split(",") if not item.isdigit()]
		# combine the strings separated by commas into whole phrases
		# the phrases won't be used in this program
		phrase = ",".join(string)
		
		# check whether keys belong to order_products.csv file
		# !! one could ignore the header info
		# !! use 'if phrase:' instead 
		if keys[0] == "order_id" and keys[1] == "product_id":
			reading_orders = True
			# add the product_id record to prod_dict, create a new 
			# Product_Record if one does not already exist for this 
			# product_id, increments the number of orders
			add_to_product_dict(prod_dict,digits[1], digits[3])
		# check whether keys belong to products.csv file
		elif keys[0] == "product_id" and keys[1] == "product_name":
			reading_departments = True
			# add the department_id & product_id records to dept_dict, 
			# create a new Department_Record if one does not already 
			# exist for this department_id
			add_to_department_dict(dept_dict,digits[2], digits[0])
	#END loop
    
	if reading_orders:
		return prod_dict
	elif reading_departments:
		return dept_dict

#END function

def open_file(filepath):
	"""Open file and check if the file path is correct"""
	
	try:
		# open file
		file = open(filepath, 'r')
	    
	except IOError:
		print("\nERROR!! Input File not found or path is incorrect")
		print("Program will exit now\n")
		exit()
		
	else:
		# read file
		with file as file_open:
			# process file info and
			# save results in data
			data = read_csv(file_open)
		# close file
		file.close()
		# return data
		return data

#END function

def save_file(filepath, data):
	"""Save the results in a csv format file"""
	
	try:
		# create file
		file = open(filepath, "x")
	
	except IOError:
		print("\nWarning!! Output File already exist")
		print("File will be appended\n")
		file = open(filepath, "a")
	    
	finally:
		# write file headder
		file.write("department_id,number_of_orders,number_of_first_orders,percentage\n")
		# print data records
		for record in sorted(data):
			# print only if number_of_orders > 0
			if record[1] > 0:
				file.write("%i,%i,%i,%.2f\n" % (record[0],record[1],record[2],record[3]))
		# close file
		file.close()

#END function

def main():
	'''Main Routine'''
    
	###########################################################################################
	#  Input files									          #
	###########################################################################################

	ORDERS_PATH = sys.argv[1]
	PRODSD_PATH = sys.argv[2]
	REPORT_PATH = sys.argv[3]
	
	# open file and process data
	orders = open_file(ORDERS_PATH)
	deppro = open_file(PRODSD_PATH)

	###########################################################################################
        # Generate report: 								          #
	# 		1) a list of department_ids in ascending order                            #
	#		2) number_of_orders: count multiple requests of same product  		  #
	#		3) percentage: number_of_first_orders divided by number_of_orders         #
	#											  #
        ###########################################################################################

	# report list, one entry for each department_id:
	#
	# report[0] = department_id
	# report[1] = number_of_orders
	# report[2] = number_of_first_orders
	# report[3] = percentage
	
	# report
	report = [[0,0,0,0] for i in range(len(deppro))]
	
	# calculate the <float> division of number_of_orders <int>
	ratio = (lambda x,y: float(x)/float(y) if y > 0. else 0.)
	
	# loop over all departments_id
	for c,v in enumerate(deppro):
		
		# save departments_id 
		report[c][0] = deppro[v].dept_id
		
		# number_of_orders
		report[c][1] = sum([orders[p].number_of_orders # sum all orders from
		                  for p in deppro[v].products # all products from department 
				  if orders.get(p, None) is not None]) # check if the product has been ordered
		# number_of_first_orders
		report[c][2] = sum([orders[p].number_of_first_orders # sum all first orders
		                  for p in deppro[v].products # all products from department
				  if orders.get(p, None) is not None]) # check the product has been ordered
		# ratio
		report[c][3] = ratio(report[c][2],report[c][1])
		
	#END cycle
	
	###########################################################################################	
	# Save report										  #
	###########################################################################################

	save_file(REPORT_PATH, report)

#END function

if __name__ == "__main__":
	
	# start the time count
	start_time = time.time()
	
	# main routine
	main()
	
	# print the total time
	elapsed = (time.time() - start_time)/60.
	print("--- %.2f minutes ---" % elapsed)

#END program
