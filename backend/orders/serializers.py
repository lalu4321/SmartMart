from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
    ReturnRequest,
    Refund,
)


# ============================
# Address Serializer
# ============================

class OrderAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order.shipping_address.field.related_model

        fields = (
            "id",
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "landmark",
            "city",
            "district",
            "state",
            "country",
            "pincode",
        )



# ============================
# Order Item Serializer
# ============================

class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True
    )

    variant_name = serializers.CharField(
        source="variant.variant_name",
        read_only=True
    )


    product_image = serializers.SerializerMethodField()


    def get_product_image(self, obj):

        try:

            image = obj.variant.product.images.first()

            if image:

                request = self.context.get("request")

                if request:
                    return request.build_absolute_uri(
                        image.image.url
                    )

                return image.image.url

        except Exception:
            pass

        return None



    class Meta:

        model = OrderItem

        fields = (
            "id",
            "variant",
            "product_name",
            "product_image",
            "variant_name",
            "quantity",
            "unit_price",
            "total_price",
        )



# ============================
# Order Status History
# ============================

class OrderStatusHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderStatusHistory

        fields = (
            "id",
            "status",
            "remarks",
            "created_at",
        )
# ============================
# Order Serializer
# ============================

class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="account.username",
        read_only=True
    )


    shipping_address = OrderAddressSerializer(
        read_only=True
    )


    items = OrderItemSerializer(
        many=True,
        read_only=True
    )


    status_history = OrderStatusHistorySerializer(
        many=True,
        read_only=True
    )


    class Meta:

        model = Order

        fields = (
            "id",
            "order_number",
            "account",
            "customer_name",
            "shipping_address",
            "status",
            "total_amount",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        )


        read_only_fields = (
            "id",
            "order_number",
            "account",
            "customer_name",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        )



# ============================
# Return Request Serializer
# ============================

class ReturnRequestSerializer(serializers.ModelSerializer):

    class Meta:

        model = ReturnRequest

        fields = (
            "id",
            "order",
            "reason",
            "status",
            "requested_at",
            "updated_at",
        )


        read_only_fields = (
            "id",
            "status",
            "requested_at",
            "updated_at",
        )



# ============================
# Refund Serializer
# ============================

class RefundSerializer(serializers.ModelSerializer):

    class Meta:

        model = Refund

        fields = (
            "id",
            "return_request",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )


        read_only_fields = (
            "id",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )