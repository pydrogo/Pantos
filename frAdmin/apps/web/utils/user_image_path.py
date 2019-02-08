import uuid
import os


def get_user_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s" % (instance.user.username)
    full_unique_path = 'profile_pic/{0}'.format(instance.user.username)
    return os.path.join('fr_pics', full_unique_path)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    full_unique_path = 'dataset/{0}/{1}'.format(instance.user.user.username, filename)
    return os.path.join('fr_pics', full_unique_path)
