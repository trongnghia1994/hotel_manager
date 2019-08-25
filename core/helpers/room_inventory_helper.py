from datetime import datetime

from bson import ObjectId

from ..models import RoomInventory, Accommodation


def find_room_inventories_by_hotel(hotel_id):
    accommodations = Accommodation.objects.raw({'hotel_id': ObjectId(hotel_id)})
    acc_ids = [a._id for a in list(accommodations) if accommodations]
    room_inventories = RoomInventory.objects.raw({'accommodation_id': {'$in': acc_ids}})
    return room_inventories


def search(args):
    room_inventories = find_room_inventories_by_hotel(args['hotel_id'])
    results = []
    utcnow = datetime.utcnow()
    for room_inventory in room_inventories:
        # Check for available rooms
        if not room_inventory.sell_start_date <= utcnow <= room_inventory.sell_end_date:
            continue

        for rate in room_inventory.daily_rates:
            if rate.remain <= 0:
                continue

        results.append(room_inventory)

    return results
