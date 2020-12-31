from rest_framework import serializers
from .models import Preference, Politician, Profile
from django.contrib.auth.models import User

class PreferenceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('owner', 'criminal_justice', 'economy_taxes','abortion', 'education', 'minority_support','immigration', 'environment', 'lbgtq_rights', 'womens_rights', 'health_care', 'corporations', 'national_security', 'gun_control')

class PoliticianSerializers(serializers.ModelSerializer):
    class Meta:
        model = Politician
        fields = ('name', 'age', 'position', 'location', 'up_for_re_election', 'biography' 'preference', 'criminal_justice', 'economy_taxes','abortion', 'education', 'minority_support','immigration', 'environment', 'lbgtq_rights', 'womens_rights', 'health_care', 'corporations', 'national_security', 'gun_control')

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'preference')

