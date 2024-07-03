# from utils.speech import SpeechRecognize
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
SERVICE_REGION = os.getenv('SERVICE_REGION')

audio_file = "audio/audio.wav"

# Recognizer = SpeechRecognize(SUBSCRIPTION_KEY, SERVICE_REGION, audio_file)

from utils.speech import pronunciation_assessment_continuous_from_file

# pronunciation_assessment_continuous_from_file(SUBSCRIPTION_KEY, SERVICE_REGION, audio_file)

def main():
    # Substitua YOUR_SUBSCRIPTION_KEY e YOUR_SERVICE_REGION com seus valores

    # Cria uma configuração de fala
    speech_config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION)

    # Configura o áudio para usar o microfone padrão
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Cria uma instância do reconhecedor de fala
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Fale algo...")

    # Inicia a escuta do áudio do microfone
    result = speech_recognizer.recognize_once()

    # Verifica se a transcrição foi bem-sucedida
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Reconhecido: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Nenhum texto foi reconhecido.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Reconhecimento de fala cancelado: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Erro: {cancellation_details.error_details}")

if __name__ == "__main__":
    main()