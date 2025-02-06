from dataclasses import dataclass, field
from typing import Tuple, List


@dataclass
class CommandTriggers:
    navigation: List[str] = field(
        default_factory=lambda: ["navigate to", "go to", "open", "visit"]
    )
    search: List[str] = field(default_factory=lambda: ["search for", "search", "find"])
    tab: List[str] = field(
        default_factory=lambda: ["new tab", "open tab", "create tab"]
    )
    close: List[str] = field(default_factory=lambda: ["close tab"])
    stop: List[str] = field(
        default_factory=lambda: ["stop listening", "goodbye", "bye", "stop"]
    )
    youtube_search: List[str] = field(
        default_factory=lambda: ["youtube search", "search youtube", "find on youtube"]
    )


class CommandParser:
    def __init__(self):
        self.triggers = CommandTriggers()

    def normalize_command(self, command: str) -> Tuple[str, str]:
        """Returns (command_type, parameter)"""
        command = command.lower().strip()

        # YouTube search commands
        for trigger in self.triggers.youtube_search:
            if trigger in command:
                query = command.replace(trigger, "").strip()
                return "youtube_search", query

        # Navigation commands
        for trigger in self.triggers.navigation:
            if trigger in command:
                destination = command.replace(trigger, "").strip()
                return "navigation", destination

        # Search commands
        for trigger in self.triggers.search:
            if trigger in command:
                query = command.replace(trigger, "").strip()
                return "search", query

        # Tab management
        for trigger in self.triggers.tab:
            if trigger in command:
                return "new_tab", ""

        # Close tab
        for trigger in self.triggers.close:
            if trigger in command:
                return "close_tab", ""

        # Stop command
        for trigger in self.triggers.stop:
            if trigger in command:
                return "stop", ""

        return "unknown", command
