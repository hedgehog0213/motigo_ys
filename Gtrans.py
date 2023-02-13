from googletrans import Translator

tr = Translator()

def en_to_ko(en_text):
    result = tr.translate(en_text, dest="ko")
    print(result)
    return result

def ko_to_en(ko_text):
    result = tr.translate(ko_text, dest="en")
    print(result.text)
    return result

def en_to_ko_text(en_text):
    result = tr.translate(en_text, dest="ko")
    print( result.text)
    return result.text

def ko_to_en_text(ko_text):
    result = tr.translate(ko_text, dest="en")
    print(result.text)
    return result.text


#만약 source가 영어라면 > 한국어로
#만약 source가 한국어라면 > 영어로
#출력값은 결과.text로 반환한다.
