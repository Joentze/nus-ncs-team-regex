import spacy
from spacy.training import Example   # Add this line
from spacy.tokens import Span
import random
import pandas as pd

roads = pd.read_csv("road_network.csv")
road_names = list(roads["road"])

# Simplified training data generation
def generate_training_data(roads, batch_size=1000, num_batches=5):
    templates = [
        "Is traffic expected to be [TRAFFIC_WORD] near [LOCATION] during the [EVENT]?", 
        "Will there be any [ISSUE] around [LOCATION] for the [EVENT]?",
        "What's the best route to [LOCATION] for the [EVENT], considering potential [TRAFFIC_WORD] traffic?", 
        "Are there any traffic advisories I should know about before heading to the [EVENT] at [LOCATION]?",
        "Should I arrive at [LOCATION] early due to anticipated traffic for the [EVENT]?",
        "How long will traffic delays last around [LOCATION] after the end of the [EVENT]?",
        "How will the [EVENT] at [LOCATION] impact traffic on surrounding roads?",
        "Will traffic be [TRAFFIC_WORD] around [LOCATION] due to the [EVENT]?",
    ]

    traffic_words = ["heavy", "congested", "slow", "backed up", "fast", "smooth"]

    traffic_issues = ["road closures", "detours", "traffic diversions", "congestion", "accidents", "lane closures", "traffic jams", "road construction", "vehicle breakdowns", "traffic accidents", "pedestrian crossings", "traffic signal malfunctions", "flooding"]

    events = ["Taylor Swift concert", "Formula 1 Grand Prix", "National Day Parade", "Singapore International Film Festival", "Singapore Food Festival", "Singapore Art Week", "Fashion Week", "Singapore International Festival of Arts", "Writers Festival", "Singapore Night Festival", "International Festival of Music", "Singapore International Photography Festival", "Singapore Design Week", "Good Friday", "Public Holiday"]

    data = []
    for _ in range(num_batches):
        batch_roads = random.sample(roads, batch_size)
        for road in batch_roads: 
            template = random.choice(templates)
            template = template.replace("[TRAFFIC_WORD]", random.choice(traffic_words))
            template = template.replace("[ISSUE]", random.choice(traffic_issues))
            template = template.replace("[EVENT]", random.choice(events))
            sentence = template.replace("[LOCATION]", road)
            road_start_idx = sentence.find(road)
            road_end_idx = road_start_idx + len(road)
            entities = [(road_start_idx, road_end_idx, "SG_ROAD")]  # Update start index
            data.append((sentence, {"entities": entities}))
    return data

# Training Setup
nlp = spacy.load("en_core_web_sm") 
# nlp.add_pipe("ner", last=True)
nlp.get_pipe("ner").add_label("SG_ROAD") 
optimizer = nlp.create_optimizer()  

# Training Loop
train_data = generate_training_data(road_names)
print(train_data)
for itn in range(20):  # Adjust iterations
    random.shuffle(train_data) 
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.2, sgd=optimizer)

# Save Model
nlp.to_disk("./NEP2/") 