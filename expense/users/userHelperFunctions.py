from expense.models import UsersModel

def userSerializer(user:UsersModel):
    userSerialized = { }
    userSerialized["id"] = user.id
    userSerialized["publicId"] = user.public_id
    userSerialized["name"] = user.name
    userSerialized["email"] = user.email
    userSerialized["created"] = user.created
    userSerialized["updated"] = user.updated
    return userSerialized
