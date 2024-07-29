import secrets

# Generate a secret key
secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Print the secret key (you can store this in a safe place)
print(secret_key)