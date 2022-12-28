from pytest import fixture
from app import *





@fixture()
def initial_setup():
    """ creates 2 stores and 2 items per each store"""
    stores= {
    "23dec3da05f2446bb10a82e00bca6f58":{
        "id": "23dec3da05f2446bb10a82e00bca6f58","name": "My Store1"},
    "5aee83cfd62a4bd7a77b4d6c366980b4":{
		"id": "5aee83cfd62a4bd7a77b4d6c366980b4",
		"name": "My Store2"},
	}

    items={
        "97c5c22585f44fdbaca723f1d04cbf81":{
            "id": "97c5c22585f44fdbaca723f1d04cbf81",
            "name": "Chair2",
            "price": 15.99,
            "store_id": "5aee83cfd62a4bd7a77b4d6c366980b4"
        },
        "49d11a28d9aa42278b80cd4dfb77204a":	{
            "id": "49d11a28d9aa42278b80cd4dfb77204a",
            "name": "Chair1",
            "price": 15.99,
            "store_id": "5aee83cfd62a4bd7a77b4d6c366980b4"
        },
        "dbe2775d0fd84cd7b3c2b28cfae33de1":{
            "id": "dbe2775d0fd84cd7b3c2b28cfae33de1",
            "name": "Chair1",
            "price": 15.99,
            "store_id": "23dec3da05f2446bb10a82e00bca6f58"
        },
        "c871488b1b2246fd8d2042a180e3765a":{
            "id": "c871488b1b2246fd8d2042a180e3765a",
            "name": "Chair2",
            "price": 15.99,
            "store_id": "23dec3da05f2446bb10a82e00bca6f58"
        }
        
    }
    
    
def test_create_store():
    pass