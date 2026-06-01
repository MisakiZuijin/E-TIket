from function.storage import baca_data, simpan_data

FILE_EVENT = "data_events.json"

def tambah_event(nama, tanggal, lokasi, harga, stok_tiket):
    data = baca_data(FILE_EVENT)
    new_id = len(data) + 1

    data.append({
        "id": new_id,
        "nama": nama,
        "tanggal": tanggal,
        "lokasi": lokasi,
        "harga": harga,
        "stok_tiket": stok_tiket
    })

    simpan_data(FILE_EVENT, data)

def tampilkan_event():
    return baca_data(FILE_EVENT)

def ubah_event(event_id, nama, tanggal, lokasi, harga, stok_tiket):
    data = baca_data(FILE_EVENT)
    for e in data:
        if e["id"] == event_id:
            e["nama"] = nama
            e["tanggal"] = tanggal
            e["lokasi"] = lokasi
            e["harga"] = harga
            e["stok_tiket"] = stok_tiket
            break
    simpan_data(FILE_EVENT, data)

def hapus_event(event_id):
    data = baca_data(FILE_EVENT)
    data_baru = [e for e in data if e["id"] != event_id]
    simpan_data(FILE_EVENT, data_baru)

def kurangi_stok(event_id, jumlah):
    data = baca_data(FILE_EVENT)
    for e in data:
        if e["id"] == event_id:
            if e["stok_tiket"] >= jumlah:
                e["stok_tiket"] -= jumlah
                simpan_data(FILE_EVENT, data)
                return True
            else:
                return False
    return False