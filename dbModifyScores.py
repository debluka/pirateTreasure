from databaseInit import ref

highscoresRef = ref.child("highscores")


# retrieve a dictionary of threescores where key is the name of the player and value is the player's highs-core
def getHighscores():
    return {name: score for name, scores in highscoresRef.order_by_child("score").get().items() for _, score in
            scores.items()}


# save a player's score
def saveScore(username, score):
    playRef = highscoresRef.child(username)
    playRef.set({"score": score})
