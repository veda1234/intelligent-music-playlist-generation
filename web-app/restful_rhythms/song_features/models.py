from common_utils import FirestoreModel
import traceback

class TrackFeaturesClass(FirestoreModel):
    def __init__(self):
        super(TrackFeaturesClass, self).__init__('track_features', keyField='audio_features.id')
    
    def get_track_features(self, track_id):
        try:
            tracks = super().get_item(track_id)
            return tracks
        except:
            print(f"some error occured in fetching song features {track_id}")
            traceback.print_exc()
            raise

TrackFeatures = TrackFeaturesClass()