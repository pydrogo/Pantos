from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        'create_user': True,
        'edit_user': True,
        'create_group': True,
        'edit_group': True,
        'send_request_for_open_door': True,
        'add_camera': True,
        'edit_camera': True,
    }


class custom(AbstractUserRole):
    available_permissions = {
        'edit_user': True,
        'edit_group': True,
        'edit_camera': True,
    }


permision = [
    'create_user',
    'edit_user',
    'create_group',
    'edit_group',
    'send_request_for_change_camera_ip',
    'send_request_for_open_door',
]
