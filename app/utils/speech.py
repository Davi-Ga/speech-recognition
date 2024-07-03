import difflib
import json
try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


class SpeechRecognize():
    def __init__(self, speech_key, service_region,file):
        self.speech_key = speech_key
        self.service_region = service_region
        self.file = file
        
    def pronunciation_assessment_continuous_from_file():
        """Performs continuous pronunciation assessment asynchronously with input from an audio file.
            See more information at https://aka.ms/csspeech/pa"""

        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        speech_config = speechsdk.SpeechConfig(subscription="YourSubscriptionKey", region="YourServiceRegion")
        # provide a WAV file as an example. Replace it with your own.
        audio_config = speechsdk.audio.AudioConfig(filename="Exemplo_1.wav")

        reference_text = "Today was a beautiful day. We had a great time taking a long walk outside in the morning. The countryside was in full bloom, yet the air was crisp and cold. Towards the end of the day, clouds came in, forecasting much needed rain."
        # create pronunciation assessment config, set grading system, granularity and if enable miscue based on your requirement.
        enable_miscue = True
        enable_prosody_assessment = True
        pronunciation_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=enable_miscue)
        if enable_prosody_assessment:
            pronunciation_config.enable_prosody_assessment()

        # Creates a speech recognizer using a file as audio input.
        language = 'en-US'
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)
        # apply pronunciation assessment config to speech recognizer
        pronunciation_config.apply_to(speech_recognizer)

        done = False
        recognized_words = []
        fluency_scores = []
        prosody_scores = []
        durations = []

