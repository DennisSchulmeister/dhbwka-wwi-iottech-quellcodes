from lib.mongo.collection_name_generator import derive_collection_name


def test_derive_collection_name():
    assert derive_collection_name('iot-project/device/1/data/temperatures') == 'c_1_data_temperatures'