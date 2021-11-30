import pickle, os, json


def run(data):
    # args ='spark-submit send_user_audio.py ' + data

    # with open('audio_test.json', 'w') as f:
    #     json.dump(data, f)

    os.system("spark-submit send_user_audio.py")
    # subprocess.Popen(["spark-submit", "send_user_audio.py"] + data)

    # with open('user_cluster_ids.pkl', 'rb') as f:
    #         data = pickle.load(f)

    return data
