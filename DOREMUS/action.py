from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.channels.direct import CollectingOutputChannel
from domain_builder import get_action

import logging

from common import command_sanitizer
from common import out_context_set
from common import intent_index
from common import in_context_set
from domain_builder import get_entity
from domain_builder import entity_types

from datetime import datetime
import parsedatetime
from date_extractor import extract_dates

logger = logging.getLogger(__name__)
contain = intent_index()


# dictionary mapping intents
intents_to_actions=intent_index().get_intents_to_actions_dict()

# this dictionary is used to track active contexts to help influence predicted actions
active_conexts_to_influence_actions={}
active_contexts={}
entities=get_entity("dialogflow").entity_list
types_entities=entity_types().entity_to_types


def contexts_reset(action_name,tracker):
    events=[]
    contexts_in = in_context_set(action_name)
    contexts_out = out_context_set(action_name)
    if len(contexts_out)==0:
        contexts_out=[action_name]
    contexts_in.extend(contexts_out)
    contexts=contexts_in
    should_reset=1
    for context in contexts:
        if context not in active_contexts:
            active_contexts[context]=0

        elif active_contexts[context]>0:
            should_reset=0
            break

    if should_reset==1:
        for entity in entities:
            try:
                next(tracker.get_latest_entity_values(entity))
            except:
                # no entities for this entity found in the last massage    
                tracker._set_slot(entity, None)
                events.append(SlotSet(entity, None))

    for context in active_contexts:
        active_contexts[context]=0

    for context in contexts_out:
        active_contexts[context]=1
        
    return events  

def action_name_to_action_object(action_name):
    """
    This function will take an action name and converts it to Action('action_name') instance
    input:
     - action_name: string defining the name of the action
    output:
     - action_object_instance: Action('action_name') instance
    """

    constructor = globals()[action_name]
    action_object_instance = constructor()
    return action_object_instance

def use_contexts_to_predict_next_action(action_name,tracker):
    contexts_in = in_context_set(action_name)
    contexts_out = out_context_set(action_name)
    could_change_action=1
    for context in contexts_in:
        if context not in active_conexts_to_influence_actions:
            active_conexts_to_influence_actions[context]=0

        elif active_conexts_to_influence_actions[context]>0:
            could_change_action=0
            break
            
    if could_change_action:
        intent_ranking=tracker.latest_message.parse_data['intent_ranking']
        for intent in intent_ranking[1:2]:
            if intent['name'] not in intents_to_actions:
                continue
            potential_action_name = intents_to_actions[intent['name']]
            contexts_potential_action=in_context_set(potential_action_name)
            for context in contexts_potential_action:
                if context not in active_conexts_to_influence_actions:
                    active_conexts_to_influence_actions[context]=0

                elif active_conexts_to_influence_actions[context]>0:
                    tracker.trigger_follow_up_action(action_name_to_action_object(potential_action_name))
                    contexts_out = out_context_set(potential_action_name)
                    break
            

    for context in active_conexts_to_influence_actions:
        active_conexts_to_influence_actions[context]=0

    for context in contexts_out:
        active_conexts_to_influence_actions[context]=1
        


def transform_slots_to_standard(tracker):
    events=[]
    latest_entities=tracker.latest_message.entities
    entity_values=[]
    # if spacy detected datetime entities use those otherwise use the 
    # the entities extracted by ner_crf
    try:
        for entity in latest_entities:
            if entity['extractor']=="ner_spacy" and (entity['entity']=='DATE'
            or entity['entity']=='TIME'):
                entity_values.append(entity['value'])

        if len(entity_values)>0:
                    entity_value = " ".join(entity_values) 
                    tracker._set_slot("datetime", DATETIME_to_iso(entity_value))
                    events.append(SlotSet("datetime", DATETIME_to_iso(entity_value))) 
                    
                    return events
    except:
        # spacy didn't find any entities related to datetime 
        # so try to see if ner_crf extracted any entities related to
        # Datetime                   

        for entity in entities:
            if types_entities[entity]=="DATETIME":
                entity_values=[]
                for tmp in tracker.get_latest_entity_values(entity):
                    entity_values.append(tmp)

                if len(entity_values)>0:
                    entity_value = " ".join(entity_values)    
                    tracker._set_slot(entity, DATETIME_to_iso(entity_value))
                    events.append(SlotSet(entity, DATETIME_to_iso(entity_value)))

    return events     


def DATETIME_to_iso(datetime_string):
        formatted_dates=[]
        matches = extract_dates(datetime_string)
        for match in matches:
            if match==None:
                break
            formatted_dates.append(match.isoformat())

        if len(formatted_dates)==0:
            cal = parsedatetime.Calendar()
            formatted_dates=[]
            dates=datetime_string.split(" and ")
            if len(dates)==1:
                dates=dates[0]
                dates=dates.split(" to ")
            for date_string in dates:
                time_struct, parse_status = cal.parse(date_string)
                date=datetime(*time_struct[:6])
                formatted_dates.append(date.isoformat())
            
        return('/'.join(formatted_dates))
    
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events

class (Action):
    def name(self):
        return ''

    @staticmethod
    def required_fields():
        return [
                ]

    def run(self, dispatcher, tracker, domain):
        index = "hello"
        template = dispatcher.retrieve_template("utter_"+"")

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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

        # use contexts to influence predicted action
        use_contexts_to_predict_next_action(self.name(),tracker)

        # reset slots if necessary
        events=contexts_reset(self.name(),tracker)
        
        # standardize the slots
        events.extend(transform_slots_to_standard(tracker))
        
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
        contexts = out_context_set(self.name)
        for c in contexts:
            events.append(SlotSet(c,1))
        events.append(SlotSet("requested_slot", None))
        return events
