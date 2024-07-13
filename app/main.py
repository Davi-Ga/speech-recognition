# from utils.speech import SpeechRecognize
import os
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
SERVICE_REGION = os.getenv('SERVICE_REGION')

audio_file = "audio/whatstheweatherlike.wav"

text = "What is the weather like."

from utils.speech import PronunciationAssessment

assessment = PronunciationAssessment(SUBSCRIPTION_KEY, SERVICE_REGION, audio_file, text)

# Iniciando a avaliação da pronúncia
assessment.start_assessment()