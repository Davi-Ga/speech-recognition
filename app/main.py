from utils.speech import SpeechRecognize
import os
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
SERVICE_REGION = os.getenv('SERVICE_REGION')

Recognizer = SpeechRecognize(SUBSCRIPTION_KEY, SERVICE_REGION, "YourAudioFile")

