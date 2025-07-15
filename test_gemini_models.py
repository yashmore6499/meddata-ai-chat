import google.generativeai as genai

genai.configure(api_key="AIzaSyBzV_5eTAXMpSw6Ircz1EClFPi24X2c2uc")

models = genai.list_models()
for model in models:
    print(f"Model: {model.name}")
    print(f"Supports generation: {'generateContent' in model.supported_generation_methods}")
    print("-----")
