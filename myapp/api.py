from rest_framework import generics
from rest_framework import mixins
from django.db.models import Q
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import *
from .serializers import *
from .api_exceptions import *
from .tasks import *

# I wrote this code -------------------------- Start
class UserPoint(mixins.RetrieveModelMixin, generics.GenericAPIView):
    '''UserPoint
    An API endpoint. Handling 'user' record, returns all data that is publically accessible.

    Accepts: 'GET'
    'api/user/' -> Without query, returns the user record associated with the logged in user
    'api/user/?user_id={PK}' -> With query, returns the user record associated with the query PK

    returns: user record, or throws error
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        try:
            user_id_query = self.request.GET.get('user_id', None)
            # If the query doesnt include a query string
            if user_id_query:
                # Get the user of the query
                response_object = self.queryset.get(id=user_id_query)
            else:
                # Get the user logged in
                response_object = self.queryset.get(id=self.request.user.id)
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("User doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class UserSearchPoint(mixins.ListModelMixin, generics.GenericAPIView):
    '''UserSearchPoint
    An API endpoint. Handling searching of the database, searches via username, first_name and last_name. Performs part string searches

    Accepts: 'GET'
    'api/user_search/?search={string}' -> Returns records that part match the search query string

    returns: list of user records, or throws error
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = self.queryset.filter(Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        else:
            raise BadRequestException("No 'search' query present")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserConnectionJunctionPoint(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView,):
    '''UserConnectionJunctionPoint
    An API endpoint. Handling user connections, creating and deleting of user connections

    Accepts: 'GET'
    'api/user_connection_junction/?user_connection_id={PK}' -> Returns a user_connection_junction record that has the user_connection PK and is associated with the logged in user
    returns: user_connection_junction record, or throws error

    Accepts: 'DELETE'
    'api/user_connection_junction/?user_connection_id={PK}' -> Deletes a user_connection_junction record for the logged in user where the user_connection has PK
    returns: nothing or error
    
    Accepts: 'POST'
    'api/user_connection_junction/' -> Creates a user_connection_junction record
    data : {
        user_connection: <PK>
    }
    returns 201 or error
    '''
    queryset = UserConnectionJunctions.objects.all()
    serializer_class = UserConnectionJunctionSerializer

    def get_object(self):
        try:
            user_connection_id_query = self.request.GET.get('user_connection_id', None)
            user_connection_junction_id_query = self.request.GET.get('user_connection_junction_id', None)
            if user_connection_id_query:
                response_object = self.queryset.get(user=self.request.user.id, user_connection=user_connection_id_query)
            elif user_connection_junction_id_query:
                response_object = self.queryset.get(id = user_connection_junction_id_query)
            else:
                raise BadRequestException("No 'user_connection_id' query present")
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("User connection doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # We overwrite to include the logged in user
        serializer = UserConnectionJunctionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise BadRequestException("Serializer is invalid")
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserConnectionJunctionsPoint_ApprovedRecords(mixins.ListModelMixin, generics.GenericAPIView):
    '''UserConnectionJunctionsPoint_ApprovedRecords
    An API endpoint. Handling user connections, returning all a user connections that are approved, and there exist a return connection

    Accepts: 'GET'
    'api/user_connection_junctions_approved/' -> Returns all user_connection_junction records

    returns: user_connection_junction records, or throws error
    '''
    queryset = UserConnectionJunctions.objects.all()
    serializer_class = UserConnectionJunctionsSerializer   
    
    def get_queryset(self):
        queryset = self.queryset.filter(
            Q(user=self.request.user) | 
            Q(user_connection=self.request.user) 
        )
        return queryset

    def get(self, request, *args, **kwargs):
        # Applying additional filters
        queryset = self.get_queryset()
        pks_to_keep = []
        for index_1 in range(len(queryset)):
            for index_2 in range(len(queryset)):
                if queryset[index_1].user == queryset[index_2].user_connection:
                    if queryset[index_1].user_connection == queryset[index_2].user:
                        if queryset[index_1].id not in pks_to_keep:
                            pks_to_keep.append(queryset[index_1].id)
                            
        self.queryset = UserConnectionJunctions.objects.filter(pk__in=pks_to_keep)

        return self.list(request, *args, **kwargs)

class UserConnectionJunctionsPoint_PendingRecords(mixins.ListModelMixin, generics.GenericAPIView):
    '''UserConnectionJunctionsPoint_PendingRecords
    An API endpoint. Handling user connections, returning all a user connections that are pending, Where the user is a connection though doesnt have a return connection

    Accepts: 'GET'
    'api/user_connection_junctions_pending/' -> Returns all user_connection_junction records

    returns: user_connection_junction records, or throws error
    '''
    queryset = UserConnectionJunctions.objects.all()
    serializer_class = UserConnectionJunctionsSerializer   
    
    def get_queryset(self):
        queryset = self.queryset.filter(
            Q(user=self.request.user) | 
            Q(user_connection=self.request.user) 
        )
        return queryset

    def get(self, request, *args, **kwargs):
        # Applying additional filters
        queryset = self.get_queryset()
        pks_to_keep = []
        for index_1 in range(len(queryset)):
            if queryset[index_1].user_connection == self.request.user:
                connected = False
                for index_2 in range(len(queryset)):
                    if queryset[index_2].user_connection == queryset[index_1].user:
                        connected = True
                if not connected and queryset[index_1].user not in pks_to_keep:
                    pks_to_keep.append(queryset[index_1].id)
                            
        self.queryset = UserConnectionJunctions.objects.filter(pk__in=pks_to_keep)
        return self.list(request, *args, **kwargs)

class UserConnectionJunctionsPoint_UserRecords(mixins.ListModelMixin, generics.GenericAPIView):
    '''UserConnectionJunctionsPoint_UserRecords
    An API endpoint. Handling user connections, returning all a user connections that the user is a user of the connection

    Accepts: 'GET'
    'api/user_connection_junctions_user/' -> Returns all user_connection_junction records

    returns: user_connection_junction records, or throws error
    '''
    queryset = UserConnectionJunctions.objects.all()
    serializer_class = UserConnectionJunctionsSerializer   
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
# class UserConnectionJunctionsPoint_ConnectionRecords(mixins.ListModelMixin, generics.GenericAPIView):
#     '''UserConnectionJunctionsPoint_ConnectionRecords
#     An API endpoint. Handling user connections, returning all a user connections that the user is a user_connection of the connection

#     Accepts: 'GET'
#     'api/user_connection_junctions_connection/' -> Returns all user_connection_junction records

#     returns: user_connection_junction records, or throws error
#     '''
#     queryset = UserConnectionJunctions.objects.all()
#     serializer_class = UserConnectionJunctionsSerializer   
    
#     def get_queryset(self):
#         return self.queryset.filter(user_connection=self.request.user)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

class UserGalleryPoint(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView,):
    '''UserGalleryPoint
    An API endpoint. Handling user_gallery, creating and deleting of user_gallery

    Accepts: 'GET'
    'api/user_gallery/?gallery_image_id={PK}' -> Returns a gallery_image record that has the gallery_image PK and is associated with the logged in user
    returns: gallery_image record, or throws error

    Accepts: 'DELETE'
    'api/user_gallery/?gallery_image_id={PK}' -> Deletes a gallery_image record for the logged in user where the gallery_image has PK and is associated with the logged in user
    returns: nothing or error
    
    Accepts: 'POST'
    'api/user_gallery/' -> Creates a gallery_image record
    data : {
        gallery_image: <Image File>
    }
    returns 201 or error
    '''
    queryset = UserGalleries.objects.all()
    serializer_class = UserGallerySerializer

    def get_object(self):
        try:
            gallery_image_id_query = self.request.GET.get('gallery_image_id', None)
            if gallery_image_id_query:
                response_object = self.queryset.get(user=self.request.user.id, id=gallery_image_id_query)
            else:
                raise BadRequestException("No 'gallery_image_id' query present")
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("Gallery image doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # We overwrite to include the logged in user
        serializer = UserGallerySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            record = serializer.save()
            # Creates a thumbnail of the image
            make_gallery_thumbnail.delay(record.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise BadRequestException("Serializer is invalid")
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserStatusPoint(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView,):
    '''UserStatusPoint
    An API endpoint. Handling user_statuses, creating and deleting of user_status

    Accepts: 'GET'
    'api/user_status/?status_id={PK}' -> Returns a user_status record that has the user_status PK and is associated with the logged in user
    returns: user_status record, or throws error

    Accepts: 'DELETE'
    'api/user_status/?status_id={PK}' -> Deletes a user_status record for the logged in user where the user_status has PK 
    returns: nothing or error
    
    Accepts: 'POST'
    'api/user_status/' -> Creates a user_status record
    data : {
        status: <string>
    }
    returns 201 or error
    '''
    queryset = UserStatuses.objects.all()
    serializer_class = UserStatusesSerializer

    def get_object(self):
        try:
            status_id_query = self.request.GET.get('status_id', None)
            if status_id_query:
                response_object = self.queryset.get(user=self.request.user.id, id=status_id_query)
            else:
                raise BadRequestException("No 'status_id' query present")
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("Status doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # We overwrite to include the logged in user
        serializer = UserStatusesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise BadRequestException("Serializer is invalid")
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ThreadPoint(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView,):
    '''ThreadPoint
    An API endpoint. Handling thread, creating and deleting of thread

    Accepts: 'GET'
    'api/thread/?thread_id={PK}' -> Returns a thread record that has the thread PK and is associated with the logged in user
    returns: thread record, or throws error

    Accepts: 'DELETE'
    'api/thread/?thread_id={PK}' -> Deletes a thread record for the logged in user where the thread has PK 
    returns: nothing or error
    
    Accepts: 'POST'
    'api/thread/' -> Creates a thread record
    data : {
        title: <string>
    }
    returns 201 or error
    '''
    queryset = Threads.objects.all()
    serializer_class = ThreadSerializer

    def get_object(self):
        try:
            thread_id_query = self.request.GET.get('thread_id', None)
            if thread_id_query:
                response_object = self.queryset.get(creating_user=self.request.user.id, id=thread_id_query)
            else:
                raise BadRequestException("No 'thread_id' query present")
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("Thread doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # We overwrite to include the logged in user
        serializer = ThreadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise BadRequestException("Serializer is invalid")
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ThreadsPoint(mixins.ListModelMixin, generics.GenericAPIView):
    '''ThreadsPoint
    An API endpoint. Handling threads, returning all threads a user has created

    Accepts: 'GET'
    'api/threads/' -> Returns a thread records that is associated with the logged in user
    returns: list of thread records, or throws error
    '''
    queryset = Threads.objects.all()
    serializer_class = ThreadsSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class UserThreadJunctionPoint(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              generics.GenericAPIView,):
    '''UserThreadJunctionPoint
    An API endpoint. Handling user_thread_junction, creating and deleting of user_thread_junction

    Accepts: 'GET'
    'api/user_thread_junction/?user_thread_junction_id={PK}' -> Returns a user_thread_junction record that has the user_thread_junction PK and is associated with the logged in user
    returns: user_thread_junction record, or throws error

    Accepts: 'DELETE'
    'api/user_thread_junction/?user_thread_junction_id={PK}' -> Deletes a user_thread_junction record for the logged in user where the user_thread_junction has PK 
    returns: nothing or error
    
    Accepts: 'POST'
    'api/user_thread_junction/' -> Creates a user_thread_junction record, Must come from the thread creator
    data : {
        thread: <PK>
        user: <PK>
    }
    returns 201 or error
    '''
    queryset = UserThreadJunctions.objects.all()
    serializer_class = UserThreadJunctionSerializer

    def get_object(self):
        try:
            user_thread_junction_id_query = self.request.GET.get('user_thread_junction_id', None)
            if user_thread_junction_id_query:
                response_object = self.queryset.get(user=self.request.user.id, id=user_thread_junction_id_query)
            else:
                raise BadRequestException("No 'user_thread_junction_id' query present")
            return response_object
        except ObjectDoesNotExist:
            raise NotFoundException("Thread doesn't exist") 

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Here we just checking logged in user is the creator of the thread
        thread = Threads.objects.get(id=request.data.get('thread'))
        if thread.creating_user.id != self.request.user.id:
            raise BadRequestException("Serializer is invalid")
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class UserThreadJunctionsPoint(mixins.ListModelMixin, generics.GenericAPIView):
    '''UserThreadJunctionsPoint
    An API endpoint. Handling user_thread_junction, returning all a users user_thread_junction

    Accepts: 'GET'
    'api/user_thread_junctions/' -> Returns all user_thread_junction records that are associated with the logged in user
    'api/user_thread_junctions/?thread_id={PK}' -> Returns all user_thread_junction records that are associated with the thread PK

    returns: list of user_thread_junction records, or throws error
    '''
    queryset = UserThreadJunctions.objects.all()
    serializer_class = UserThreadJunctionsSerializer 
    
    def get_queryset(self):
        thread_id_query = self.request.GET.get('thread_id', None)
        if thread_id_query:
            response_object = self.queryset.filter(thread=thread_id_query)
        else:
            response_object = self.queryset.filter(user=self.request.user.id)
        return response_object

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ThreadMessagesPoint(mixins.ListModelMixin, generics.GenericAPIView):
    '''ThreadMessagesPoint
    An API endpoint. Handling thread_message, returns records of thread_messages from a particular thread

    Accepts: 'GET'
    'api/thread_messages/?thread_id={PK}' -> Returns all thread_message records that are associated with the thread PK, and checks user is connected to thread

    returns: list of thread_messages records, or throws error
    '''
    queryset = ThreadMessages.objects.all()
    serializer_class = ThreadMessagesSerializer   
    
    def get_queryset(self):
        try:
            thread_id_query = self.request.GET.get('thread_id', None)
            if thread_id_query:
                user_thread_junction = UserThreadJunctions.objects.get(user=self.request.user.id, thread_id = thread_id_query)
                if not user_thread_junction:
                    raise NotFoundException("Thread doesn't exist")
                return self.queryset.filter(thread_id=thread_id_query)
            else:
                raise BadRequestException("No 'thread_id' query present")
        except ObjectDoesNotExist:
            raise NotFoundException("Thread doesn't exist")

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
# I wrote this code -------------------------- End