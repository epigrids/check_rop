import os
import sys
import numpy
import csv

def retrieve_a_b(file):
	
	bus_num_id_list, MW_cost_dict = get_rop_information(file)

	filename = file.split('\\')[-1][:-4]
	print(filename)

	constant_file = open("a_b_of_" + filename + ".csv","w", newline = '')
	wrt = csv.writer(constant_file)
	wrt.writerow(('Busnum', 'Id', 'alpha', 'beta'))

	for busnum_id in bus_num_id_list:
		points = MW_cost_dict[busnum_id[2]]
		
		point1_x = float(points[0][0])
		point1_y = float(points[0][1])
		point2_x = float(points[1][0])
		point2_y = float(points[1][1])
		
		a, b = calculate_a_b(point1_x, point1_y, point2_x, point2_y)

		wrt.writerow((busnum_id[0], busnum_id[1], a, b))


	constant_file.close()



def calculate_a_b(x1, y1, x2, y2):
	y = numpy.array([[y1], [y2]])
	x = numpy.array([[x1*x1, x1], [x2*x2, x2]])
	
	result = numpy.linalg.inv(x) @ y
	a = result[0][0]
	b = result[1][0]
	# print('Second result ', a, b)

	return a, b


def get_rop_information(file):

	print('Processing ' + file)
	f = open(file, 'r')

	table_num = 1	# determine which table to read
	table_find = 0	# 0 if the current line is '0 /.....' instead of content
	bus_num_id_list = []	# list used to store the busNum and ID and corresponding cost table
	MW_cost_dict = {}	# dictionary used to store table_id : cost points

	while True:

		current_line = f.readline()
		# read first table
		if table_num == 1:

			if '0 /' in current_line:
				if table_find == 1:
					table_num = 2
					table_find = 0
				continue
			table_find = 1

			# start to fetch the bus number and the id number from the line
			first_table_split = current_line.split()[0].split(',')
			num_and_id_tuple = (first_table_split[0], 
						first_table_split[1], first_table_split[3])
			bus_num_id_list.append(num_and_id_tuple)

		# scan second table without checking
		if table_num == 2:
			
			if '0 /' in current_line:
				if table_find == 1:
					table_num = 3
					table_find = 0
				continue
			table_find = 1
			
		# read third table
		if table_num == 3:
			
			if '0 /' in current_line:
				if table_find == 1:
					break
				continue
			if ' ' in current_line:
				third_table_split = current_line.split(',')
				table_id = third_table_split[0]
				point_num = third_table_split[2].replace(' ', '').replace('\n', '')
				
				point_list = []
				for i in range(int(point_num)):
					current_line = f.readline()
					split_point = current_line.split()[0].split(',')
					point_list.append((split_point[0], split_point[1]))
				MW_cost_dict.update({table_id : point_list})

			table_find = 1

	f.close()

	return bus_num_id_list, MW_cost_dict





if __name__ == '__main__':
	files = []
	for r, d, f in os.walk(sys.argv[1]):
		for file in f:
			if '.rop' in file:
				files.append(os.path.join(r, file))

	for file in files:
		print(file)
		retrieve_a_b(file)