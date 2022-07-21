from rest_framework import serializers
from .models import ConfrenceHall , ConfrenceHallImages , HallBookings

class ConfrenceHallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ConfrenceHall
        exclude = ['isactive',]
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfrenceHallImages
        fields = (
            'hall',
            'image'
        )

class HallBookingsSerializer(serializers.ModelSerializer):
    hall_name = serializers.SerializerMethodField()
    
    def get_hall_name(self,object):
        return object.hall.name
        
    class Meta:
        model = HallBookings
        fields = "__all__"