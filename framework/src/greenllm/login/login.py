from huggingface_hub import login

def login_hugging_face():
    with open("../api_h.key", "r") as f:

        API_KEY = f.read().strip()

    login(API_KEY)   
    print()