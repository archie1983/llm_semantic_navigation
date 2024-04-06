from enum import Enum

###
# We need a unified Enum for room types.
###
class RoomType(Enum):
    LIVING_ROOM = 1
    KITCHEN = 2
    BEDROOM = 3
    BATHROOM = 4
    NOT_KNOWN = 5

    @classmethod
    def parse_llm_response(self, text):
        ret_val = RoomType.NOT_KNOWN
        nearest_index = 1000000

        ##
        # Find the first occurence of any of the rooms. This may not be perfect, but probably will do for now
        ##
        if "LIVING ROOM" in text.upper() and nearest_index > text.upper().find("LIVING ROOM"):
            ret_val = RoomType.LIVING_ROOM
            nearest_index = text.upper().find("LIVING ROOM")
        if "KITCHEN" in text.upper() and nearest_index > text.upper().find("KITCHEN"):
            ret_val = RoomType.KITCHEN
            nearest_index = text.upper().find("KITCHEN")
        if "BEDROOM" in text.upper() and nearest_index > text.upper().find("BEDROOM"):
            ret_val = RoomType.BEDROOM
            nearest_index = text.upper().find("BEDROOM")
        if "BATHROOM" in text.upper() and nearest_index > text.upper().find("BATHROOM"):
            ret_val = RoomType.BATHROOM
            nearest_index = text.upper().find("BATHROOM")

        return ret_val

    @classmethod
    def interpret_label(self, text):
        ret_val = RoomType.NOT_KNOWN
        if "LIVING ROOM" in text.upper():
            ret_val = RoomType.LIVING_ROOM
        if "KITCHEN" in text.upper():
            ret_val = RoomType.KITCHEN
        if "BEDROOM" in text.upper():
            ret_val = RoomType.BEDROOM
        if "BATHROOM" in text.upper():
            ret_val = RoomType.BATHROOM

        return ret_val
