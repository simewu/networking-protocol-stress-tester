import os
import re
import sys

# https://www.badunetworks.com/traffic-shaping-with-tc/

# Send a command to the linux terminal
def terminal(cmd):
	return os.popen(cmd).read()

# Change the color of text in the terminal
# Leaving the forground or background blank will reset the color to its default
# Providing a message will return the colored message (reset to default afterwards)
# If it's not working for you, be sure to call os.system('cls') before modifying colors
# Usage:
# - print(color('black', 'white', 'Inverted') + ' Regular')
# - print(color('black', 'white') + 'Inverted' + color() + ' Regular')
def color(foreground = '', background = '', message = ''):
	fg = {
		'red': '1;31',
		'green': '1;32',
		'yellow': '1;33',
		'blue': '1;34',
		'purple': '1;35',
		'cyan': '1;36',
		'white': '1;37',
		'black': '0;30',
		'gray': '1;30'
	}
	bg = {
		'red': ';41m',
		'green': ';42m',
		'yellow': ';43m',
		'blue': ';44m',
		'purple': ';45m',
		'cyan': ';46m',
		'white': ';47m',
		'black': ';48m'
	}
	if foreground not in fg or background not in bg: return '\033[0m' # Reset
	color = f'\033[0m\033[{ fg[foreground.lower()] }{ bg[background.lower()] }'

	if message == '': return color
	else: return f'{ color }{ str(message) }\033[0m'

# Draws the header
def header(message, width):
	print(color('black', 'white', ' ' * width))
	print(color('black', 'white', message.center(width)))
	print(color('black', 'white', ' ' * width))
	print()

# Draws the header
def subheader(message, width):
	print()
	print(color('cyan', 'blue', ' ' * width))
	print(color('cyan', 'blue', message.center(width)))
	print(color('cyan', 'blue', ' ' * width))
	print()

# Return an array of networking interfaces (minus localhost)
def get_interfaces():
	raw = terminal('ip link show')
	interfaces = re.findall(r'[0-9]+: ([^:]+): ', raw)
	interfaces.remove('lo')
	return interfaces

# Ask the user a yes/no question, returns True or False
def confirm(msg):
	response = ''
	while response not in ['y', 'n', 'yes', 'no']:
		response = input(f'{msg} (y/n): ').strip().lower()
	if response in ['y', 'yes']: return True
	else: return False

# Start of program
if __name__ == '__main__':
	os.system('clear')
	width = os.get_terminal_size().columns
	height = os.get_terminal_size().lines
	header('Networking Stress Tester', width)
	print('Intentionally delays, drops, corrupts, or reorders packets.')
	print()
	interfaces = get_interfaces()
	interface = ''
	if len(interfaces) == 0:
		print(terminal('ifconfig'))
		print()
		print('No networking interfaces were found.')
		sys.exit()

	elif len(interfaces) == 1:
		interface = interfaces[0]

	else:
		for i in range(0, len(interfaces)):
			print(f'{i + 1} : {interfaces[i]}')
		selection = -1
		while selection < 1 or selection > len(interfaces):
			try:
				selection = int(input(f'Please select an interface (1 to {len(interfaces)}): '))
			except: pass
		interface = interfaces[selection - 1]
		print()

	print(f'Using interface "{interface}"')
	print()
	check = terminal(f'tc -s qdisc ls dev {interface}')
	if 'netem' in check:
		reset = confirm('A packet filter has been detected. Remove it?')
		if reset:
			#terminal(f'sudo tc -s qdisc ls dev {interface}')
			terminal(f'sudo sudo tc qdisc del dev {interface} root netem')
			#terminal(f'sudo tc qdisc del dev {interface} handle ffff: ingress')
			#terminal(f'modprobe -r ifb')
			print('Current networking filters have been removed.')
		print()

	subheader('Packet delaying', width)
	delay = confirm('Would you like to delay the networking packets?')
	if delay:
		milliseconds = -1
		while(milliseconds < 0):
			try:
				milliseconds = float(input('How many milliseconds on average? '))
			except: pass

		randomness = -1
		while(randomness < 0):
			try:
				randomness = float(input(u'How many milliseconds of \u00B1 randomness? (causes re-ordering) '))
			except: pass

		if randomness != 0:
			normal_distribution = confirm('Would you like gaussian distribution?')
		else:
			normal_distribution = False

		cmd = f'sudo tc qdisc add dev {interface} root netem delay {milliseconds}ms'
		if randomness != 0:
			cmd += f' {randomness}ms'
		if normal_distribution:
			cmd += ' distribution normal'
		print()
		print(cmd)
		terminal(cmd)
		print()

	subheader('Packet dropping', width)
	drop = confirm('Would you like to drop the networking packets?')
	if drop:
		percent = -1
		while(percent < 0):
			try:
				percent = float(input('What percentage of packets would you like to drop? (0 to 100): '))
			except: pass
		cmd = f'sudo tc qdisc change dev {interface} root netem loss {percent}%'
		print(cmd)
		terminal(cmd)
		print()

	subheader('Packet duplicating', width)
	duplicate = confirm('Would you like to duplicate the networking packets?')
	if duplicate:
		percent = -1
		while(percent < 0):
			try:
				percent = float(input('What percentage of packets would you like to duplicate? (0 to 100): '))
			except: pass
		cmd = f'sudo tc qdisc change dev {interface} root netem duplicate {percent}%'
		print(cmd)
		terminal(cmd)
		print()

	subheader('Packet corrupting', width)
	corrupt = confirm('Would you like to corrupt the networking packets (flip a random bit)?')
	if corrupt:
		percent = -1
		while(percent < 0):
			try:
				percent = float(input('What percentage of packets would you like to corrupt? (0 to 100): '))
			except: pass
		cmd = f'sudo tc qdisc change dev {interface} root netem corrupt {percent}%'
		print(cmd)
		terminal(cmd)
		print()

	print()
	header('Goodbye', width)

	# reorder = confirm('Would you like to re-order the networking packets?')
	# if reorder:
	# 	percent = -1
	# 	while(percent < 0):
	# 		try:
	# 			percent = float(input('What percentage of packets would you like to re-order? (0 to 100): '))
	# 		except: pass


	# 	milliseconds = -1
	# 	while(milliseconds < 0):
	# 		try:
	# 			milliseconds = float(input('A delay is required. How many milliseconds? '))
	# 		except: pass

	# 	cmd = f'sudo tc qdisc change dev {interface} root netem delay {milliseconds} reorder {percent}%'
	# 	print(cmd)
	# 	terminal(cmd)
	# 	print()
