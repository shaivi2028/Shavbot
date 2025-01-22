# import openai
# import pyttsx3
# import assemblyai as aai

# class AI_Assistant:
#     def __init__(self):
#         aai.settings.api_key = "ADD API KEY"
#         openai.api_key = "ADD API KEY"
#         self.full_transcript = [
#             {"role": "system", "content": "You are a friendly virtual assistant named ShavBot. Answer questions helpfully."},
#         ]
#         self.transcriber = None

#     def start_transcription(self):
#         self.transcriber = aai.RealtimeTranscriber(
#             sample_rate=16000,
#             on_data=self.on_data,
#             on_error=self.on_error,
#             on_open=self.on_open,
#             on_close=self.on_close,
#             end_utterance_silence_threshold=1000
#         )
#         self.transcriber.connect()
#         microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
#         self.transcriber.stream(microphone_stream)

#     def stop_transcription(self):
#         if self.transcriber:
#             self.transcriber.close()
#             self.transcriber = None

#     def on_open(self, session_opened: aai.RealtimeSessionOpened):
#         print("Session ID:", session_opened.session_id)

#     def on_data(self, transcript: aai.RealtimeTranscript):
#         if not transcript.text.strip():
#             print("No speech detected.")
#             return

#         if isinstance(transcript, aai.RealtimeFinalTranscript):
#             self.generate_ai_response(transcript)
#         else:
#             print(transcript.text, end="\r")

#     def on_error(self, error: aai.RealtimeError):
#         print("An error occurred:", error)

#     def on_close(self):
#         print("Closing Session")

#     def generate_ai_response(self, transcript):
#         self.stop_transcription()
#         self.full_transcript.append({"role": "user", "content": transcript.text})
#         print(f"\nYou: {transcript.text}")

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=self.full_transcript
#         )
#         ai_response = response.choices[0].message.content

#         self.generate_audio(ai_response)
#         self.start_transcription()

#     def generate_audio(self, text):
#         self.full_transcript.append({"role": "assistant", "content": text})
#         print(f"ShavBot: {text}")
#         engine = pyttsx3.init()
#         engine.say(text)
#         engine.runAndWait()

# greeting = "Hello! I am ShavBot. How can I assist you today?"
# ai_assistant = AI_Assistant()
# ai_assistant.generate_audio(greeting)
# ai_assistant.start_transcription()


import openai
import pyttsx3
import assemblyai as aai
import sounddevice as sd
import scipy.io.wavfile as wav
import time

class AI_Assistant:
    def __init__(self):
        aai.settings.api_key = "ADD API KEY"
        openai.api_key = "ADD API KEY"
        self.full_transcript = [
            {"role": "system", "content": "You are a friendly virtual assistant named ShavBot. Answer questions helpfully."},
        ]

    def record_audio(self):
        print("Recording your voice for 5 seconds...")
        sample_rate = 16000
        duration = 5
        recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        wav.write("audio.wav", sample_rate, recording)
        print("Recording complete!")

    def transcribe_audio(self, audio_file_path):
        print("Sending audio to AssemblyAI for transcription...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)

        while transcript.status not in ["completed", "failed"]:
            print("Waiting for transcription to complete...")
            time.sleep(3)
            transcript = transcriber.get_transcription(transcript.id)

        if transcript.status == "completed":
            print(f"Transcription: {transcript.text}")
            return transcript.text
        else:
            print("Transcription failed.")
            return ""

    def generate_ai_response(self, user_input):
        self.full_transcript.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )
        ai_response = response.choices[0].message.content
        self.full_transcript.append({"role": "assistant", "content": ai_response})
        return ai_response

    def speak_text(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()

    def start(self):
        print("ShavBot is ready! Say 'exit' to quit.")
        while True:
            self.record_audio()
            transcript = self.transcribe_audio("audio.wav")
            if "exit" in transcript.lower():
                print("Goodbye!")
                self.speak_text("Goodbye!")
                break
            if not transcript:
                print("No valid transcription. Please try again.")
                continue
            response = self.generate_ai_response(transcript)
            print(f"ShavBot: {response}")
            self.speak_text(response)
    
    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"ShavBot: {text}")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
greeting = "Hello! I am ShavBot. How can I assist you today?"
ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start()
