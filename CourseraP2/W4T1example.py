class Character:

    def __init__(self):
        self.name = "Nagibator"
        self.xp = 0
        self.taken_quests = set()
        self.passed_quests = set()


QUEST_SPEAK, QUEST_HUNT, QUEST_CARRY = "QSPEAK", "QHUNT", "QCARRY"


class Event:

    def __init__(self, kind):
        self.kind = kind


class Quest:

    @staticmethod
    def _quest(char, quest_name, xp):
        if quest_name not in (char.passed_quests | char.taken_quests):
            print(f"Quest received: {quest_name}")
            char.taken_quests.add(quest_name)
        elif quest_name in char.taken_quests:
            print(f"quest passed: {quest_name}")
            char.passed_quests.add(quest_name)
            char.taken_quests.remove(quest_name)
            char.xp += xp


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor:
            self.__successor.handle(char, event)


class QuestSpeak(NullHandler, Quest):

    def add_quest_speak(self, char, quest_name="Talk to farmer", xp=100):
        self._quest(char, quest_name, xp)

    def handle(self, char, event):
        if event.kind == QUEST_SPEAK:
            self.add_quest_speak(char)
        else:
            print("Handing over...")
            super().handle(char, event)


class QuestHunt(NullHandler, Quest):

    def add_quest_hunt(self, char, quest_name="Rats hunt", xp=300):
        self._quest(char, quest_name, xp)

    def handle(self, char, event):
        if event.kind == QUEST_HUNT:
            self.add_quest_hunt(char)
        else:
            print("Handing over...")
            super().handle(char, event)


class QuestCarry(NullHandler, Quest):

    def add_quest_carry(self, char, quest_name="Take boards from the shed", xp=200):
        self._quest(char, quest_name, xp)

    def handle(self, char, event):
        if event.kind == QUEST_CARRY:
            self.add_quest_carry(char)
        else:
            print("Handing over...")
            super().handle(char, event)


class QuestGiver:

    def __init__(self):
        self.handlers = QuestCarry(QuestHunt(QuestSpeak(NullHandler)))
        self.events = []

    def add_events(self, event):
        self.events.append(event)

    def handle_quests(self, char):
        for event in self.events:
            self.handlers.handle(char, event)


events = [Event(QUEST_CARRY), Event(QUEST_HUNT), Event(QUEST_SPEAK)]

quest_giver = QuestGiver()

for event in events:
    quest_giver.add_events(event)

player = Character()

quest_giver.handle_quests(player)
player.taken_quests = {"Talk to farmer", "Take boards from the shed"}
quest_giver.handle_quests(player)
print(player.taken_quests, player.passed_quests)