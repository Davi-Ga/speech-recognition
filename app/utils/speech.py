import difflib
import json
import string
import time
import azure.cognitiveservices.speech as speechsdk


class PronunciationAssessment:
    def __init__(self, subscription_key, service_region, file, text):
        self.subscription_key = subscription_key
        self.service_region = service_region
        self.file = file or "audio/whatstheweatherlike.wav"
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key, region=self.service_region
        )
        self.audio_config = speechsdk.audio.AudioConfig(filename=self.file)
        self.reference_text = text or "What is the weather like."
        self.enable_miscue = True
        self.enable_prosody_assessment = True
        self.pronunciation_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=self.reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=self.enable_miscue,
        )
        if self.enable_prosody_assessment:
            self.pronunciation_config.enable_prosody_assessment()
        self.language = "en-US"
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            language=self.language,
            audio_config=self.audio_config,
        )
        self.pronunciation_config.apply_to(self.speech_recognizer)
        self.done = False
        self.recognized_words = []
        self.fluency_scores = []
        self.prosody_scores = []
        self.durations = []

    def canceled(self, evt):
        if evt.reason == speechsdk.CancellationReason.Error:
            print("Recognition canceled due to an error.")
            print(f"Error Details: {evt.error_details}")
            print(f"Error Code: {evt.error_code}")
        elif evt.reason == speechsdk.CancellationReason.EndOfStream:
            print("Recognition canceled because the end of the stream was reached.")
        else:
            print("Recognition canceled for another reason.")

    def stop_cb(self, evt):
        print("CLOSING on {}".format(evt))
        self.done = True

    def recognized(self, evt):
        print("Pronunciation assessment for: {}".format(evt.result.text))
        pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
        print(
            "    Accuracy score: {}, pronunciation score: {}, completeness score : {}, fluency score: {}, prosody score: {}".format(
                pronunciation_result.accuracy_score,
                pronunciation_result.pronunciation_score,
                pronunciation_result.completeness_score,
                pronunciation_result.fluency_score,
                pronunciation_result.prosody_score,
            )
        )
        self.recognized_words += pronunciation_result.words
        self.fluency_scores.append(pronunciation_result.fluency_score)
        self.prosody_scores.append(pronunciation_result.prosody_score)
        json_result = evt.result.properties.get(
            speechsdk.PropertyId.SpeechServiceResponse_JsonResult
        )
        jo = json.loads(json_result)
        nb = jo["NBest"][0]
        self.durations.append(sum([int(w["Duration"]) for w in nb["Words"]]))

    def connect_callbacks(self):
        self.speech_recognizer.recognized.connect(self.recognized)
        self.speech_recognizer.canceled.connect(self.canceled)
        self.speech_recognizer.session_started.connect(
            lambda evt: print("SESSION STARTED: {}".format(evt))
        )
        self.speech_recognizer.session_stopped.connect(
            lambda evt: print("SESSION STOPPED {}".format(evt))
        )
        self.speech_recognizer.canceled.connect(
            lambda evt: print("CANCELED {}".format(evt))
        )
        self.speech_recognizer.session_stopped.connect(self.stop_cb)
        self.speech_recognizer.canceled.connect(self.stop_cb)

    def start_assessment(self):
        self.connect_callbacks()
        self.speech_recognizer.start_continuous_recognition()
        while not self.done:
            time.sleep(0.5)
        self.speech_recognizer.stop_continuous_recognition()
        self.process_results()

    def process_results(self):
        reference_words = [
            w.strip(string.punctuation) for w in self.reference_text.lower().split()
        ]
        if self.enable_miscue:
            diff = difflib.SequenceMatcher(
                None, reference_words, [x.word.lower() for x in self.recognized_words]
            )
            final_words = []
            for tag, i1, i2, j1, j2 in diff.get_opcodes():
                if tag in ["insert", "replace"]:
                    for word in self.recognized_words[j1:j2]:
                        if word.error_type == "None":
                            word._error_type = "Insertion"
                        final_words.append(word)
                if tag in ["delete", "replace"]:
                    for word_text in reference_words[i1:i2]:
                        word = speechsdk.PronunciationAssessmentWordResult(
                            {
                                "Word": word_text,
                                "PronunciationAssessment": {
                                    "ErrorType": "Omission",
                                },
                            }
                        )
                        final_words.append(word)
                if tag == "equal":
                    final_words += self.recognized_words[j1:j2]
        else:
            final_words = self.recognized_words

        final_accuracy_scores = [
            word.accuracy_score
            for word in final_words
            if hasattr(word, "accuracy_score")
        ]
        accuracy_score = (
            sum(final_accuracy_scores) / len(final_accuracy_scores)
            if final_accuracy_scores
            else 0
        )
        fluency_score = (
            sum([x * y for (x, y) in zip(self.fluency_scores, self.durations)])
            / sum(self.durations)
            if self.durations
            else 0
        )
        completeness_score = (
            len([w for w in final_words if w.error_type == "None"])
            / len(reference_words)
            * 100
            if reference_words
            else 0
        )
        completeness_score = min(completeness_score, 100)
        prosody_score = (
            sum(self.prosody_scores) / len(self.prosody_scores)
            if self.prosody_scores
            else 0
        )
        pron_score = (
            accuracy_score * 0.4
            + prosody_score * 0.2
            + fluency_score * 0.2
            + completeness_score * 0.2
        )

        print(
            "    Paragraph pronunciation score: {}, accuracy score: {}, completeness score: {}, fluency score: {}, prosody score: {}".format(
                pron_score,
                accuracy_score,
                completeness_score,
                fluency_score,
                prosody_score,
            )
        )

        for idx, word in enumerate(final_words):
            print(
                "    {}: word: {}\taccuracy score: {}\terror type: {};".format(
                    idx + 1, word.word, word.accuracy_score, word.error_type
                )
            )
