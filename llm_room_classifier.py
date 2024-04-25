import pickle
import os.path

from time import time

from ae_llm import LLMControl, LLMType
from room_type import RoomType

##
# A class that is sort of a middle man between the LLM that we will use for
# classifying rooms and the data that is being provided.
##
class LLMRoomClassifier:
  def __init__(self):
    self.data_counter = 0
    self.false_cnt = 0
    self.true_cnt = 0

    self.stored_labels_loaded = False

    self.glc = LLMControl(LLMType.MISTRAL_4b)

  def __init__(self, llm_type):
    self.data_counter = 0
    self.false_cnt = 0
    self.true_cnt = 0

    self.stored_labels_loaded = False

    self.glc = LLMControl(llm_type)

    #########################################################

  def load_stored_data(self):
    if (not self.stored_labels_loaded):
        self.stored_labels_loaded = True
        # read our labels from a pickle file
        self.labels_fname = "pkl/labels_shuffled.pkl"
        self.features_fname = "pkl/features_for_each_label.pkl"

        file = open(self.features_fname,'rb')
        self.features_for_each_label = pickle.load(file)
        file.close()

        file = open(self.labels_fname,'rb')
        self.labels_shuffled = pickle.load(file)
        file.close()

    #print(self.labels_shuffled[119] + " @@@@ " + self.features_for_each_label[119])

  def get_next_data_item(self):
      self.load_stored_data()
      if (self.data_counter < len(self.labels_shuffled)):
          ret_tuple = (self.labels_shuffled[self.data_counter], self.features_for_each_label[self.data_counter])
          self.data_counter += 1
          return ret_tuple
      else:
          return ("", "")

  def classify_room_by_this_object_set(self, obj_set):
      # now we'll get the objects into a string separated by a space
      objs_in_room_as_string = ""
      for obj in obj_set:
          objs_in_room_as_string += obj + ", "

      objs_in_room_as_string = objs_in_room_as_string[:-2]

      self.glc.construct_classifier_question(objs_in_room_as_string)

      #t0 = time()
      ans = self.glc.get_answer()
      #print("llm predict time:", round(time()-t0, 3), "s")

      #print("\n" + str(ans) + " :: " + list(self.room_types.keys())[list(self.room_types.values()).index(ans)])
      #print("\n" + ans.name + " :: " + str(ans.value))

      return ans

  ##
  # Allows us asking the LLM where to find a given object
  ##
  def where_to_find_this(self, object_name):
      self.glc.construct_room_selector_question(object_name)
      ans = self.glc.get_answer()

      return ans

  def where_to_look_first(self, what_to_look_for, where_to_look):
      objs_to_look_near = ""
      for obj in where_to_look:
          objs_to_look_near += obj + ", "
      
      objs_to_look_near = objs_to_look_near[:-2]

      self.glc.construct_object_selector_question(what_to_look_for, objs_to_look_near)
      ans = self.glc.get_object_selector_answer(where_to_look)

      print("ANS: " + ans)
      return ans

  def test_classification_on_stored_data(self):
      self.load_stored_data()
      for i in range(len(self.labels_shuffled)):
          (label, features) = rc.get_next_data_item()
          #if (i >= 118):
          print(label + " :: " + features)
          self.glc.construct_classifier_question(features)
          ans = self.glc.get_answer()
          #print("\n" + str(i) + ") ANS: " + label + " " + str(ans) + " ## " + str(self.room_types.get(label)) + " # " + " @@ " + str(self.room_types.get(label) == ans))
          print("\n" + str(i) + ") ANS: " + label + " " + ans.name + " ## " + str(ans.value) + " # " + " @@ " + str(RoomType.interpret_label(label) == ans))

          if (RoomType.interpret_label(label) == ans):
              self.true_cnt += 1
          else:
              self.alse_cnt += 1

      print("TRUE CNT: " + str(self.true_cnt) + " :: False CNT: " + str(self.false_cnt))


if __name__ == "__main__":
    rc = LLMRoomClassifier()
    rc.test_classification_on_stored_data()

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
