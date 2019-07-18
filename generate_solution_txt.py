import sys

def generate_solution(filepath):
	if '-W' not in filepath:
		print('The input raw file must be -W.raw.')
		return

	raw_file = open(filepath, 'r')
	solution_file = open(filepath.replace('-W.raw', '_solution1.txt'), 'w+')


	# Start writing the bus section
	solution_file.write('-- bus section\ni, v(p.u.), theta(deg), bcs(MVAR at v = 1 p.u.)')

	# get to the first line of bus table
	current_line = raw_file.readline()
	current_line = raw_file.readline()
	current_line = raw_file.readline()

	bus_section_values = {}
	# read through the bus table
	while True:
		current_line = raw_file.readline()
		if 'END OF BUS DATA' in current_line:
			break
		current_value = current_line.split(',')
		bus_section_values.update({current_value[0]:current_value})
	# read through the unused table
	while True:
		current_line = raw_file.readline()
		if 'BEGIN SWITCHED SHUNT DATA' in current_line:
			break
	# read through the switched shunt table
	while True:
		current_line = raw_file.readline()
		if 'END OF SWITCHED SHUNT DATA' in current_line:
			break
		switch_value = current_line.split(',')
		bus_section_values[switch_value[0]] = (bus_section_values[switch_value[0]], switch_value[9])
		#print('new bus vale: ', bus_section_values[switch_value[0]])
	# write the values to te bus section
	for key in bus_section_values:
		bus_values = bus_section_values[key]
		#print('print value:', bus_values)
		if len(bus_values) == 13:
			solution_file.write(bus_values[0] + ', ' + bus_values[7] + ', ' + bus_values[8] + ', ' + '0.0\n')
		else:
			solution_file.write(bus_values[0][0]+', '+ bus_values[0][7]+ ', '+ bus_values[0][8]+ ', '+ bus_values[1]+'\n')

	solution_file.write('-- generator section\ni, id, p(MW), q(MVAR)')
	raw_file.close()
	raw_file = open(filepath, 'r') # open a new one to read the switch shunt table


	# START WRITING THE generator section
	while True:
		current_line = raw_file.readline()
		if 'BEGIN GENERATOR DATA' in current_line:
			break
	while True:
		current_line = raw_file.readline()
		if 'END OF GENERATOR DATA' in current_line:
			break
		generator_values = current_line.split(',')
		solution_file.write(generator_values[0]+ ', '+ generator_values[1]+ ', '+ 
							generator_values[2]+ ', '+ generator_values[3]+'\n')





if __name__ == '__main__':
	generate_solution(sys.argv[1])
	print('Finished')