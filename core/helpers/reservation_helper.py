from ..models import Reservation, RoomInventory
from datetime import datetime


def confirm_reservation(reservation_id, conf_number):
    status = "confirmed" if conf_number == "1" else "cancelled"
    reservation = Reservation.get_by_id(reservation_id)
    reservation.conf_number = conf_number
    reservation.status = status
    return reservation.save()


def create_reservation(payload):
    check_in = datetime.strptime(payload['check_in'], "%Y-%m-%dT%H:%M:%S.%fZ")
    check_out = datetime.strptime(payload['check_out'], "%Y-%m-%dT%H:%M:%S.%fZ")
    room_inventory = RoomInventory.find_by_id(payload['room_inventory_id'])

    for rate in room_inventory.daily_rates:
        print rate.date, type(rate.date)
        if check_in <= rate.date <= check_out:
            rate.remain -= 1

    room_inventory.save()

    reservation = Reservation.from_document(payload)
    reservation.created_at = datetime.utcnow()
    return reservation.save()
