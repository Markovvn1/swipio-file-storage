import random
import string


def generate_unique_identifier():
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for i in range(32)
    )
