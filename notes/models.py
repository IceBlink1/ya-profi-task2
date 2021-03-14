from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=20000, blank=True, default='')
    content = models.CharField(max_length=20000, blank=True, default='')

    class Meta:
        ordering = ['id']


# Serializers define the API representation.
class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('content', instance.content)
        instance.save()
        return instance

