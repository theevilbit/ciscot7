import re
import random
import optparse
"""
http://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566

To calculate xlat use the full p or full a password, after 51 charaters it's repeating.
The first 2 numbers (salt) are taken off

p = "140316144B1B161F315C5E19091507021B1C143A3B3438232532031706131146494843441E130806494847434245441B4B16174847"
a = "051207055A0A070E204D4F08180416130A0D052B2A2529323423120617020057585952550F021917585956525354550A5A07065956"
xlat = []
for i in range(len(a)/2):
	xlat.append(hex(int(a[2*i:2*i+2],16) ^ ord("a")))

print xlat

"""

xlat = [0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f, 0x41, 0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6b, 0x6c, 0x64
, 0x4a, 0x4b, 0x44, 0x48, 0x53, 0x55, 0x42, 0x73, 0x67, 0x76, 0x63, 0x61, 0x36, 0x39, 0x38, 0x33, 0x34, 0x6e, 0x63,
0x78, 0x76, 0x39, 0x38, 0x37, 0x33, 0x32, 0x35, 0x34, 0x6b, 0x3b, 0x66, 0x67, 0x38, 0x37]

			
def decrypt_type7(ep):
	"""
	Based on http://pypi.python.org/pypi/cisco_decrypt/
	Regex improved
	"""
	dp = ''
	regex = re.compile('(^[0-9A-Fa-f]{2})([0-9A-Fa-f]+)')
	result = regex.search(ep)
	s, e = int(result.group(1)), result.group(2)
	for pos in range(0, len(e), 2):
		magic = int(e[pos] + e[pos+1], 16)
		if s <= 50:
			# xlat length is 51
			newchar = '%c' % (magic ^ xlat[s])
			s += 1
		if s == 51: s = 0
		dp += newchar
	return dp

def encrypt_type7(pt):
	"""
	Make Type 7 Cisco password from a string
	"""
	salt = random.randrange(0,15);
	ep = "%02x" % salt
	for i in range(len(pt)):
		ep += "%02x" % (ord(pt[i]) ^ xlat[salt])
		salt += 1
		if salt == 51: salt = 0
	return ep

def main():
	usage = "Usage: %prog [options]"
	parser = optparse.OptionParser(usage=usage)
	parser.add_option('-e', '--encrypt', action='store_true', dest='encrypt', default=False, help='Encrypt password')
	parser.add_option('-d', '--decrypt', action='store_true', dest='decrypt',default=True, help='Decrypt password. This is the default')
	parser.add_option('-p', '--password', action='store', dest="password", help='Password to encrypt / decrypt')
	parser.add_option('-f', '--file', action='store', dest="file", help='Cisco config file, only for decryption')
	options, args = parser.parse_args()
	render_as = "files"

	#fix issue 1, if encrypt is selected, that takes precedence
	if (options.encrypt):
		options.decrypt = False
	if (options.password is not None):
		if(options.decrypt):
			print("Decrypted password: " + decrypt_type7(options.password))
		elif(options.encrypt):
			print("Encrypted password: " + encrypt_type7(options.password))
	elif (options.file is not None):
		if(options.decrypt):
			try:
				f = open(options.file)
				regex = re.compile('(7 )([0-9A-Fa-f]+)($)')
				for line in f:
					result = regex.search(line)
					if(result):
						print("Decrypted password: " + decrypt_type7(result.group(2)))
			except IOError:
				print("Couldn't open file: " + options.file)
		elif(options.encrypt):
			parser.error("You can't encrypt a config file\nPlease run 'python ciscot7.py --help' for usage instructions.")
	else:
		parser.error("Password or config file is not specified!\nPlease run 'python ciscot7.py --help' for usage instructions.")


if __name__ == '__main__':
	main()

