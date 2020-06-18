# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
        EnumTypeDebugLinkShowTextStyle = Literal[0, 1, 2, 3, 4, 5, 6]
    except ImportError:
        pass


class DebugLinkShowTextItem(p.MessageType):

    def __init__(
        self,
        style: EnumTypeDebugLinkShowTextStyle = None,
        content: str = None,
    ) -> None:
        self.style = style
        self.content = content

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('style', p.EnumType("DebugLinkShowTextStyle", (0, 1, 2, 3, 4, 5, 6)), 0),
            2: ('content', p.UnicodeType, 0),
        }
