from googletrans import Translator

translator = Translator()

a = translator.translate('hello!!', src='en', dest='ko')

print(a.text)