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
	while response not in ['y', 'n', 'yes', 'no', '\n']:
		response = input(f'{msg} (y/n): ').strip().lower()
	if response in ['y', 'yes']: return True
	else: return False

# Start of program
if __name__ == '__main__':
	width = os.get_terminal_size().columns
	height = os.get_terminal_size().lines
	
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

	print()
	print()
	print(f'Using interface "{interface}"')
	cmd = f'sudo sudo tc qdisc del dev {interface} root netem'
	print(cmd)
	terminal(cmd)

	header('All filters have been cleared.', width)
	