import base64

def decode_secret(encoded_secret):
    # This is not the real secret, just a distraction!
    return base64.b64decode(encoded_secret).decode('utf-8')

encoded_flag = "VEhJU19JU19UR0hfRkxBRw=="

# Your mission, should you choose to accept it, is to find the real flag.
# The flag is NOT what is returned by the decode_secret function.
