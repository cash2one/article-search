# coding: utf-8
from rest_framework import serializers
from common.helper import RestfulJsonField
from composition.models import Composition


class CompositionSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username', 
        label=Composition._meta.get_field('creator').verbose_name)
    approver = serializers.ReadOnlyField(source='approver.username', 
        label=Composition._meta.get_field('approver').verbose_name)
    json_tags = RestfulJsonField(source='tags', allow_null=True, required=False, 
        label=Composition._meta.get_field('tags').verbose_name)
    status = serializers.ReadOnlyField(source='get_status_display', 
        label=Composition._meta.get_field('status').verbose_name)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'json_tags', 'atype', 'grade', 'number', \
            'content', 'source', 'creator', 'approver', 'status', 'image', \
            'abstract', 'beginning', 'ending', 'created', 'modified',)
        read_only_fields = ('created', 'modified', 'status','image',)

class CompositionDetailSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username', 
        label=Composition._meta.get_field('creator').verbose_name)
    approver = serializers.ReadOnlyField(source='approver.username', 
        label=Composition._meta.get_field('approver').verbose_name)
    json_tags = RestfulJsonField(source='tags', allow_null=True, required=False, 
        label=Composition._meta.get_field('tags').verbose_name)
    status = serializers.ReadOnlyField(source='get_status_display', 
        label=Composition._meta.get_field('status').verbose_name)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'json_tags', 'atype', 'grade', 'number', \
            'content', 'source', 'creator', 'approver', 'status', 'image', \
            'abstract', 'beginning', 'ending', 'created', 'modified',)
        read_only_fields = ('created', 'modified','status','image',)

class CompositionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ('id','image', )
