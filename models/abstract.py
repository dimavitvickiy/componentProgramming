class DBAbstraction:
    def get_list(self):
        raise NotImplementedError

    def get(self, entity_id):
        pass

    def update(self, entity_id, **kwargs):
        pass

    def delete(self, entity_id):
        pass

    def create(self, **kwargs):
        pass
