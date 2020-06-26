# Imports
# "Response" is used to return responses from APIView
# "status" object holds HTTP status codes - used when returning responses from the API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from ifbcatsandbox_api import serializers

# ChangelogView is just a test API View, done in case APIView(s) are needed in the ifbcatsandbox API
class ChangelogView(APIView):
    """Test API View.  Currently just returns the ifbcatsandbox API changelog."""

    serializer_class = serializers.ChangelogSerializer

    # format=None can be updated if support for other formats is required in future.
    def get(self, request, format=None):
        """Returns the ifbcatsandbox API changelog."""
        changelog = [
        'ifbcatsandbox API changelog.',
        '1. UserProfile model: customises default user model (to use email rather than username).',
        '   Supports creation of normal and super-users.',
        '2. Djano Admin is configured and tested (available at /admin endpoint).',
        '3. /api/changelog endpoint: returns the implementation changelog of the API',
        ]

        return Response({'message': changelog})

    def post(self, request):
        """Creates a test message."""
        # "self.serializer_class" function retrieves the serializer class configured above
        # "data=request.data" assigns the data passed in from the POST request, to the serializer
        serializer = self.serializer_class(data=request.data)

        # is_valid() function valdates the data as per the definition in serializers.py (where "testinput" is defined)
        if(serializer.is_valid()):
            testinput = serializer.validated_data.get('testinput')
            message = f'Test input was: {testinput}'
            return Response({'message': message})
        else:
            # "serializer.errors" is dictionary of errors generated by the serializer.
            # Good to return this to the user in case they submitted an invlid response.
            # 400 is the standard response code for this sort of error.
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    # "pk=None" defaults the primary key to none (normally the ID of the object being updated is specified)
    def put(self, request, pk=None):
        """Dummy "put" method (to update an object)."""
        return Response({'method called': 'PUT'})

    def patch(self, request, pk=None):
        """Dummy "patch" method (for partial update of an object)."""
        return Response({'method called': 'PATCH'})

    def delete(self, request, pk=None):
        """Dummy "delete" method (to delete an object)."""
        return Response({'method called': 'DELETE'})



# TestViewSet is just a test API ViewSet
class TestViewSet(viewsets.ViewSet):
    """Test API ViewSet.  Currently just returns the ifbcatsandbox API changelog."""

    # Note - reusing the serializer that was used for the "Changelog" APIView - this is OK!
    serializer_class = serializers.ChangelogSerializer

    # "list" method returns list of objects.  The list request corresponds to the root of the API.
    def list(self, request):
        """Dummy "list" method (to list set of objects that ViewSet represents)"""
        message = [
        "Test message for list method on APIViewSet.",
        ]

        return Response({'message': message})


    # "create" method is used to create new objects
    def create(self, request):
        """Dummy "create" method (to create a new object)"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            testinput = serializer.validated_data.get('testinput')
            message = f'testinput: {testinput}'
            return Response({'message': message})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    # "retrieve" function is for retrieving a specific object in the ViewSet
    # A primary key (pk) ID is passed into the URL / request
    def retrieve(self, request, pk=None):
        """Dummy "retrieve" function (to get an object by its ID)"""
        return Response({'http_method:': 'GET'})

    # "update" function is for updating a specific object in the ViewSet
    # A primary key (pk) ID is  passed into the URL / request
    def update(self, request, pk=None):
        """Dummy "update" function (to update an object)"""
        return Response({'http_method:': 'PUT'})

    # "partial_update" function is for partially updating a specific object in the ViewSet
    # A primary key (pk) ID is passed into the URL / request
    def partial_update(self, request, pk=None):
        """Dummy "partial_update" function (to partially update an object)"""
        return Response({'http_method:': 'PATCH'})

    # "destroy" function is for deleting a specific object in the ViewSet
    # A primary key (pk) ID is passed into the URL / request
    def destroy(self, request, pk=None):
        """Dummy "destroy" function (to delete an object)"""
        return Response({'http_method:': 'DELETE'})
