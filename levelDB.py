import plyvel

db = plyvel.DB('./testdb', create_if_missing=True)

# db.put(b'key', b'value')
# db.put(b'another-key', b'another-value')
# # db.delete(b'another-key')
# # db.delete(b'key')
# # print(db.get(b'key'))
# # print(db.get(b'another-key'))
# # # print(db.get(b'yet-another-key'))
stateDB = {}
with db.iterator() as it:
    for k, v in it:
        stateDB[k] = v
        # db.delete(k)


print(stateDB)

# '''tranverse the key and value in stateDB'''
# stateDB = {b's'+b'key': b'value', b's'+b'another-key': b'another-value'}
# print(stateDB)
# key = list(stateDB.keys())
# value = list(stateDB.values())
# with db.write_batch() as b:
#     for n in range(len(key)):
#         b.put(key[n], value[n])
#
# print(stateDB)
