from typing import Iterable, List, Reversible, Tuple
import textwrap

from tcod import Console

import color


class Message:
    def __init__(self, text:str, fg: Tuple[int, int, int] = color.gray_85) -> None:
        self.plain_text = text
        self.fg = fg
        self.count = 1
    
    @property
    def full_text(self) -> str:
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []
    
    def add_message(
        self, text: str, fg: Tuple[int, int, int] = color.white, 
        *, stack: bool = True,
    ) -> None:
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))
    
    def render(
        self, console: Console, x: int, y: int, width: int, height: int,
    ) -> None:
        self.render_messages(console, x, y, width, height, self.messages)
    
    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        # Return a wrapped text message.
        for line in string.splitlines():
            yield from textwrap.wrap(line, width, expand_tabs = True)

    @classmethod
    def render_messages(
        cls,
        console: Console,
        x: int, y: int,
        width: int, height: int,
        messages: Reversible[Message],
    ) -> None:
        y_offest = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x, y + y_offest, line, fg = message.fg)
                y_offest -= 1
                if y_offest < 0:
                    return  # Ran out of space to print messages.
