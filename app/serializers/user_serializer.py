from oxapy import serializer  # type: ignore
from sqlalchemy.orm import Session

from app.core.utils import new_id
from app.models import User


class Crendential(serializer.Serializer):
    email = serializer.EmailField()
    password = serializer.CharField(min_length=8)


class UserSerializer(serializer.Serializer):
    id = serializer.CharField(write_only=True, required=False)
    name = serializer.CharField()
    email = serializer.EmailField()
    password = serializer.CharField(write_only=True, min_length=8)

    def create(self, session: Session, validated_data: dict):
        user_id = new_id()
        validated_data["id"] = user_id
        return super().create(session, validated_data)

    class Meta:
        models = User


class UpdateUserSerializer(serializer.Serializer):
    name = serializer.CharField()
    email = serializer.EmailField()
