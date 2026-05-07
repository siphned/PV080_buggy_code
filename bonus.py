import os
import json

SECRET_KEY = os.urandom(32)


class Profile:
    def __init__(self):
        self.secret_key = None
        self.name = "Default name"
        self.address = "Default address"
        self.age = -1
        self.extra = {
            "hobbies": ["Default hobby"],
        }

    def __str__(self):
        return json.dumps(
            {
                "name": self.name,
                "address": self.address,
                "age": self.age,
                "extra": self.extra,
            },
            indent=4,
        )


def merge(src, dst):
    # Recursive merge function
    for k, v in src.items():
        if hasattr(dst, "__getitem__"):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)


profile = Profile()

for _ in range(100):
    try:
        merge(json.loads(input("input json info to update profile>>>")), profile)
    except Exception as e:
        print("Error: ", e)
        continue
    if profile.secret_key == SECRET_KEY:
        print("You found the secret key! Now show your exploit to the tutor.")
        break

    print("Profile updated: ", profile)
