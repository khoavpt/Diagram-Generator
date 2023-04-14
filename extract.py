import spacy
import re
from spacy import displacy
from spacy.matcher import DependencyMatcher
from spacy.symbols import LOWER

from geometry_object.Intersection import Intersection
from geometry_object.BasicGeometryObject import BasicGeometryObject
from my_types import relation_types, geometry_types

nlp = spacy.load("vi_core_news_lg")

# Pattern for extracting geometric objects
patterns = [[{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": "<", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type2", "REL_OP": ">", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type2", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "intersect_name", "REL_OP": ">", "RIGHT_ATTRS" : {"LENGTH" : 1}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": "<", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name2", "RIGHT_ID" : "intersect_name", "REL_OP": "$++", "RIGHT_ATTRS" : { "LENGTH" : 1}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": "<", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name2", "RIGHT_ID" : "intersect_name", "REL_OP": "$++", "RIGHT_ATTRS" : {"LENGTH" : 1}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name1", "RIGHT_ID" : "name2", "REL_OP": "$++", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name2", "RIGHT_ID" : "intersect_name", "REL_OP": "$++", "RIGHT_ATTRS" : {"LENGTH" : 1}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": ">", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "geometric_type2", "REL_OP": "$++", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type2", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": "<", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type2", "REL_OP": ">", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type2", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],
                    
            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": ">", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name2", "REL_OP": "$++", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type1", "REL_OP": "<", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name1", "RIGHT_ID" : "geometric_type2", "REL_OP": "$++", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type2", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": "<", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "geometric_type2", "REL_OP": ">", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type2", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],
                    
            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "name1", "RIGHT_ID" : "name2", "REL_OP": "$++", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "relation_type", "RIGHT_ATTRS" : {"LOWER" : {"IN": relation_types}}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name1", "REL_OP": "<", "RIGHT_ATTRS" : {"TAG": "Np"}},
             {"LEFT_ID" : "relation_type", "RIGHT_ID" : "name2", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}],

            [{"RIGHT_ID" : "geometric_type1", "RIGHT_ATTRS" : {"LOWER" : {"IN": geometry_types}}},
             {"LEFT_ID" : "geometric_type1", "RIGHT_ID" : "name1", "REL_OP": ">", "RIGHT_ATTRS" : {"TAG": "Np"}}]]

# Add patterns to dependency matcher
dep_matcher = DependencyMatcher(nlp.vocab)
for i in range(len(patterns)):
    dep_matcher.add("pattern" + str(i), patterns=[patterns[i]])

def tokenization(text):
    """
    Take in a text as input and return two lists of sentences:
    introduces: Contain sentences that introduce a new geometric object.
    asserts: Contain sentences that assert conditions between different geometric objects.
    """
    # If text end with a dot, remove it
    if text[-1] == ".":
        text = text[:-1]

    # Assert sentences are detected after words like "thỏa mãn" or "sao cho"
    sentences = re.split('\. |, |thỏa mã|sao ch', text)
    introduces = []
    asserts = []
    for sentence in sentences:
        if sentence[0] in ["n", "o"]:
            asserts.append(sentence[2:])
        else:
            introduces.append(sentence)
    print(introduces, asserts)
    return introduces, asserts

def pre_process(sentence):
    """
    Accept a sentence as input and return a processed spacy doc object (fixed POS tagging of geometry objects) 
    """
    # Convert the first letter of the sentence to lowercase
    words = sentence.split(' ')
    sentence_lower = ""
    for word in words:
        if not word.isupper():
            sentence_lower += (word.lower() + " ")
        else:
            sentence_lower += (word + " ")
            
    doc = nlp(sentence_lower)
    for token in doc:
        # Convert the POS of geometry objects's name to Np (proper noun)
        if token.text.isupper() or token.tag_ == "Ny" or token.text in ["delta", "gamma", "omega", "beta", "d", "c"]:
            token.tag_ = "Np"
        
    return doc

def extract_informations_from_sentence(doc):
    """
    Accept a spacy doc object as input and return a list of geometric objects
    """
    visualize(doc)
    geometric_objects = []
    result = dep_matcher(doc)
    if result == []:
        return None
    pattern_id, matches_id = dep_matcher(doc)[0]
    pattern_name = nlp.vocab[pattern_id].text
    matches_text = [doc[match_id].text for match_id in matches_id]
    if pattern_name == "pattern0":
        geometric_objects.append(Intersection(matches_text[2], matches_text[4], matches_text[5]))
    elif pattern_name in "pattern1":
        geometric_objects.append(Intersection(matches_text[2], matches_text[3], matches_text[4]))
    elif pattern_name in ["pattern2", "pattern3"]:
        geometric_objects.append(Intersection(matches_text[1], matches_text[2], matches_text[3]))
    elif pattern_name in ["pattern4", "pattern5"]:
        geometric_objects.append(BasicGeometryObject(matches_text[1], matches_text[2], matches_text[0], matches_text[3], matches_text[4]))
    elif pattern_name in ["pattern6", "pattern7"]:
        geometric_objects.append(BasicGeometryObject(matches_text[1], matches_text[2], matches_text[0], "none", matches_text[3]))
    elif pattern_name == "pattern8":
        geometric_objects.append(BasicGeometryObject("none", matches_text[1], matches_text[0], matches_text[2], matches_text[3]))
    elif pattern_name == "pattern9":
        geometric_objects.append(BasicGeometryObject("none", matches_text[1], matches_text[0], matches_text[2], matches_text[3]))
    elif pattern_name in ["pattern10", "pattern11"]:
        geometric_objects.append(BasicGeometryObject("none", matches_text[1], matches_text[0], "none", matches_text[2]))
    elif pattern_name == "pattern12":
        geometric_objects.append(BasicGeometryObject(matches_text[0], matches_text[1], "none", "none", "none"))
    return geometric_objects


def visualize(doc):
    """
    Accept a spacy doc object as input and write a visualization of the dependency parse of doc to visual.html
    """
    html = displacy.render(doc, style="dep")
    with open("visual.html", "w", encoding="utf-8") as f:
        f.write(html)

def extract_informations_from_text(text):
    gmbl_commands = []
    object_summaries = []
    condition_summaries = []
    memories = []
    try:
        introduces, asserts = tokenization(text)
        for sentence in introduces:
            processed_sentece = pre_process(sentence)
            geometric_objects = extract_informations_from_sentence(doc=processed_sentece)
            for go in geometric_objects:
                go.printObject()
                if type(go) == BasicGeometryObject:
                    if go.geometry_type1 != "none" and go.name1 != "none":
                        memories.append((go.geometry_type1, go.name1))
                    go.process(memories)
                object_summaries.append(go.summaries())
                gmbl_commands.append(go.toGMBL())
        for sentence in asserts:
            processed_sentece = pre_process(sentence)
            geometric_conditions = extract_informations_from_sentence(doc=processed_sentece)
            for gc in geometric_conditions:
                gc.process(memories)
                condition_summaries.append(gc.summaries())
                gmbl_commands.append(gc.toGMBLassert())
                gc.printObject()
        return gmbl_commands, object_summaries, condition_summaries
    except Exception:
        return gmbl_commands, object_summaries, condition_summaries

    