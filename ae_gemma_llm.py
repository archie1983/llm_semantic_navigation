import ollama

class GemmaLLMControl:
    def initialise(self):
        self.prompt_system = """
        You are a robot exploring an environment for the first time .
        You will be given an object to look for and should provide
        guidance of where to explore based on a series of
        observations . Observations will be given as a list of
        object clusters numbered 1 to N .

        Your job is to provide guidance about where we should explore
        next . For example if we are in a house and looking for a tv
        we should explore areas that typically have tv ’ s such as
        bedrooms and living rooms .

        You should always provide reasoning along with a number
        identifying where we should explore . If there are multiple
        right answers you should separate them with commas . Always
        include Reasoning : < your reasoning > and Answer : < your
        answer ( s ) >. If there are no suitable answers leave the
        space afters Answer : blank .
        """

        self.prompt_user = """
        I observe the following clusters of objects while exploring a
        house :
        1. sofa , tv , speaker
        2. desk , chair , computer
        3. sink , microwave , refrigerator

        Where should I search next if I am looking for a knife
        """

        self.prompt_assistant = """
        Reasoning : Knifes are typically kept in the kitchen and a sink ,
        microwave , and refrigerator are commonly found in kitchens
        . Therefore we should check the cluster that is likely to
        be a kitchen first .
        Answer : 3

        Other considerations

        1. Disregard the frequency of the objects listed on each line .
        If there are multiple of the same item in a cluster it
        will only be listed once in that cluster .
        2. You will only be given a list of common items found in the
        environment . You will not be given room labels . Use your
        best judgement when determining what room a cluster of
        objects is likely to belong to .
        """

        self.question = """
        I observe the following clusters of objects while exploring a house:
        1. couch
        2. wooden chair
        3. refrigerator

        Where should I search next if I am looking for a gas stove?

        You should always provide justification
        """

    def initialise_for_ai2_thor_room_classification(self):
        self.prompt_system = """
        You are a robot exploring a room for the first time .
        You will be given a list of objects that you can see in the room
        and should provide a guess of what kind of room it is . Objects
        will be given as a list separated by a comma .

        Your job is to make a guess of what room type these objects belong to .
        You will only have 4 room types to choose from: Living room , Kitchen ,
        Bedroom , Bathroom . For example if you are in a room and observing the
        following objects: Bath , Towel , Toiler Paper , Toothbrush then you
        should guess that you are in a Bathroom because you would typically
        find these objects in a Bathroom . Coverseley if you observe:
        Arm chair , TV , Couch then your guess should be a Living Room because
        you would typically find these objects in a Living Room.

        You should always provide reasoning along with a number
        identifying the guessed room . If there are multiple
        right answers you should separate them with commas . Always
        include Reasoning : < your reasoning > and Answer : < your
        answer ( s ) >. If there are no suitable answers leave the
        space afters Answer : blank .
        """

        self.prompt_user = """
        You observe the following objects while exploring a room:
        sink , microwave , refrigerator , waste bin

        What kind of room are you in

        1. Living room
        2. Kitchen
        3. Bedroom
        4. Bathroom
        """

        self.prompt_assistant = """
        Reasoning : Waste bin is typically kept in the kitchen and a sink ,
        microwave , and refrigerator are commonly found in kitchens
        . Therefore I would guess that I am in the kitchen .
        Answer : 2

        Other considerations

        1. Disregard the frequency of the objects listed on each line .
        If there are multiple of the same object in the list
        treat it as if mentioned only once .
        2. You will only be given a list of common items found in the
        environment . Use your best judgement when determining what room
        objects likely belong to .
        """

        self.question = """
        I observe the following objects while exploring a room:
        Candle, Plunger, Scrub Brush, Toilet

        What kind of room is this?

        1. Living room
        2. Kitchen
        3. Bedroom
        4. Bathroom

        You should always provide justification
        """

    def construct_classifier_question(self, query_words):
        template = """
        I observe the following objects while exploring a room:
        {0}

        What kind of room is this?

        1. Living room
        2. Kitchen
        3. Bedroom
        4. Bathroom

        You should always provide justification
        """

        self.question = template.format(query_words)

        return self.question

    def get_answer(self):
        stream = ollama.chat(
            model='gemma:7b-instruct-q6_K',
            messages=[
                {"role": "user", "content": self.question}
            ],
            stream=True,
        )

        full_answer = ""
        cur_chunk = ""
        ret_answer = -1

        for chunk in stream:
          cur_chunk = chunk['message']['content']
          full_answer += cur_chunk
          print(cur_chunk, end='', flush=True)

        full_answer = full_answer.replace(".", "")
        ndx = full_answer.index("**Answer:**")

        if (ndx >= 0 and len(full_answer) > ndx + 15):
            #ret_answer = full_answer[ndx + 12]
            nums = [int(s) for s in full_answer[ndx:(ndx + 20)].split() if s.isdigit()]
            ret_answer = nums[0]

        #print("NDX: " + str(ndx) + " : " + str(len(full_answer)) + " : " + full_answer[ndx + 12] + " ## " + ret_answer)
        return ret_answer