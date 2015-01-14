# -*- coding: utf-8 -*-
puncRe=u'(\r|\n|,|"|\'|\(|\)|-|:|;|\.|!|\?|؟|،|؛|{|}|\[|\]|\\\)'
# Standard punctuation
underscoreRe=u'\_'
hashRe=u'\#'
# Underscore (for hashtags)
httpRe=u'http'
httpCleanRe=u'(\r|\n|"|”)'
atRe=u'\A\@'

alifRe=u'(آ|أ|إ|آ)'
alifMaksourRe=u'ى'
# Variations of letter alif
wawRe=u'ؤ'
# Letter waw
hahRe=u'ه\Z'
# Letter hah
alRe=u'(\Aال|\Aفال|\Aوال|\Aلل)'
# Variations of al
tuhaRe=u'تها\Z'
haRe=u'ها\Z'
# Strip feminine pronoun
verbSuffixesRe=u'(ون\Z|ين\Z|وا)'
# Verb sufixes
harakatRe=u'(ٍ|َ|ُ|ِ|ّ|ْ|ً)'
# Diacritics
# All unicode regular expressions must be uncompiled

