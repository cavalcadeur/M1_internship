import json
import csv

class Post:

    def __init__(self):
        self.txt = ""
        self.isHateSpeech = -1        # Coded as -1: don't know 0: no 1: yes (depending on the hate detector we might have more info like hate_speech or hate_slur)
        self.topic = -1               # -1 if not decided yet
        self.complete_topic = []
        self.source = -1
        self.isHopeSpeech = -1
        self.realHate = -1
        self.stemmed_txt = []

    def get_data_from_csv(self,post,source="csv",head=["txt","hateSpeech","topic","hopeSpeech"]):
        self.source = source

        if source == "youtube":
            lookingFor = {"youtube":"text"}
            for i in range(len(head)):
                if head[i] == lookingFor[source]:
                    self.txt = post[i]

        elif source == "csv":
            post = list(post)
            self.txt = post[1]
            self.isHateSpeech = int(post[2])
            if post[3] == "random":
                self.topic = -1
            else:
                self.topic = int(post[3])
            self.isHopeSpeech = int(post[4])
            if len(post) >= 6:
                self.realHate = int(post[5])
                if len(post) >= 7:
                    self.complete_topic = self.str_to_topics(post[6])
                    if len(post) >= 8:
                        self.stemmed_txt = json.loads(post[7])
            else:
                self.realHate = -1

        else: # The post is a dictionnary
            for keyWord in ["message","description"]:
                if keyWord in post:
                    self.txt = post[keyWord]
                    break


    def label_hope_as(self,label):
        self.isHopeSpeech = label

    def label_hate_as(self,label):
        self.isHateSpeech = label

    def get_topic_from_model(self,topic_list):
        max_value = 0
        result = 0
        for index,score in topic_list:
            if score >= max_value:
                max_value = score
                result = index
        return result

    def label_topic_as(self,true_label):

        self.complete_topic = []
        for topic, score in true_label:
            self.complete_topic.append([topic,score])
        self.topic = self.get_topic_from_model(true_label)

    def is_hateful(self):
        return self.isHateSpeech == 1

    def is_hopeful(self):
        return self.isHopeSpeech == 0


    def topics_to_str(self,topics):
        result = []
        for t in topics:
            a = [str(t[0]),str(t[1])]
            result.append(a)
        return json.dumps(result)

    def str_to_topics(self,topics):
        topics = json.loads(topics)
        result = []
        for t in topics:
            result.append([int(t[0]),float(t[1])])
        return result

    def get_csv(self):
        return [self.txt,self.isHateSpeech,self.topic,self.isHopeSpeech,self.realHate,self.topics_to_str(self.complete_topic),json.dumps(self.stemmed_txt)]

    def __str__(self):             # This function needs to be completed to show more info about the post
        result = "text : " + self.txt
        result += " hate_speech : " + str(self.isHateSpeech)
        result += " hope_speech : " + str(1 - self.isHopeSpeech) # Hope speech is labeled 0 if true and 1 if false but it's inconsistent with hate_speech notation
        result += " topic : " + str(self.topic)
        return result


def open_csv(fileName):
    post_list = []
    with open(fileName, newline='') as my_file:
        reader = csv.reader(my_file, delimiter='\t',quotechar='|')
        first_line = True
        for row in reader:
            if first_line:
                first_line = False
            else:
                new_post = Post()
                new_post.get_data_from_csv(row)
                post_list.append(new_post)

    return post_list


def save_csv(posts,fileName):

    with open(fileName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id','text','isHate','topic','isHope','realHate','completeTopic','stemmedText'])
        for i in range(len(posts)):
            spamwriter.writerow([i] + posts[i].get_csv())
