from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str

    def serialize(self):
        return {'role': self.role, 'content': self.content}

    @classmethod
    def deserialize(cls, d):
        role = d['role']
        content = d['content']
        return cls(role, content)

    def __str__(self):
        return f"{self.content}"
