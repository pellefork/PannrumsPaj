
from pyfcm import FCMNotification

fcm_server_key = "AAAAwj-EEQc:APA91bFcphgkhXVTdrPoFHK8UWNC1tH5DlK6t8oRaSVEFV-UhnE0h-z_S8EDuq161i5gV8BSlNUQD4NTbNexbkdBYQUwKyazMd4d8adLD5yUkC1i7hzxkHTsAPyHSCVC1s1stxHA6nbQ"

push_service = FCMNotification(api_key=fcm_server_key)

def fetch_devices(db, user):
    devices = db.child("DeviceTokens").get(user['idToken'])
    return devices

def notify_clients(message_title, message_body, db, user):
    client_list = []

    devices_response = fetch_devices(db, user)

    for device in devices_response.each():
        client_list.append(device.key())

    # print(*client_list, sep='\n')

    result = push_service.notify_multiple_devices(registration_ids=client_list, message_title=message_title, message_body=message_body)
    print(result)

# blabla

