import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
import argparse
import sys
import pickle
import base64
import os


DATE_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


SSML = """\
<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="{voice_name}" style="{style}" styledegree="{styledegree}">
    {utterance}
  </voice>
</speak>
"""





class STT:
    def __init__(self, playback: bool = False) -> None:

        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) if playback else None
        speech_config = speechsdk.SpeechConfig(subscription= os.getenv("AZURE_API_KEY"), region="westeurope")
        self.voice_name = "it-IT-CalimeroNeural"
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        

    def __call__(
        self,
        style: str,
        styledegree: float,
        utterance: str
    ):
       

        ssml_string = SSML.format(
            voice_name=self.voice_name,
            style=style,
            styledegree=styledegree,
            utterance=utterance
        )

        result = self.synthesizer.speak_ssml(ssml_string)
        #result = self.synthesizer.speak_ssml_async(ssml_string).get()
        print("there3")
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            audio_data = base64.b64encode(audio_data)
            audio_duration = result.audio_duration
            
            return audio_duration, audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            self.logger.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
            print("there")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.logger.error("Error details: {}".format(cancellation_details.error_details))

            return None, []


if __name__ == "__main__":
    model = STT(True)

    utterance = "Quando c'è il sole le lucciole non brillano"

    audio_duration, audio = model(
        "default",
        1,
        utterance
    )
