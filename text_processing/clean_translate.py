# from googletrans import Translator
from deep_translator import GoogleTranslator

def translate_to_english(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)
def clean_prompt(prompt):
    return ' '.replace("\n", " ").replace("\r", " ").join(prompt.strip().split())
def clean_and_translate_prompt(prompt):
    return translate_to_english(clean_prompt(prompt))
