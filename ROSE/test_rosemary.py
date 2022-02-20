from rosemary import Item, update


def test_create_instance():
    item = Item('Bread', days_left=3, quality=5)
    if item.name != 'Bread':
        return False
    if item.days_left != 3:
        return False
    if item.quality != 5:
        return False
    return True


# DAYS LEFT
def test_update_days_left_normal():
    item = Item('Bread', days_left=3, quality=5)
    update(item)
    return item.days_left == 2


def test_update_days_left_diamond():
    item = Item('Diamond', days_left=3, quality=100)
    update(item)
    return item.days_left == 3


def test_update_days_left_tickets():
    item = Item('Tickets', days_left=3, quality=5)
    update(item)
    return item.days_left == 2


def test_update_days_left_brie():
    item = Item('Aged Brie', days_left=3, quality=5)
    update(item)
    return item.days_left == 2


# QUALITY
def test_update_quality_normal():
    item = Item('Bread', days_left=3, quality=5)
    update(item)
    return item.quality == 4


def test_update_quality_diamond():
    item = Item('Diamond', days_left=3, quality=100)
    update(item)
    return item.quality == 100


def test_update_quality_tickets():
    item = Item('Tickets', days_left=12, quality=5)
    for i in range(11):
        update(item)
    return item.quality == 29


def test_update_quality_tickets_over_ten():
    item = Item('Tickets', days_left=56, quality=5)
    update(item)
    return item.quality == 6


def test_update_quality_tickets_over_five():
    item = Item('Tickets', days_left=10, quality=5)
    update(item)
    return item.quality == 7


def test_update_quality_tickets_under_five():
    item = Item('Tickets', days_left=5, quality=5)
    update(item)
    return item.quality == 8


def test_update_quality_tickets_zero():
    item = Item('Tickets', days_left=0, quality=5)
    update(item)
    return item.quality == 0


def test_update_quality_tickets_over_zero():
    item = Item('Tickets', days_left=1, quality=5)
    update(item)
    return item.quality == 8


def test_update_quality_brie():
    item = Item('Aged Brie', days_left=3, quality=5)
    for i in range(3):
        update(item)
    return item.quality == 8


# quality megative days left
def test_update_quality_negative_normal():
    item = Item('Bread', days_left=0, quality=5)
    for i in range(2):
        update(item)
    return item.quality == 1


def test_upate_quality_negative_tickets():
    item = Item('Tickets', days_left=3, quality=5)
    for i in range(5):
        update(item)
    return item.quality == 0


def test_upate_quality_negative_brie():
    item = Item('Aged Brie', days_left=3, quality=5)
    for i in range(5):
        update(item)
    return item.quality == 10


#quality in interval
def test_quality_in_interval_normal():
    item = Item('Bread', days_left=0, quality=5)
    for i in range(4):
        update(item)
    return item.quality == 0


def test_quality_in_interval_brie():
    item = Item('Aged Brie', days_left=15, quality=45)
    for i in range(5):
        update(item)
    return item.quality == 50


def test_quality_in_interval_tickets():
    item = Item('Tickets', days_left=5, quality=45)
    for i in range(3):
        update(item)
    return item.quality == 50


def test_quality_in_interval_diamond():
    item = Item('Diamond', days_left=3, quality=100)
    for i in range(50):
        update(item)
    return item.quality == 100


# name unchanged
def test_name_unchanged_normal():
    item = Item('Bread', days_left=5, quality=45)
    for i in range(30):
        update(item)
    return item.name == 'Bread'


def test_name_unchanged_diamond():
    item = Item('Diamond', days_left=5, quality=100)
    for i in range(30):
        update(item)
    return item.name == 'Diamond'


def test_name_unchanged_tickets():
    item = Item('Tickets', days_left=5, quality=45)
    for i in range(30):
        update(item)
    return item.name == 'Tickets'


def test_name_unchanged_brie():
    item = Item('Aged Brie', days_left=5, quality=45)
    for i in range(30):
        update(item)
    return item.name == 'Aged Brie'


# returns none
def test_returns_none_normal():
    item = Item('Bread', days_left=3, quality=5)
    for i in range(5):
        if update(item) != None:
            return False
    return True


def test_returns_none_diamond():
    item = Item('Diamond', days_left=3, quality=100)
    for i in range(5):
        if update(item) != None:
            return False
    return True


def test_returns_none_tickets():
    item = Item('Tickets', days_left=3, quality=5)
    for i in range(5):
        if update(item) != None:
            return False
    return True
    

def test_returns_none_brie():
    item = Item('Aged Brie', days_left=3, quality=5)
    for i in range(5):
        if update(item) != None:
            return False
    return True
