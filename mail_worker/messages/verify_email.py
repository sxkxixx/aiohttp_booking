from .abc import AbstractMessage, AbstractMessageData


class VerificationMessageData(AbstractMessageData):
    """Params for verification message"""

    verify_token: str


class VerificationMessage(AbstractMessage):
    """
    Schema of email verification message
    type: str
    message_data: {
        receiver: List or str,
        verify_token: str
    }
    """
    type: str = 'verify_email'
    message_data: VerificationMessageData
