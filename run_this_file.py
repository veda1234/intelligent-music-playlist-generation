import json
from get_features_from_model import run

with open("audio_test.json", "r") as f:
        load_dict = json.load(f)

cluster_ids = run(load_dict)
# print("These are the cluster ids : ",str(cluster_ids))
