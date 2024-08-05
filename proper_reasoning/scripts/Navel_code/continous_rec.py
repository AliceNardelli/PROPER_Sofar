import azure.cognitiveservices.speech as speechsdk

# Define the callback functions
def speech_start_detected_callback(evt):
    print("Speech start detected: {}".format(evt))

def speech_end_detected_callback(evt):
    print("Speech end detected: {}".format(evt))

def recognized_callback(evt):
    print("Recognized: {}".format(evt.result.text))

def recognizing_callback(evt):
    print("Recognizing: {}".format(evt.result.text))

def session_started_callback(evt):
    print("Session started: {}".format(evt))

def session_stopped_callback(evt):
    print("Session stopped: {}".format(evt))

def canceled_callback(evt):
    print("Canceled: {}".format(evt))

# Set up the speech configuration
speech_key = "c6986565293c45098cb640f879d80254"
service_region = "westeurope"
language = "it-IT"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language=language)
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Connect the callbacks
recognizer.recognized.connect(recognized_callback)
recognizer.recognizing.connect(recognizing_callback)
recognizer.session_started.connect(session_started_callback)
recognizer.session_stopped.connect(session_stopped_callback)
recognizer.canceled.connect(canceled_callback)

recognizer.speech_start_detected.connect(speech_start_detected_callback)
recognizer.speech_end_detected.connect(speech_end_detected_callback)

# Start continuous recognition
print("Starting continuous recognition...")
recognizer.start_continuous_recognition()

try:
    # Keep the script running to listen to events
    while True:
        pass
except:
    # Stop recognition on user interrupt
    print("Stopping recognition...")
    recognizer.stop_continuous_recognition()
