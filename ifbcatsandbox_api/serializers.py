# Imports
# "re" is regular expression library
import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ifbcatsandbox_api import models
from django.core.exceptions import ObjectDoesNotExist


# This is just for testing serialization
class TestApiViewSerializer(serializers.Serializer):
    """Serializes a test input field."""
    testinput = serializers.CharField(max_length=10)


# Model serializer for user profile
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile (UserProfile object)."""

    # Validation isn't specified for fields where basic validation defined in models.py is adequate
    # "allow_null" means None is considered a val'id' value (it defauls to False)
    # "required=False" means the field is not required to be present during (de)serialization (it defaults to True)
    # firstname, lastname and email are mandatory
    # NB. "allow_blank=False" means am empty string is considered invalid and will raise a validation error
    # (it is False by default, so no need to set it)

    # firstname (no further validation needed)
    # lastname (no further validation needed)
    # email (no further validation needed)
    # orcidid = serializers.CharField(
    #     allow_blank=False,
    #     allow_null=True,
    #     required=False,
    #     validators=[UniqueValidator(queryset = models.UserProfile.objects.all())])
    # homepage = serializers.URLField(allow_blank=False, allow_null=True, required=False)

    # Metaclass is used to configure the serializer to point to a specific object
    # and setup a list of fields in the model to manage with the serializer.
    class Meta:
        model = models.UserProfile
        fields = ('id', 'password', 'firstname', 'lastname', 'email', 'orcidid', 'homepage')

        # password field is set to be write-only - it should only be used when creating a new user profile
        # Would be security risk e.g. to allow password hash to be retrieved via API!
        # Also set the field style so that *** are given in the data entry field when the password is typed in
        extra_kwargs = {
            'password':
            {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # Validation logic
    def validate_orcidid(self, orcidid):
        """Validate supplied orcidid."""

        # orcidid is not mandatory - catch that
        if orcidid is None:
            return orcidid

        p = re.compile('^https?://orcid.org/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$', re.IGNORECASE | re.UNICODE)
        if not p.search(orcidid):
            raise serializers.ValidationError('This field can only contain a valid ORCID ID.  Syntax: ^https?://orcid.org/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$')
        return orcidid

    # Override the defult "create" function of the object manager, with the "create_user" function (defined in models.py)
    # This will ensure the password gets created as a hash, rather than clear text
    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile.objects.create_user(
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email'],
            orcidid=validated_data['orcidid'],
            homepage=validated_data['homepage'])

        return user

    # Override the default "update" function to ensure the user password is hashed when updating
    # If this was not done, if a user updated their profile, the password field would be stored in cleartext,
    # and they'd be unable to login
    # NB.  we "pop" (assign the value and remove from the dictionary) the password from the validated data
    # and set is using "set_password" which saves the password as a hash
    # "super().update()" is used to pass the values to the Django REST update() method, to handle updating the remaining fields.
    def update(self, instance, validated_data):
        """Handle updating user account."""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


# News item serializer
class NewsItemSerializer(serializers.ModelSerializer):
    """Serializes a news item (NewsItem object)."""

    # news and created_on are mandatory

    # news (no further validation needed)
    # created_on (no further validation needed)

    class Meta:
        model = models.NewsItem
        # By default, Django adds a primary key ID ('id') to all models that are created.
        # It's read-only by default and gets an integer value that's incremented from the corresponding database table.
        # The other fields come from NewsItem.
        # NB. "created_on" is also auto-created (and thus read-only)
        # Don't want users to be able to set the user profile when creating a news item!
        # It must be set to the autheticated user.  Thus it's read-only.
        # Set read-only fields using the shortcut "read_only_fields" rather than extra_kwargs:
        #   extra_kwargs = {
        #      'user_profile': {'read_only': True}}

        fields = ('id', 'user_profile', 'news', 'created_on')
        read_only_fields = ['user_profile']


# Model serializer for event keyword
class EventKeywordSerializer(serializers.ModelSerializer):
    """Serializes an event keyword (EventKeyword object)."""

    # keyword = serializers.CharField(
    #     allow_blank=False,
    #     required=False,
    #     validators=[UniqueValidator(queryset = models.EventKeyword.objects.all())])

    class Meta:
        model = models.EventKeyword
        fields = ('id', 'keyword')
        # extra_kwargs = {'id': {'read_only': True}}
        # fields = ('keyword')



# Model serializer for event prerequisite
class EventPrerequisiteSerializer(serializers.ModelSerializer):
    """Serializes an event prerequisite (EventPrerequisite object)."""

    # prerequisite = serializers.CharField(
    #     allow_blank=False,
    #     required=False,
    #     validators=[UniqueValidator(queryset = models.EventPrerequisite.objects.all())])

    class Meta:
        model = models.EventPrerequisite
        fields = ('id', 'prerequisite')



# See  https://stackoverflow.com/questions/28009829/creating-and-saving-foreign-key-objects-using-a-slugrelatedfield/28011896
class CreatableSlugRelatedField(serializers.SlugRelatedField):
    """Custom SlugRelatedField that creates the new object when one doesn't exist."""

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.get_queryset().create(**{self.slug_field: data})  # to create the object
        except (TypeError, ValueError):
            self.fail('invalid')


class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDate
        exclude = ('id',)
        extra_kwargs = dict(
            dateStart= dict(format="%Y-%m-%d"),
            dateEnd= dict(format="%Y-%m-%d"),
            timeStart = dict(format="%H:%M"),
            timeEnd = dict(format="%H:%M"),
        )


# Model serializer for user profile
class EventSerializer(serializers.ModelSerializer):
    """Serializes an event (Event object)."""

    # CharField in ModelSerializer corresponds to both CharField and TextField in Django models
    # IntegerField in ModelSerializer corresponds to PositiveSmallIntegerField etc. in Django models
    # For BooleanField, if an input value is omitted in HTML-encoded form, it
    # is treated as setting the value to False. However, the default of "required=True"
    # is not set for them, and "allow_blank" is not supported.
    # See https://www.django-rest-framework.org/api-guide/fields/#booleanfield
    #
    # max_value of maxParticipants set to 32767 corresponding to PositiveSmallIntegerField defined in models.py
    # See https://www.geeksforgeeks.org/positivesmallintegerfield-django-models/
    #
    #
    # "many=True" for keyword etc. instantiates a ListSerializer, see https://www.django-rest-framework.org/api-guide/serializers/#listserializer
    # "allow_empty=False" disallows empty lists as valid input.

    # name, description, homepage, accessibility, contactName and contactEmail are mandatory

    costs = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="cost",
        queryset=models.EventCost.objects.all())

    topics = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="topic",
        queryset=models.EventTopic.objects.all())
    # keyword = EventKeywordSerializer(many=True, allow_empty=False, required=False)
    keywords = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="keyword",
        queryset=models.EventKeyword.objects.all())
    prerequisites = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="prerequisite",
        queryset=models.EventPrerequisite.objects.all())
    dates = EventDateSerializer(
        many=True,
        read_only=False,
        required=False,
    )
    elixirPlatforms = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="name",
        queryset=models.ElixirPlatform.objects.all())
    communities = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="name",
        queryset=models.Community.objects.all())
    hostedBy = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        lookup_field="name",
        view_name='organisation-detail',
        queryset=models.Organisation.objects,
    )

#    accessibility = serializers.ChoiceField(
#         choices = ('Public', 'Private'),
#         allow_blank=True,
#         required=False)


    # To-add to "fields" below:  'organisedBy', 'sponsoredBy', 'logo'
    class Meta:
        model = models.Event

        fields = ('id', 'user_profile', 'name', 'shortName', 'description', 'homepage', 'type', 'dates',
        'venue', 'city', 'country', 'onlineOnly', 'costs', 'topics', 'keywords', 'prerequisites', 'accessibility', 'accessibilityNote',
        'maxParticipants', 'contactName', 'contactEmail', 'contactId', 'market', 'elixirPlatforms', 'communities', 'hostedBy')

        # "{'style': {'rows': 4, 'base_template': 'textarea.html'}}" sets the field style to an HTML textarea
        # See https://www.django-rest-framework.org/topics/html-and-forms/#field-styles

        extra_kwargs = {
            # 'id': {'read_only': True},
            'user_profile': {'read_only': True},
            'description': {'style': {'rows': 4, 'base_template': 'textarea.html'}},
            'venue': {'style': {'rows': 4, 'base_template': 'textarea.html'}},
        }

    # Validation logic
    def validate_topics(self, topics):
        """Validate supplied EDAM topic URIs."""

        # topics is not mandatory - catch that
        if topics is None:
            return topics

        p = re.compile('^https?://edamontology.org/topic_[0-9]{4}$', re.IGNORECASE | re.UNICODE)
        for topic in topics:
            if not p.search(topic.__str__()):
                raise serializers.ValidationError('This field can only contain valid EDAM Topic URIs.  Syntax: ^https?://edamontology.org/topic_[0-9]{4}$')
        return topics


    # Validation logic
    def validate_costs(self, costs):
        """Validate supplied event costs."""

        if costs is None:
            return costs

        # In TextChoices (e.g. CostType):
        # .values gives e.g. "Free to academics" - the actual term we want in the database (as specified in the object)
        # .names gives e.g. "FREE_TO_ACADEMICS" (the variable name)
        # .labels gives e.g. "Free to Academics" (derived from the variable name )
        for cost in costs:
            if cost.__str__() not in models.EventCost.CostType.values:
                msg = 'This field can only contain valid cost strings: ' + ','.join(models.EventCost.CostType.values)
                raise serializers.ValidationError(msg)
        return costs

    def update(self, instance, validated_data):
        sub_instances = dict()
        for nested_field in [
            'dates',
        ]:
            try:
                serialized_sub_instances = validated_data.pop(nested_field)
            except KeyError:
                continue
            # get the serializer, then the model, then the model manager
            qs = self.fields[nested_field].child.Meta.model.objects
            sub_instances_for_this_field = sub_instances.setdefault(nested_field, [])
            # iterate over each values (json dict) provided for the field, also remove them from validated_data
            for serialized_sub_instance in serialized_sub_instances:
                # get or create it
                sub_instance, _ = qs.get_or_create(**serialized_sub_instance)
                # append the instance the new new list of sub_instance the instance will be associated with
                sub_instances_for_this_field.append(sub_instance)
        # update this object minus the nested field(s)
        super().update(instance=instance, validated_data=validated_data)
        # for each fields, set the new sub instances list
        for k, v in sub_instances.items():
            getattr(instance, k).set(v)
        if len(sub_instances) > 0:
            instance.save()
        return instance



# Organisation serializer
class OrganisationSerializer(serializers.ModelSerializer):
    """Serializes an organisation (Organisation object)."""

    fields = CreatableSlugRelatedField(
        many=True,
        read_only=False,
        slug_field="field",
        queryset=models.OrganisationField.objects.all())


    class Meta:
        model = models.Organisation

        # logo ... TO_DO
        fields = ('id', 'user_profile', 'name', 'description', 'homepage', 'orgid', 'fields', 'city')
        read_only_fields = ['user_profile']


    # Validation logic
    def validate_orgid(self, orgid):
        """Validate supplied organisation ID (GRID or ROR ID)."""

        # orcidid is not mandatory - catch that
        if orgid is None:
            return orcidid

        p1 = re.compile('^grid.[0-9]{4,}.[a-f0-9]{1,2}$', re.IGNORECASE | re.UNICODE)
        p2 = re.compile('^0[0-9a-zA-Z]{6}[0-9]{2}$', re.IGNORECASE | re.UNICODE)
        if not p1.search(orgid):
            if not p2.search(orgid):
                raise serializers.ValidationError('This field can only contain a valid GRID or ROR ID.   GRID ID Syntax: grid.[0-9]{4,}.[a-f0-9]{1,2}   ROR ID Syntax: ^0[0-9a-zA-Z]{6}[0-9]{2}')
        return orgid
