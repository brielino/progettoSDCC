from boto3.dynamodb.conditions import Key, Attr


def read_items(table):
    items = table.scan(
        FilterExpression=Attr('Id').gte(0)
    )
    return items['Items']


def read_item(table, id_hospital):
    item = table.query(
        KeyConditionExpression=Key('Id').eq(id_hospital)
    )
    return item['Items']


def update_item(table, id_hospital, value):
    # value rappresenta se devo decrementare o incrementare
    # 0 decremento
    # 1 incremento
    item = read_item(table, id_hospital)
    if value == 0:
        item.__getitem__(0)['NumA'] = item.__getitem__(0)['NumA'] - 1
    else:
        item.__getitem__(0)['NumA'] = item.__getitem__(0)['NumA'] + 1
    na = item.__getitem__(0)['NumA']
    table.update_item(
        Key={'Id': id_hospital},
        UpdateExpression = 'SET NumA = :val1',
        ExpressionAttributeValues = {
            ':val1': na
        }
    )


