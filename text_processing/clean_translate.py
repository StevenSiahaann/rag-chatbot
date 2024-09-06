from googletrans import Translator
def clean_prompt(prompt):
    return ' '.replace("\n", " ").replace("\r", " ").join(prompt.strip().split())

def translate_to_english(prompt):
    translator = Translator()
    try:
        return translator.translate(prompt, dest='en').text
    except Exception as e:
        print(f"Translation error: {e}")
        return prompt

def clean_and_translate_prompt(prompt):
    return translate_to_english(clean_prompt(prompt))
