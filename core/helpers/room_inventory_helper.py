from datetime import datetime

from ..models import RoomInventory


def search(args):
    room_inventories = RoomInventory.find_by_hotel(args['hotel_id'])
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
