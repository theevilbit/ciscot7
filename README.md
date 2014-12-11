Cisco Type 7 Password Decrypter
===============================
Small tool to decrypt Cisco IOS type 7 passwords, it can also encrypt clear text passwords if required. 

Usage
=====

```
c:\>ciscot7.py --help
Usage: ciscot7.py [options]

Options:
  -h, --help            show this help message and exit
  -e, --encrypt         Encrypt password
  -d, --descrypt        Decrypt password. This is the default
  -p PASSWORD, --password=PASSWORD
                        Password to encrypt / decrypt
  -f FILE, --file=FILE  Cisco config file, only for decryption
```

If we specify a config file, it will look for all type 7 passwords in it.