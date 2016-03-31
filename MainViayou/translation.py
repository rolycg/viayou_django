from modeltranslation.translator import translator, TranslationOptions
from MainViayou.models import Countries


class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Countries, NewsTranslationOptions)
