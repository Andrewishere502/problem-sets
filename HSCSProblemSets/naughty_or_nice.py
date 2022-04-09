from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from typing import Iterable, Union

class GoodnessSniffer:
    def __init__(self):
        self.special_stems = {
                "gave": "give"
            }
        self.nltk_stemmer = PorterStemmer().stem
        self.stopwords = stopwords.words("english")

        # Rate each verb -1 to 1 (inclusive). Value should be negative
        # for bad verbs and positive for good verbs.
        self.verbs = {
                # bad
                "kill": -0.9,
                "hurt": -0.8,
                "murder": -1,
                "hit": -0.7,
                "punch": -0.7,
                "lie": -0.4,

                # good
                "help": 0.7,
                "give": 0.5,
                "teach": 0.4,
                "learn": 0.2
            }
        self.check_stems(self.verbs)  # ensure all verbs are stemmed

        # Good nouns: rate how good a noun is between 1 and 2
        # (inclusive), 1 being neutral and 2 being the best possible.
        # Bad nouns: rate the noun like you would a good noun but
        # based on how bad it is, then multiply by -1.
        #    Examples:
        #        theif = 1.3 * -1
        #        murderer = 2 * -1
        #
        # Nouns must be stemmed in self.nouns to match their usage in
        # action because nouns are still stemmed. Keep in mind, though,
        # that they have already been tagged as nouns before they are
        # stemmed so there is no meaning lost when stemming.
        # i.e. No meaning lost from 'murderer' stemmed to 'murder'.
        self.nouns = {
                # bad
                "theif": -1.3,
                "crimin": -1.1,  # stem of criminal
                "robber": -1.3,
                "murder": -2,  # stem of murderer

                # good
                "babi": 1.6,  # stem of baby
                "peopl": 1.2,  # stem of people
                "children": 1.4,
                "dog": 1.1,
                "cat": 1.1
            }
        self.check_stems(self.nouns)  # ensure all nouns are stemmed
        return

    def stemmer(self, word: str, tag: str) -> str:
        """Return the stem of a word if it is a verb, otherwise return
        the unchanged word.
        
        Examples:
            teaching --> teach
            gave --> give

        NOTE: Verbs that are congugated irregularly in the past tense
              might need to be manually input into self.special_stems
        """
        stem = self.special_stems.get(word)
        if stem == None:
            stem = self.nltk_stemmer(word)
        return stem

    def check_stems(self, words: Iterable[str]) -> None:
        """Check that all words in an iterable of words are equal
        to their stems. If not, raise ValueError suggesting the stem
        to change the word to.
        """
        for word in words:
            if word != self.stemmer(word, "VB"):
                raise ValueError("incorrect stem, {} -> {}".format(word,
                                                    self.stemmer(word, "VB")))
        return

    def calc_score(self, processed_action: Iterable[str]) -> Union[int, float]:
        """Return the goodness score an action."""
        scores = []
        for word, tag in processed_action:
            if tag[0:2] == "VB":  # word tagged as verb
                # Default verb is nuetral, not affecting the total
                # score.
                weight = self.verbs.get(word, 0)
                scores.append(weight)
            elif tag[0:2] == "NN":  # word tagged as noun
                # Default noun will not change the goodness of the
                # verb before it.
                weight = self.nouns.get(word, 1)
                scores[-1] = round(scores[-1] * weight, 7)
        return round(sum(scores), 7)

    def process_action(self, action: str) -> Iterable[str]:
        action = word_tokenize(action)
        action = pos_tag(action)  # tag right away to keep context
        action = [t for t in action if t[0] not in self.stopwords]
        action = [(self.stemmer(*t), t[1]) for t in action]
        return action

    def sniff(self, action: str) -> Union[int, float]:
        action = self.process_action(action)
        score = self.calc_score(action)
        return score

    @staticmethod
    def interpret_goodness(score: Union[int, float]) -> str:
        """Return a qualitative determination of how good the action
        was based on the quantitative scoring of the action.
        """
        if score >= -1:
            goodness = "extremely naughty"
        elif score > -1 and score <= -0.7:
            goodness = "very naughty"
        elif score > -0.7 and score <= -0.3:
            goodness = "naughty"
        elif score > -0.3 and score < 0:
            goodness = "kinda naughty"
        elif score == 0:
            goodness = "neutral"
        elif score > 0 and score < 0.3:
            goodness = "kinda nice"
        elif score >= 0.3 and score < 0.7:
            goodness = "nice"
        elif score >= 0.7 and score < 1:
            goodness = "very nice"
        elif score >= 1:
            goodness = "extremely nice"
        return goodness


santa = GoodnessSniffer()

# print(g.sniff("teaching people to lie at the market"))
# print(g.sniff("lying to robbers at the market"))

print(santa.sniff(input("Please type an action:  ")))
