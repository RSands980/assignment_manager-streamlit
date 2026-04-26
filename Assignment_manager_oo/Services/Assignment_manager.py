import uuid


class AssignmentManager:
    def __init__(self, initial_assignments: list[dict]) -> None:
        self._assignments = initial_assignments

    def all(self) -> list[dict]:
        return list(self._assignments)

    def add(self, title: str, description: str, points: int, assignment_type: str) -> dict:
        allowed_types = {"homework", "lab", "other"}
        if not title.strip():
            raise ValueError("Title is required.")
        if points < 0:
            raise ValueError("Points must be zero or greater.")
        if assignment_type.lower() not in allowed_types:
            raise ValueError("Assignment type is invalid.")

        new_assignment = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "points": points,
            "type": assignment_type.lower(),
        }
        self._assignments.append(new_assignment)
        return new_assignment

    def delete(self, assignment_id: str) -> None:
        for index, assignment in enumerate(self._assignments):
            if assignment.get("id") == assignment_id:
                del self._assignments[index]
                return
        raise ValueError("Assignment not found.")
