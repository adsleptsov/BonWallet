from werkzeug.security import generate_password_hash
import sys

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print("not enough arguments provided")

file = open('pw_hashes.txt', 'a')

print(generate_password_hash(password), file=file)

file.close()
