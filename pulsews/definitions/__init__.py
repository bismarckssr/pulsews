from dataclasses import dataclass, field
from abc import abstractmethod
from typing import Callable, Any

@dataclass
class ActivateObject:
    path: list[str]
    value: str

# Defines the PulseHandler class. Used as the main class for handlers used during websocket messaging.
# Has the ability to run action.run() if activate_on string matches the received message.
@dataclass
class PulseHandler:
    activate_object: ActivateObject # Note: shall be the entire piece of message you are looking for (gotta change this)
    action: Callable[[str], str]
    is_triggered: Callable[[dict], bool] = field(init=False)


    # Recursive function to check if specified path exists in JSON, then compares to expected value. Returns True/False
    def _create_trigger(self, json_object: dict, current_index: int = 0):
        keys = list(json_object.keys()) #gather all keys in the JSON object
        local_path = self.activate_object.path # ["address", "street"]

        if len(local_path) == current_index + 1:
            final_value = json_object.get(keys[0]) # Uses .get to survive errors against non-existent keys. Arriving here means deepest stratus has been reached.
            return final_value == self.activate_object.value #a sto punto l'albero del json non ha più chiavi rimanenti. fine.

        for key in keys:
            if key == local_path[current_index]:
                current_index+=1
                return self._create_trigger(json_object[key], current_index=current_index)
        return False


    def __post_init__(self):
        self.is_triggered = self._create_trigger