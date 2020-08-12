import os, requests, json
import azure.cognitiveservices.speech as speechsdk
import time
import wave

speech_key, service_region = "81286058da9045db800eb60035324009", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def get_recognizer(audio_filename, language):
    done = False
    audio_input = speechsdk.AudioConfig(filename=audio_filename)
    lst = list()

    '''
    supports = ["en-US", "de-DE", "ar-AE", "ar-BH", "ar-EG", "ar-IL", 
    "ar-JO", "ar-KW", "ar-LB", "ar-PS", "ar-QA", "ar-SA", "ar-SY", 
    "ca-ES", "cs-CZ", "da-DK", "fr-FR", "en-AU", "en-CA", "en-HK", 
    "en-IE", "en-GB", "en-IN", "en-NZ", "en-PH", "en-SG", "en-ZA", 
    "es-AR", "es-BO", "es-CL", "es-CO", "es-CR", "es-CU", "es-DO", 
    "es-EC", "es-ES", "es-GT", "es-HN", "es-MX", "es-NI", "es-PA", 
    "es-PE", "es-PR", "es-PY", "es-SV", "es-US", "es-UY", "es-VE", 
    "fi-FI", "fr-CA", "gu-IN", "hi-IN", "hu-HU", "it-IT", "ja-JP", 
    "ko-KR", "mr-IN", "nb-NO", "nl-NL", "pl-PL", "pt-BR", "pt-PT", 
    "ru-RU", "sv-SE", "ta-IN", "te-IN", "th-TH", "tr-TR", "zh-CN", 
    "zh-HK", "zh-TW"]
    '''

    if language == 'auto':
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "de-DE", "fr-FR", "es-ES"])
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config, audio_config=audio_input)
    else:
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_input)

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def combine(x):
        nonlocal lst
        lst.append(x)

    speech_recognizer.recognized.connect(lambda evt: combine(evt.result.text))
    #print(lst)
    speech_recognizer.session_started.connect(lambda evt: print(evt.result.text))
    speech_recognizer.session_stopped.connect(lambda evt: evt)
    speech_recognizer.canceled.connect(lambda evt: evt)
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(5)

    speech_recognizer.stop_continuous_recognition()

    s = " ".join(lst)
    print(s)
    data = {"text": s}
    return json.dumps(data)