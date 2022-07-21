from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .helpers import modify_input_for_multiple_files
from .models import ConfrenceHall, ConfrenceHallImages, HallBookings
from .serializers import ConfrenceHallSerializer, HallBookingsSerializer, ImageSerializer
from django.db.models import Q , F
import datetime
from datetime import datetime

class HallList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes= [IsAuthenticated]
    def get(self, request, format=None):
        if request.user.rolename == 'AO':
            hallobj = ConfrenceHall.objects.all()
            serializer = ConfrenceHallSerializer(hallobj, many=True)
            all_images = ConfrenceHallImages.objects.all()
            serializer2 = ImageSerializer(all_images, many=True)
            data = {}
            data["a"]=serializer.data
            data["b"]=serializer2.data
            return Response(data , status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.rolename == 'AO':
            serializer = ConfrenceHallSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            hall = serializer.data["id"]
            images = dict((request.data).lists())['image']
            flag = 1
            for img_name in images:
                modified_data = modify_input_for_multiple_files(hall,
                                                                img_name)
                file_serializer = ImageSerializer(data=modified_data)
                if file_serializer.is_valid(raise_exception=True):
                    file_serializer.save()
                else:
                    flag = 0
            if flag == 1:
                return Response({"success":"Successfully created hall!!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You cannot add a hall!!"}, status=status.HTTP_403_FORBIDDEN)

class HallDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes= [IsAuthenticated]
    def get_object(self, pk):
        try:
            return ConfrenceHall.objects.get(pk=pk)
        except ConfrenceHall.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ConfrenceHallSerializer(snippet)
        imgobj = ConfrenceHallImages.objects.filter(hall = pk)
        imgserializer = ImageSerializer(imgobj,many = True)
        data = { "images": imgserializer.data, "data": serializer.data}
        return JsonResponse(data ,status=status.HTTP_200_OK,safe=False)

    def put(self, request, pk, format=None):
        if request.user.rolename == 'AO':
            snippet = self.get_object(pk)
            serializer = ConfrenceHallSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":"Successfully updated!!"} , status = status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"You don't have permission to access this request!"},status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        if request.user.rolename == 'AO':
            snippet = self.get_object(pk)
            snippet.delete()
            return Response({"success": "Deleted Successfully"} ,status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"You don't have permission to access this request!"},status=status.HTTP_403_FORBIDDEN)

class AvailabilityView(APIView):
    def get(self, request):
        permission_classes= [IsAuthenticated]
        start_inp = request.query_params['start']
        end_inp = request.query_params['end']
        occupancy_inp = request.query_params['occupancy']
        print(start_inp, end_inp , occupancy_inp)
        start_time = datetime.strptime(start_inp, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strptime(end_inp, "%Y-%m-%dT%H:%M:%S.%fZ")
        print(start_time.date)
        if (start_time < end_time) and int(occupancy_inp) > 0 and start_time >= datetime.now():
            availability_list = []
            booking_list = HallBookings.objects.filter(Q( Q(start__range = (start_inp, end_inp))  | Q (end__range = (start_inp, end_inp))  | Q(Q(start__lte  = start_inp) & Q(end__gte = end_inp))) & Q(response__AO = True) )
            for book in booking_list:
                if(book.hall.max_occupancy >= int(occupancy_inp)):
                    hall = { "id": book.hall.id, "name": book.hall.name}
                    availability_list.append(hall)
            availability_list = []
            booking_list = HallBookings.objects.filter(Q( Q(start__range = (start_inp, end_inp))  | Q (end__range = (start_inp, end_inp))  | Q(Q(start__lte  = start_inp) & Q(end__gte = end_inp))) & Q(response__AO = True) )
            hall_list = list(ConfrenceHall.objects.exclude(id__in = booking_list.values_list('hall', flat=True)).exclude(max_occupancy__lt=occupancy_inp).exclude(booking_limit__lt = ((end_time) - (start_time)).days).values('id','name'))
            return Response(hall_list, status = status.HTTP_200_OK)
        else:
            return Response({"error":"Input conditions are not satisfied!"} , status = status.HTTP_400_BAD_REQUEST)

class HallBookingView(APIView):
    permission_classes= [IsAuthenticated]
    
    def get(self, request, format=None):
        if request.user.rolename == "AO":
            bookingobj = HallBookings.objects.filter(Q( Q(response__HOD = True) | Q(response__HOD = False) )& Q(response__AO = None))
            serializer = HallBookingsSerializer(bookingobj, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
            
        if request.user.rolename == 'HOD':
            bookingobj = HallBookings.objects.filter(Q(response__HOD = None) & Q(response__AO = None))
            serializer = HallBookingsSerializer(bookingobj, many=True)
            return Response(serializer.data , status = status.HTTP_200_OK)
        
        elif request.user.rolename == "Employee":
            bookingobj = HallBookings.objects.filter(submittedBy = request.user)#.values().annotate(hall_name = F("hall__name")))   #
            serializer = HallBookingsSerializer(bookingobj, many=True )
            return Response(serializer.data , status = status.HTTP_200_OK)
        else:
            return Response('Invalid request!',status=status.HTTP_401_UNAUTHORIZED)

    
    def post(self, request, format=None):
        if request.user.rolename == "Employee":
            request.data["submittedBy"] = request.user.id
            request.data["remarks"] = { "AO":None, "HOD": None , "Employee": (request.data).pop("remarks") } 
            serializer = HallBookingsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": "Successfully booked the hall!!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": "You cannot fill this form!!"}, status=status.HTTP_403_FORBIDDEN)    
    
class HallBookingorUpdating(APIView):
    permission_classes= [IsAuthenticated]
    def get_object(self, pk):
        try:
            return HallBookings.objects.get(pk=pk)
        except HallBookings.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = HallBookingsSerializer(snippet)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.rolename == "AO":
                for i in [ "start","end", "participantcount","purpose","submittedBy"]:request.data.pop(i,None)
                snippet = self.get_object(pk)
                if request.data == {}:
                    return Response({"messgage": "Cannot pass empty update request!"} , status =status.HTTP_400_BAD_REQUEST)
                snippet.response["AO"] = request.data["response"]
                snippet.remarks["AO"] = request.data["remarks"]
                snippet.isEditable["AO"] = True
                snippet.responseTime["AO"] = str(datetime.now())
                snippet.save()
                return Response({"success":"Successfully updated!!"} , status = status.HTTP_202_ACCEPTED)            
            
            elif request.user.rolename == "HOD":
                for i in [  "start","end", "participantcount","hall","purpose","submittedBy"]:request.data.pop(i,None)
                snippet = self.get_object(pk)
                if request.data == {}:
                    return Response({"messgage": "Cannot pass empty update request!"} , status =status.HTTP_400_BAD_REQUEST)
                snippet.response["HOD"] = request.data["response"]
                snippet.remarks["HOD"] = request.data["remarks"]
                snippet.isEditable["HOD"] = True
                snippet.responseTime["HOD"] = str(datetime.now())
                snippet.save()
                return Response({"success":"Successfully updated!!"} , status = status.HTTP_202_ACCEPTED)
            else:
                return Response("You do not have permission to access this page!!" , status=status.HTTP_403_FORBIDDEN)
