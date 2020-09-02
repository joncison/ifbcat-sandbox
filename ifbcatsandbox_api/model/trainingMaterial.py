# Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

from ifbcatsandbox_api.model.resource import *
from ifbcatsandbox_api.model.misc import *
from ifbcatsandbox_api.model.bioinformaticsTeam import *


# Training material model
class TrainingMaterial(Resource):
    """Training material model: Digital media such as a presentation or tutorial that can be used for bioinformatics training or teaching."""

    class TrainingMaterialLicenseName(models.TextChoices):
        """Controlled vocabulary of training material licenses."""

        LICENSE_A = 'License A', _('License A')

    # fileLocation, fileName is mandatory
    # TO-DO:  providedBy
    doi = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        help_text="Unique identier (DOI) of the training material, e.g. a Zenodo DOI.",
    )
    fileLocation = models.URLField(
        max_length=255, help_text="A link to where the training material can be downloaded or accessed."
    )
    fileName = models.CharField(
        max_length=255, help_text="The name of a downloadable file containing the training material."
    )
    topics = models.ManyToManyField(
        Topic,
        blank=True,
        related_name='trainingMaterials',
        help_text="URIs of EDAM Topic terms describing the scope of the training material.",
    )
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        related_name='trainingMaterials',
        help_text="A keyword (beyond EDAM ontology scope) describing the training material.",
    )
    audienceTypes = models.ManyToManyField(
        AudienceType,
        blank=True,
        related_name='trainingMaterials',
        help_text="The education or professional level of the expected audience of the training material.",
    )
    audienceRoles = models.ManyToManyField(
        AudienceRole,
        blank=True,
        related_name='trainingMaterials',
        help_text="The professional roles of the expected audience of the training material.",
    )
    difficultyLevel = models.CharField(
        max_length=255,
        choices=DifficultyLevelType.choices,
        blank=True,
        help_text="The required experience and skills of the expected audience of the training material.",
    )
    providedBy = models.ManyToManyField(
        BioinformaticsTeam,
        blank=True,
        related_name='trainingMaterials',
        help_text="The bioinformatics team that provides the training material.",
    )
    dateCreation = models.DateField(help_text="Date when the training material was created.")
    dateUpdate = models.DateField(help_text="Date when the training material was updated.")
    license = models.CharField(
        max_length=255,
        choices=TrainingMaterialLicenseName.choices,
        blank=True,
        help_text="License under which the training material is made available.",
    )

    def __str__(self):
        """Return the TrainingMaterial model as a string."""
        return self.name