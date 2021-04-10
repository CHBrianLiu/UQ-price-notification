from typing import Dict, List, Optional, TypedDict


class MessageBase:
    type: str
    text: str


class EmojiInTextMessage(TypedDict):
    index: int
    productId: str
    emojiId: str


class TextMessage(MessageBase):
    emojis: Optional[List[EmojiInTextMessage]]

    def json(self) -> dict:
        encoded = {"type": self.type, "text": self.text}
        if self.emojis is not None:
            encoded.update({"emojis": self.emojis})
        return encoded


class ConfirmTemplateMessage(MessageBase):
    actions: List[Dict[str, str]]
