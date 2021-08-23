from hatesonar import Sonar

sonar = Sonar()

def isHateInside(txt):
    result = sonar.ping(txt)
    for a in result["classes"]:
        if a["class_name"] == "hate_speech":
            if a["confidence"] <= 0.0:
                return False
    return result["top_class"] == "hate_speech"


def get_hate_confidence(txt):
    result = sonar.ping(txt)
    for a in result["classes"]:
        if a["class_name"] == "hate_speech":
            return a["confidence"]

def label_hate(post):         # For the time being, this function is pretty simple. We will expand it later.
    if isHateInside(post.txt):
        post.label_hate_as(1)
    else:
        post.label_hate_as(0)
    return post
