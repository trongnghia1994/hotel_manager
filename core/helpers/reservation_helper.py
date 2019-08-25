from datetime import datetime

from bson import ObjectId

from ..models import Reservation, RoomInventory, Accommodation


def confirm_reservation(reservation_id, conf_number):
    status = "confirmed" if conf_number == "1" else "cancelled"
    reservation = Reservation.find_reservation(reservation_id)
    reservation.conf_number = conf_number
    reservation.status = status
    return reservation.save()


def create_reservation(payload):
    check_in = datetime.strptime(payload['check_in'], "%Y-%m-%d")
    check_out = datetime.strptime(payload['check_out'], "%Y-%m-%d")
    room_inventory = RoomInventory.find_room_inventory(payload['room_inventory_id'])

    for rate in room_inventory.daily_rates:
        if rate.remain > 0 and (check_in <= rate.date < check_out):
            rate.remain -= 1

    room_inventory.save()

    reservation = Reservation.from_document(payload)
    reservation.created_at = datetime.utcnow()
    return reservation.save()


def find_reservations_by_hotel(hotel_id):
    accommodations = Accommodation.objects.raw({'hotel_id': ObjectId(hotel_id)})
    acc_ids = [a._id for a in list(accommodations) if accommodations]
    room_inventories = RoomInventory.objects.raw({'accommodation_id': {'$in': acc_ids}})
    ri_ids = [ri._id for ri in list(room_inventories) if room_inventories]
    reservations = Reservation.objects.raw({'room_inventory_id': {'$in': ri_ids}, 'status': 'pending'})
    return reservations
