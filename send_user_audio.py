import sys,json
from get_user_cluster_ids import get_user_audio_features


# with open("audio_test.json", "r") as f:
#         load_dict = json.load(f)

# Send your dictionary here
print_this = get_user_audio_features('audio_test.json')

