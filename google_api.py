def translate_to_en_text(text,target = 'en' ):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    #print(u"Text: {}".format(result["input"]))
    #return(u"Translation: {}".format(result["translatedText"]))
    return (result["translatedText"])
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


def translate_to_ko_text(text,target = 'ko' ):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    #print(u"Text: {}".format(result["input"]))
    #return(u"Translation: {}".format(result["translatedText"]))
    return (result["translatedText"])
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


#translate_to_ko_text('hello') ## 영어에서 한국어로
#translate_to_en_text('안녕하세요') ## 한국에서 영어로