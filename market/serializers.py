from rest_framework import serializers
from .models import Listing, Offer

class ListingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    seller = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'category', 'price', 'condition_display', 'image_url', 'seller']

    def get_title(self, obj):
        return obj.game.title if obj.game else obj.custom_title

    def get_category(self, obj):
        return obj.game.category.name if obj.game else "Inne"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'listing', 'price', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at', 'buyer']

    def validate(self, data):
        listing = data['listing']
        offered_price = data['price']

        user = self.context['request'].user
        if listing.user == user:
            raise serializers.ValidationError("Nie możesz składać ofert do własnego ogłoszenia.")

        if offered_price >= listing.price:
            raise serializers.ValidationError("Proponowana cena musi być niższa niż cena wyjściowa.")

        if offered_price <= 0:
            raise serializers.ValidationError("Cena musi być dodatnia.")

        return data