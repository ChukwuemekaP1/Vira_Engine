import google.generativeai as genai

genai.configure(api_key="AIzaSyAkjX6h9Ii-nmfp3mLaHEiUnmP1FNln9rA")
for m in genai.list_models():
    print(m.name)
