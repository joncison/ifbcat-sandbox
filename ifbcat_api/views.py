# Imports
#
# "Response" is used to return responses from APIView
# "status" object holds HTTP status codes - used when returning responses from the API
# TokenAuthentication is used to users to authenticate themselves with the API
# "filters" is for filtering the ViewSets
# "ObtainAuthToken" is a view used to generate an auth token
# "api_settings" is used when configuring the custom ObtainAuthToken view
# "IsAuthenticatedOrReadOnly" is used to ensure that a ViewSet is read-only if the user is not autheticated.
# "IsAuthenticated" is used to block access to an entire ViewSet endpoint unless a user is autheticated
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from ifbcat_api import serializers
from ifbcat_api import models
from ifbcat_api import permissions


class SourceInfoViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            with open("source_info.json", "r") as stream:
                info = json.load(stream)
                info["commit_url"] = "https://github.com/IFB-ElixirFr/ifbcat/commit/%s" % info["commit_sha"]
                return Response(info)
        except FileNotFoundError as e:
            return Response(str(e))


# TestApiView is just a test API View - not currently used but kept in case it's needed later.
class TestApiView(APIView):
    """Test API View.  Currently just returns a test message."""

    serializer_class = serializers.TestApiViewSerializer

    # format=None can be updated if support for other formats is required in future.
    def get(self, request, format=None):
        """Returns a test message."""
        msg = ["Test message."]

        return Response({'message': msg})

    def post(self, request):
        """Creates a test message."""
        # "self.serializer_class" function retrieves the serializer class configured above
        # "data=request.data" assigns the data passed in from the POST request, to the serializer
        serializer = self.serializer_class(data=request.data)

        # is_valid() function valdates the data as per the definition in serializers.py (where "testinput" is defined)
        if serializer.is_valid():
            testinput = serializer.validated_data.get('testinput')
            message = f'Test input was: {testinput}'
            return Response({'message': message})
        else:
            # "serializer.errors" is dictionary of errors generated by the serializer.
            # Good to return this to the user in case they submitted an invlid response.
            # 400 is the standard response code for this sort of error.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


# TestViewSet is just a test API ViewSet - not currently used but kept in case it's needed later.
class TestViewSet(viewsets.ViewSet):
    """Test API ViewSet.  Currently just returns a test message."""

    # Note - reusing the serializer that was used for the "TestApiView" APIView - this is OK!
    serializer_class = serializers.TestApiViewSerializer

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


# UserProfile ViewSet
# This is a ModelViewSet (which are bundled with functionality for managing models through the API)
# They're wired to a serializer class, and a query set is provided so it knows which objects
# in the DB are managed through this ViewSet
# Django REST takes care of create, list, update etc. functions on the ViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    # permission_classes set how user has gets permission to do certain things.
    permission_classes = (permissions.UpdateOwnProfile,)

    # filter_backends adds ability to search profiles by name or email (via filtering)
    # search_fields specifies which fields are searchable by this filter.
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'firstname',
        'lastname',
        'email',
        'orcidid',
        'expertise__topic',
    )


# Class for handling user authentication.
# ObtainAuthToken has to be customised so that is enabled in the Django admin site
# (this is not not enabled by default)
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens."""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# Model ViewSet for news item
class NewsItemViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating news items."""

    serializer_class = serializers.NewsItemSerializer
    queryset = models.NewsItem.objects.all()

    #  This ensures users can only create news items when the user profile is assigned to them.
    # i.e. they cannot update news items of other users in the system.
    # "IsAuthenticatedOrReadOnly" (imported above) permission ensures users must be autheticated to perform any request that is not a read request
    # i.e. they cannot create new feed items when they're not autheticated.
    # NB. Could instead use "IsAuthenticated" to restrict access of the entire endpoint to autheticated users.
    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)

    # Set the user_profile to read-only
    # "perform_create" is a convenience function for customising object creation through a model ViewSet.
    # When a request is made to the ViewSet, it gets passed to the serializer, is validated, then the
    # (because it's a ModelSerializer) a serializer.save function is called, which saves the content of
    # the serializer to an object in the database.
    #
    # "serializer.save" is called manually below, and we pass in user_profile
    # "request" object is passed into all ViewSets whenever a request is made.
    # Because we added TokenAuthentication to the ViewSet, if the user has autheticated, then the request
    # will have a user associatd with it.
    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('news',)


# Model ViewSet for events
class EventViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating events."""

    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    permission_classes = (
        permissions.PubliclyReadableEditableByOwner | permissions.PubliclyReadableEditableByContact,
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'shortName',
        'description',
        'type',
        'venue',
        'city',
        'country',
        'costs_cost',
        'topics__topic',
        'keywords__keyword',
        'prerequisites__prerequisite',
        'accessibility',
        'accessibilityNote',
        'contactName',
        'contactId__name',
        'contactEmail',
        'market',
        'elixirPlatforms__name',
        'communities__name',
        'hostedBy__name',
        'organisedByTeams__name',
        'organisedByBioinformaticsTeams__name',
        'organisedByOrganisations__name',
        'sponsoredBy__name',
        'sponsoredBy__organisationId__name',
    )


# Model ViewSet for training events
class TrainingEventViewSet(EventViewSet):
    """Handles creating, reading and updating training events."""

    serializer_class = serializers.TrainingEventSerializer
    queryset = models.TrainingEvent.objects.all()

    permission_classes = (
        permissions.PubliclyReadableEditableByTrainers
        | permissions.PubliclyReadableEditableByContact
        | permissions.PubliclyReadableEditableByOwner,
        IsAuthenticated,
    )

    search_fields = EventViewSet.search_fields + (
        'audienceTypes__audienceType',
        'audienceRoles__audienceRole',
        'difficultyLevel',
        'learningOutcomes',
    )


# Model ViewSet for keywords
class KeywordViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating keywords."""

    serializer_class = serializers.KeywordSerializer
    queryset = models.Keyword.objects.all()
    lookup_field = 'keyword__iexact'

    permission_classes = (permissions.PubliclyReadableByUsers, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Saves the serializer."""
        serializer.save()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('keyword',)


# Model ViewSet for event prerequisites
class EventPrerequisiteViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating event prerequisites."""

    serializer_class = serializers.EventPrerequisiteSerializer
    queryset = models.EventPrerequisite.objects.all()

    permission_classes = (permissions.PubliclyReadableByUsers, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Saves the serializer."""
        serializer.save()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('prerequisite',)


# Model ViewSet for trainer
class TrainerViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating trainers."""

    serializer_class = serializers.TrainerSerializer
    queryset = models.Trainer.objects.all()

    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'trainerName',
        'trainerEmail',
    )


# Model ViewSet for training event metrics
class TrainingEventMetricsViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating training event metrics."""

    serializer_class = serializers.TrainingEventMetricsSerializer
    queryset = models.TrainingEventMetrics.objects.all()

    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'dateStart',
        'dateEnd',
    )


# Model ViewSet for event sponsors
class EventSponsorViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating event sponsors."""

    serializer_class = serializers.EventSponsorSerializer
    queryset = models.EventSponsor.objects.all()
    lookup_field = 'name'

    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# Model ViewSet for organisation
class OrganisationViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating organisations."""

    serializer_class = serializers.OrganisationSerializer
    queryset = models.Organisation.objects.all()
    lookup_field = 'name'

    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'description',
        'homepage',
        'orgid',
        'fields__field',
        'city',
    )


# Model ViewSet for elixirPlatform
class ElixirPlatformViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating elixirPlatforms."""

    serializer_class = serializers.ElixirPlatformSerializer
    queryset = models.ElixirPlatform.objects.all()
    lookup_field = 'name'

    permission_classes = (permissions.PubliclyReadableEditableByCoordinator, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'description',
        'homepage',
        'coordinator__firstname',
        'coordinator__lastname',
        'coordinator__email',
        'deputies__firstname',
        'deputies__lastname',
        'deputies__email',
    )


# Model ViewSet for elixirPlatform
class CommunityViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating elixirPlatforms."""

    serializer_class = serializers.CommunitySerializer
    queryset = models.Community.objects.all()
    lookup_field = 'name'

    permission_classes = (permissions.PubliclyReadableByUsers, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'description',
        'homepage',
        'organisations__description',
        'organisations__name',
    )


# Model ViewSet for projects
class ProjectViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating projects."""

    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()
    lookup_field = 'name'

    permission_classes = (
        permissions.PubliclyReadableEditableByOwner | permissions.PubliclyReadableEditableByMembers,
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    # TODO: : add to "search_fields" below:   'topics', 'hostedBy', 'fundedBy', 'communities', 'elixirPlatform'
    search_fields = (
        'name',
        'homepage',
        'description',
        'team__name',
        'uses_name',
    )


# Model ViewSet for resources
class ResourceViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating resources."""

    permission_classes = (permissions.PubliclyReadableEditableByOwner, IsAuthenticatedOrReadOnly)
    lookup_field = 'name'

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'description',
        'communities__name',
        'elixirPlatforms__name',
    )


# Model ViewSet for computing facilities
class ComputingFacilityViewSet(ResourceViewSet):
    """Handles creating, reading and updating computing facilities."""

    serializer_class = serializers.ComputingFacilitySerializer
    queryset = models.ComputingFacility.objects.all()
    permission_classes = (
        permissions.PubliclyReadableEditableByOwner | permissions.PubliclyReadableEditableByMembers,
        IsAuthenticatedOrReadOnly,
    )

    search_fields = ResourceViewSet.search_fields + (
        'homepage',
        'providedBy__name',
        'team',
        'accessibility',
        'serverDescription',
    )


# Model ViewSet for training materials
class TrainingMaterialViewSet(ResourceViewSet):
    """Handles creating, reading and updating training materials."""

    serializer_class = serializers.TrainingMaterialSerializer
    queryset = models.TrainingMaterial.objects.all()

    search_fields = ResourceViewSet.search_fields + (
        'doi__doi',
        'fileName',
        'topics__topic',
        'keywords__keyword',
        'audienceTypes__audienceType',
        'audienceRoles__audienceRole',
        'difficultyLevel',
        'providedBy__name',
        'license',
    )


# Model ViewSet for teams
class TeamViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating teams."""

    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
    lookup_field = 'name'

    permission_classes = (
        permissions.PubliclyReadableEditableByOwner | permissions.PubliclyReadableEditableByMembers,
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)

    filter_backends = (filters.SearchFilter,)
    # TODO: : add to "search_fields" below:   'team', 'providedBy'
    search_fields = (
        'name',
        'description',
        'expertise',
        'leader',
        'deputies',
        'scientificLeader',
        'technicalLeader',
        'members',
        'maintainers',
    )


# Model ViewSet for teams
class BioinformaticsTeamViewSet(TeamViewSet):
    """Handles creating, reading and updating bioinformatics teams."""

    serializer_class = serializers.BioinformaticsTeamSerializer
    queryset = models.BioinformaticsTeam.objects.all()

    # TODO: : add to "search_fields" below:   'team', 'providedBy'
    search_fields = TeamViewSet.search_fields + (
        'orgid',
        'unitId',
        'address',
        'fields',
        # 'topics__topic',
        # 'keywords__keyword',
        'ifbMembership',
        'platforms',
        'communities',
        'projects',
    )


# Model ViewSet for services
class ServiceViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating services."""

    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()
    lookup_field = 'name'

    permission_classes = (
        permissions.PubliclyReadableEditableByOwner | permissions.PubliclyReadableEditableByMembers,
        IsAuthenticatedOrReadOnly,
    )

    # TODO: : add to "search_fields" below:   'team', 'providedBy'
    search_fields = (
        'name',
        'description',
        'bioinformaticsTeams__name',
        'computingFacilities__name',
        'trainingEvents__name',
        'publications__doi',
    )


# Model ViewSet for service submissions
class ServiceSubmissionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating service submissions."""

    serializer_class = serializers.ServiceSubmissionSerializer
    queryset = models.ServiceSubmission.objects.all()

    permission_classes = (
        permissions.PubliclyReadableEditableByOwner
        | permissions.PubliclyReadableEditableBySubmitters
        | permissions.PubliclyReadableEditableByAuthors,
        IsAuthenticatedOrReadOnly,
    )

    search_fields = (
        'service__name',
        'authors',
        'submitters',
        'year',
        'motivation',
        'scope',
        'caseForSupport',
        'qaqc',
        'usage',
        'sustainability',
    )
