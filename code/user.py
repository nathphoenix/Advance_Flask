class User:
  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password
    # return super().__init__(*args, **kwargs)()