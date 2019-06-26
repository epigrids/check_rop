import pandas as pd
import os
import sys
import pdb


def check_rop():
	files = []
	for r, d, f in os.walk(sys.argv[1]):
		for file in f:
			if '.rop' in file:
				files.append(os.path.join(r, file))

	print('Tested files:')
	for file in files:
		print(file)
	print('')

	df = pd.DataFrame(columns = ['BUS_NUM', 'ID', 'MW1', 
		'$1', 'MW2', '$2', 'SLOPE', 'VERSION'])

	df = read_files(files, df)
	print(df)

	casename = files[0][:-7]
	df.to_csv(casename + '.csv')

	return




def read_files(files, df):
	version_num = 0
	for file in files:

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

		df = insert_into_df(bus_num_id_list, MW_cost_dict, df, version_num)
		f.close()
		version_num += 1

	return df

"""'BUS_NUM', 'ID', 'MW1', '$1', 'MW2', '$2', 'SLOPE', 'VERSION'"""
def insert_into_df(bus_num_id_list, MW_cost_dict, df, version_num):
	for bus_num_id_tuple in bus_num_id_list:
		# for n points, we have n-1 slopes
		point_list = MW_cost_dict[bus_num_id_tuple[2]]
		for i in range(len(MW_cost_dict[bus_num_id_tuple[2]])-1):
			point1 = point_list[i]
			point2 = point_list[i+1]
			slope = (float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))
			
			df = df.append({'BUS_NUM': bus_num_id_tuple[0],
							'ID': bus_num_id_tuple[1],
							'MW1': point1[0],
							'$1': point1[1],
							'MW2': point2[0],
							'$2': point2[1],
							'SLOPE': slope,
							'VERSION': version_num}, ignore_index = True)
	return df





if __name__ == '__main__':
	check_rop()