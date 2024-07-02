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
        
    def speech_recognize_once_from_file(self):
        """performs one-shot speech recognition with input from an audio file"""
        # <SpeechRecognitionWithFile>
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        audio_config = speechsdk.audio.AudioConfig(filename=self.weatherfilename)
        # Creates a speech recognizer using a file as audio input, also specify the speech language
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, language="de-DE", audio_config=audio_config)

        # Starts speech recognition, and returns after a single utterance is recognized. The end of a
        # single utterance is determined by listening for silence at the end or until a maximum of 15
        # seconds of audio is processed. It returns the recognition text as result.
        # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
        # shot recognition like command or query.
        # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
        result = speech_recognizer.recognize_once()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))