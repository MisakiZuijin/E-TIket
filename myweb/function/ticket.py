from function.storage import baca_data, simpan_data
from function.event import kurangi_stok, tampilkan_event

FILE_TICKET = "data_tickets.json"
FILE_EVENT = "data_events.json"

def beli_tiket(user_id, event_id, jumlah):
    events = tampilkan_event()
    harga_tiket = None
    for e in events:
        if e["id"] == event_id:
            harga_tiket = e["harga"]
            break

    if harga_tiket is None:
        return "Event tidak ditemukan!"

    total_harga = harga_tiket * jumlah

    if not kurangi_stok(event_id, jumlah):
        return "Stok tiket tidak mencukupi!"

    data = baca_data(FILE_TICKET)
    for tiket in data:
        if tiket["user_id"] == user_id and tiket["event_id"] == event_id:
            tiket["jumlah"] += jumlah
            tiket["total_harga"] += total_harga
            simpan_data(FILE_TICKET, data)
            return "success"

    data.append({
        "user_id": user_id,
        "event_id": event_id,
        "jumlah": jumlah,
        "total_harga": total_harga
    })
    simpan_data(FILE_TICKET, data)
    return "success"

def tiket_user(user_id):
    data = baca_data(FILE_TICKET)
    return [t for t in data if t["user_id"] == user_id]

def batalkan_tiket(user_id, event_id):
    data_tiket = baca_data(FILE_TICKET)
    data_event = baca_data(FILE_EVENT)

    tiket_baru = []
    jumlah_dikembalikan = 0

    for t in data_tiket:
        if t["user_id"] == user_id and t["event_id"] == event_id:
            jumlah_dikembalikan = t["jumlah"]
        else:
            tiket_baru.append(t)

    for e in data_event:
        if e["id"] == event_id:
            e["stok_tiket"] += jumlah_dikembalikan

    simpan_data(FILE_EVENT, data_event)
    simpan_data(FILE_TICKET, tiket_baru)
    return "success"