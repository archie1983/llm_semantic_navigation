import pickle
import os.path

from time import time

from ae_gemma_llm import GemmaLLMControl

class LLMRoomClassifier:
  def __init__(self):
    # read our labels from a pickle file
    self.labels_fname = "labels_shuffled.pkl"
    self.features_fname = "features_for_each_label.pkl"

    file = open(self.features_fname,'rb')
    self.features_for_each_label = pickle.load(file)
    file.close()

    file = open(self.labels_fname,'rb')
    self.labels_shuffled = pickle.load(file)
    file.close()

    self.room_types = {
        "living room" : 1,
        "kitchen" : 2,
        "bedroom" : 3,
        "bathroom" : 4
    }

    #print(self.labels_shuffled)

    self.data_counter = 0

    self.glc = GemmaLLMControl()

    #########################################################

  def predict(self, data_tuple):
    print("Prediction of: " + data_tuple[0] + " : " + result[0])

  def get_next_data_item(self):

      if (self.data_counter < len(self.labels_shuffled) -1):
          ret_tuple = (self.labels_shuffled[self.data_counter], self.features_for_each_label[self.data_counter])
          self.data_counter += 1
          return ret_tuple
      else:
          return ("", "")

  def process_data_items(self):
      for i in range(len(self.labels_shuffled)):
          (label, features) = rc.get_next_data_item()
          #if (i == 55):
          self.glc.construct_classifier_question(features)
          ans = self.glc.get_answer()
          print(str(i) + ") ANS: " + label + " " + str(ans) + " ## " + str(self.room_types.get(label)) + " # " + " @@ " + str(self.room_types.get(label) == ans))


rc = LLMRoomClassifier()
rc.process_data_items()

#print(rc.get_next_data_item())
#print(rc.get_next_data_item())
#print(rc.get_next_data_item())
#print(rc.get_next_data_item())

#rc.predict("SinkBasin CounterTop SoapBar ToiletPaperHanger")
#rc.predict("SinkBasin Chair Egg Toaster Microwave CounterTop DiningTable StoveKnob Lettuce SaltShaker")
#rc.predict("SinkBasin Chair Egg Toaster Microwave CounterTop DiningTable StoveKnob Lettuce")
#rc.predict("Egg")
##rc.predict("SinkBasin CounterTop SoapBar ToiletPaperHanger ToiletPaper SprayBottle Floor GarbageCan Candle Plunger ScrubBrush Toilet Sink HandTowelHolder Faucet Mirror Cloth Towel Drawer SoapBottle ShowerHead HandTowel LightSwitch ShowerDoor TowelHolder ShowerGlass")
##rc.predict("Candle Plunger ScrubBrush Toilet Sink HandTowelHolder SoapBottle")
#rc.predict("Candle Plunger ScrubBrush Toilet")
#rc.predict("TV Sofa")
#rc.predict("ScrubBrush ToiletCandle Plunger")