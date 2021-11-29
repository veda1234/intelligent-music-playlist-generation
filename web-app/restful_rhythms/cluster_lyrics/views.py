from rest_framework import viewsets
from rest_framework.response import Response
import traceback
import sys
from spotify.util import is_spotify_authenticated
from rest_framework import status

NUM_CLUSTERS = 7
emotion_labels = {
  "sadness": 4,
  "joy": 2,
  "anger": 0,
  "fear": 1,
  "love": 3,
  "surprise": 5
}

class EmotionView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({ "emotions": list(emotion_labels.keys()) })
        except:
            print("some error occured while fetching emotions")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)

class ClusterView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({ 
                "clusters" : { f"Cluster {i}" : i for i in list(range(NUM_CLUSTERS)) } 
            })
        except:
            print("some error occured while fetching emotions")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)


        