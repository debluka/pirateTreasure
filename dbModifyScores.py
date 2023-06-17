from collections import OrderedDict

from firebase_admin.db import Reference

from databaseInit import ref

highscoresRef: Reference = ref.child("highscores")


# Retrieve a dictionary of threescores where key is the name of the player and value is the player's highs-core
def getHighscores() -> dict[str: int]:
    print(OrderedDict(sorted({name: score for name, scores in highscoresRef.order_by_child("score").get().items() for _, score in
            scores.items()}.items(), key=lambda x:x[1], reverse=True)))
    return OrderedDict(sorted({name: score for name, scores in highscoresRef.order_by_child("score").get().items() for _, score in
            scores.items()}.items(), key=lambda x:x[1], reverse=True))


# Save a player's score
def saveScore(username: str, score: int) -> None:
    playRef: Reference = highscoresRef.child(username)
    playRef.set({"score": score})
