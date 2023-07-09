class CommentsRepository:
    def __init__(self):
        self.comments= []

    def get_all(self):
        return self.comments

    def get_one(self, comm_id):
        for comm in self.comments:
            if comm["id"] == comm_id:
                return comm
        return None

    def save(self, comm):
        if "id" not in comm or not comm["id"]:
            comm["id"] = self.get_next_id()
        self.comments.append(comm)
        return comm

    def get_next_id(self):
        return len(self.comments) + 1