from abc import ABC, abstractmethod


class Player(ABC):

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class Hero(Player):

    """ class to wrap """
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }
        self.main_stats = ["Strength", "Perception", "Endurance",
                           "Charisma", "Intelligence", "Agility", "Luck"]

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, Player):

    """ Abstract class for pos/neg effects"""
    def __init__(self, base):
        super().__init__()
        self.base = base

    def get_positive_effects(self):
        return super().get_positive_effects()

    def get_negative_effects(self):
        return super().get_negative_effects()

    @abstractmethod
    def get_effect_stats(self):
        pass

    def get_stats(self):
        stats = self.base.get_stats()
        for st, val in self.get_effect_stats().items():
            stats[st] += val
        return stats


class AbstractPositive(AbstractEffect):

    """ Positive abstract class """
    def get_positive_effects(self):
        effects = self.base.get_positive_effects()
        effects.append(self.__class__.__name__)
        return effects

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_effect_stats(self):
        pass


class AbstractNegative(AbstractEffect):

    """ Negative abstract class """
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        effects = self.base.get_negative_effects()
        effects.append(self.__class__.__name__)
        return effects

    @abstractmethod
    def get_effect_stats(self):
        pass


class Berserk(AbstractPositive):

    def get_effect_stats(self):
        return {
            "Strength": 7, "Endurance": 7, "Agility": 7, "Luck": 7,
            "Perception": -3, "Charisma": -3, "Intelligence": -3,
            "HP": 50
        }


class Blessing(AbstractPositive):

    def get_effect_stats(self):
        delta = 2
        return {st: delta for st in self.main_stats}


class Weakness(AbstractNegative):

    def get_effect_stats(self):
        delta = -4
        return {st: delta for st in ("Strength", "Endurance", "Agility")}


class EvilEye(AbstractNegative):

    def get_effect_stats(self):
        return {"Luck": -10}


class Curse(AbstractNegative):

    def get_effect_stats(self):
        delta = -2
        return {st: delta for st in self.main_stats}


