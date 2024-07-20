from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.schema.output_parser import StrOutputParser
from deepgram import DeepgramClient, SpeakOptions
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from playsound import playsound
import time

DEEPGRAM_API_KEY = "your deepgram api key"


class PomodoroGpt:
    store = {}

    def __init__(self, topic: str) -> None:
        self.topic = topic

    def reminder(self, type: str) -> None:
        playsound(f"/home/faizan/Documents/PomodoroGPT/reminder_sounds/{type}")

    def text_to_voice(self, TEXT: str) -> None:
        try:
            deepgram = DeepgramClient(DEEPGRAM_API_KEY)

            options = SpeakOptions(
                model="aura-asteria-en",
            )
            FILENAME = "/home/faizan/Documents/PomodoroGPT/reminder_sounds/audio.mp3"
            deepgram.speak.v("1").save(FILENAME, {"text": TEXT}, options)
            playsound(FILENAME)

        except Exception as e:
            print(f"Exception: {e}")

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def generate_quiz(self) -> None:
        chain = (
            PromptTemplate.from_template(
                """Please generate a only one unique quiz on that topic. The quiz should contain concise question and four options. Please do not generate a lengthy quiz; keep it as short as possible. {topic}"""
            )
            | ChatGroq(model_name="mixtral-8x7b-32768")
            | StrOutputParser()
        )
        wrapped_chain = RunnableWithMessageHistory(chain, self.get_session_history)
        self.text_to_voice(
            wrapped_chain.invoke(
                self.topic, config={"configurable": {"session_id": "abc123"}}
            )
        )

    def pomodoro_timer(self) -> None:
        """Implements a Pomodoro timer with 25 minutes work and 5 minutes break."""

        while True:  # Loop for continuous cycles
            # Work session
            print("Starting work session...")
            self.reminder("25minutesfocusstarted.mp3")
            time.sleep(1500)  # 25 minutes in seconds
            self.reminder("25minutesfoucended.mp3")

            # Break session
            print("Time for a break!")
            time.sleep(300)  # 5 minutes in seconds
            self.reminder("breaktimeendandquizreminder.mp3")
            self.generate_quiz()


user1 = PomodoroGpt(input("Enter topic:"))
user1.pomodoro_timer()
# user1.text_to_voice("my name is Muhammad.")
