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

    def get_answer(self):
        stream = ollama.chat(
            model='gemma:7b-instruct-q6_K',
            messages=[
                {"role": "system", "content": self.prompt_system},
                {"role": "user", "content": self.prompt_user},
                {"role": "assistant", "content": self.prompt_assistant},
                {"role": "user", "content": self.question}
            ],
            stream=True,
        )

        for chunk in stream:
          print(chunk['message']['content'], end='', flush=True)
