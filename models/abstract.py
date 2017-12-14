

class AbstractModel:
    @classmethod
    def get_list(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def update(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def delete(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_entity(cls, *args, **kwargs):
        raise NotImplementedError
