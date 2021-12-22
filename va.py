import speech_recognition
import pyttsx3 
from neuralintents import GenericAssistant
import sys 

recognizer=speech_recognition.Recognizer()
speaker=pyttsx3.init()
speaker.setProperty('rate',100)

# med_lists = ['Take medicines','Sleep','Doctor appointment']


def create_reminder():
    global recognizer
    speaker.say("What do you wantt to set a reminder about?")
    speaker.runAndWait()

    done=False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio=recognizer.listen(mic)
                reminder=recognizer.recognize_google(audio)
                reminder=reminder.lower()
                speaker.say("Choose a name")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio=speaker.listen(mic)
                name=recognizer.recognize_google(audio)
                name=name.lower()

            with open(name,'w') as f:
                f.write(reminder)
                done=True
                speaker.say(f"Successfully set the reminder {name}")
                speaker.runAndWait()

                except speech_recognition.UnknownValueError:
                    recognizer=speech_recognition.Recognizer()
                    speaker.say("Did not catch that, please try again")
                    speaker.runAndWait()

def show_reminders():
    speaker.say("The reminders you have set are")
    for item in create_reminder:
        speaker.say(item)
    speaker.runAndWait()

def greet():
    speaker.say("Hi, what can I do for you?")
    speaker.runAndWait()

def quit():
    speaker.say("Goodbye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    "greeting":hello,
    "create_reminder":create_reminder,
    "show_reminders":show_reminders,
    "exit":quit
}
assistant=GenericAssistant('neural.json')
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=0.2)
            audio=recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message=message.lower()
         assistant.request(message)
    
    except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()