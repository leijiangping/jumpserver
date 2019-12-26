# -*- coding: utf-8 -*-
#

from django.utils.translation import ugettext as _
from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import AuthBook, Asset
from ..backends import AssetUserManager

from .base import ConnectivitySerializer, AuthSerializerMixin


__all__ = [
    'AssetUserWriteSerializer',
    'AssetUserReadSerializer', 'AssetUserAuthInfoSerializer',
    'AssetUserExportSerializer', 'AssetUserPushSerializer',
]


class AssetUserWriteSerializer(AuthSerializerMixin, BulkOrgResourceModelSerializer):
    class Meta:
        model = AuthBook
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'username', 'password', 'private_key',
            'asset', 'comment',
        ]
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True},
            'private_key': {'write_only': True},
            'public_key': {'write_only': True},
        }


class AssetUserReadSerializer(AssetUserWriteSerializer):
    hostname = serializers.CharField(read_only=True, label=_("Hostname"))
    ip = serializers.CharField(read_only=True, label=_("IP"))
    asset = serializers.CharField(source='asset_id')
    backend = serializers.CharField(read_only=True, label=_("Backend"))

    class Meta(AssetUserWriteSerializer.Meta):
        read_only_fields = (
            'date_created', 'date_updated',
            'created_by', "version",
        )
        fields = AssetUserWriteSerializer.Meta.fields + [
            "hostname", "ip", "backend",
            "version",
            "date_created", "date_updated",
        ]
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True},
            'private_key': {'write_only': True},
            'public_key': {'write_only': True},
        }

    def create(self, validated_data):
        if not validated_data.get("name") and validated_data.get("username"):
            validated_data["name"] = validated_data["username"]
        instance = AssetUserManager.create(**validated_data)
        instance.set_to_latest()
        return instance






class AssetUserExportSerializer(AssetUserReadSerializer):
    password = serializers.CharField(
        max_length=256, allow_blank=True, allow_null=True,
        required=False, label=_('Password')
    )
    public_key = serializers.CharField(
        max_length=4096, allow_blank=True, allow_null=True,
        required=False, label=_('Public key')
    )
    private_key = serializers.CharField(
        max_length=4096, allow_blank=True, allow_null=True,
        required=False, label=_('Private key')
    )


class AssetUserAuthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthBook
        fields = ['password', 'private_key', 'public_key']


class AssetUserPushSerializer(serializers.Serializer):
    asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects, label=_("Asset"))
    username = serializers.CharField(max_length=1024)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
