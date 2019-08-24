from ..models import Accommodation


def find_hotel_accommodations(hotel_id):
    return Accommodation.objects.find({"hotel_id": hotel_id})
