"""Example implementation of OSRSSkillTrainer."""

from typing import List

from gaming_systems.osrs.skills.base_trainer import OSRSSkillTrainer, OSRSLocation


class DummySkillTrainer(OSRSSkillTrainer):
    """Trivial trainer used for documentation examples."""

    def can_train_at_location(self, location: OSRSLocation) -> bool:
        return True

    def get_training_locations(self) -> List[OSRSLocation]:
        return []

    def start_training(self, location: OSRSLocation) -> bool:
        self.is_training = True
        return True

    def stop_training(self) -> bool:
        self.is_training = False
        return True

    def perform_training_action(self) -> bool:
        self.actions_completed += 1
        return True
