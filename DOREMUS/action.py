from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.channels.direct import CollectingOutputChannel

import logging

from common import command_sanitizer
from common import out_context_set
from common import intent_index


logger = logging.getLogger(__name__)
contain = intent_index()



class input_unknown(Action):
    def name(self):
        return 'input_unknown'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "Default_Fallback_Intent"
        template = dispatcher.retrieve_template("utter_"+"input_unknown")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class input_welcome(Action):
    def name(self):
        return 'input_welcome'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "Default_Welcome_Intent"
        template = dispatcher.retrieve_template("utter_"+"input_welcome")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class discover_artist(Action):
    def name(self):
        return 'discover_artist'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "discover_artist"
        template = dispatcher.retrieve_template("utter_"+"discover_artist")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class find_artist(Action):
    def name(self):
        return 'find_artist'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "find_artist"
        template = dispatcher.retrieve_template("utter_"+"find_artist")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class find_performance(Action):
    def name(self):
        return 'find_performance'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "find_performance"
        template = dispatcher.retrieve_template("utter_"+"find_performance")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events



class help(Action):
    def name(self):
        return 'help'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "help"
        template = dispatcher.retrieve_template("utter_"+"help")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class reset(Action):
    def name(self):
        return 'reset'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "reset"
        template = dispatcher.retrieve_template("utter_"+"reset")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_works_by_no(Action):
    def name(self):
        return 'works_by_works_by_no'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by___no"
        template = dispatcher.retrieve_template("utter_"+"works_by_works_by_no")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_works_by_yes(Action):
    def name(self):
        return 'works_by_works_by_yes'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by___yes"
        template = dispatcher.retrieve_template("utter_"+"works_by_works_by_yes")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_artist(Action):
    def name(self):
        return 'works_by_artist'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by_artist"
        template = dispatcher.retrieve_template("utter_"+"works_by_artist")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_genre(Action):
    def name(self):
        return 'works_by_genre'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by_genre"
        template = dispatcher.retrieve_template("utter_"+"works_by_genre")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_instrument(Action):
    def name(self):
        return 'works_by_instrument'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by_instrument"
        template = dispatcher.retrieve_template("utter_"+"works_by_instrument")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by_years(Action):
    def name(self):
        return 'works_by_years'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by_years"
        template = dispatcher.retrieve_template("utter_"+"works_by_years")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class works_by(Action):
    def name(self):
        return 'works_by'

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "works_by"
        template = dispatcher.retrieve_template("utter_"+"works_by")

        # Checking required parameters
        intent = contain.index[index]
        for entity in intent.entities:
            if entity.required == True:
                slot = entity.name
                if slot!= None:
                    slot_val = tracker.get_slot(slot)
                    if slot_val is None:
                        logger.info("Uttering the required parameter")
                        dispatcher.utter_template(command_sanitizer("utter_{}_follow_up_{}".format(self.name(),slot)))
                        events = []
                        events.append(SlotSet("requested_slot", slot))
                        return events
                        
        text = template["text"]
        modified_text = ""
        i=0
        while i < (len(text)):
            if text[i]=='{':
                j = i+1
                slot = ""
                while(text[j]!='}' and j<len(text)):
                    slot += text[j]
                    j += 1
                modified_text += tracker.get_slot(slot)
                i = j
            else:
                modified_text += text[i]
            i += 1
        dispatcher.utter_message(modified_text)
        events = []
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events
