

from GUI.Screens.Screen import Screen
from GUI.Screens.Screen import Screen
from GUI.State import State

class MenuScreen(Screen):
    def render(self, events) -> State:
        for event in events:
            pass

        return State.TWO_PLAYER