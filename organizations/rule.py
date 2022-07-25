import json
import logging
from typing import Optional, Dict

from spade.template import BaseTemplate

logger = logging.getLogger("spade.Message")


class Rule(BaseTemplate):

    def __init__(self,
                 sender_role: Optional[str] = None,
                 reciever_role: Optional[str] = None,
                 metadata: Optional[dict] = None,
                 body: Optional[str] = None):

        self.__sender_role = sender_role
        self.__reciever_role = reciever_role
        self.__metadata = metadata
        self.__body = body

        # if all are null -> disallow
        if not (self.__reciever_role or self.__sender_role or self.__metadata or self.__body):
            raise Exception("Warning!:This rule {} is inconsistent".format(self))

        # check type errors
        if self.__sender_role and not isinstance(self.__sender_role, str):
            raise TypeError("Warning!: The sender_role MUST be a string")
        if self.__reciever_role and not isinstance(self.__reciever_role, str):
            raise TypeError("Warning!: The reciever_role MUST be a string")
        if self.__body and not isinstance(self.__body, str):
            raise TypeError("Warning!: The body MUST be a string")
        if (self.__metadata and not (isinstance(self.__metadata, dict)
                                     and all(isinstance(k, str) for k in self.__metadata.keys())
                                     and all(isinstance(v, str) for v in self.__metadata.values()))):
            raise TypeError("Warning!: The metadata MUST be a Dict[str,str]")

    @property
    def sender_role(self):
        return self.__sender_role

    @property
    def reciever_role(self):
        return self.__reciever_role

    @property
    def metadata(self):
        return self.__metadata

    @property
    def body(self):
        return self.__body

    def __eq__(self, other) -> bool:
        if self.__sender_role != other.sender_role:
            return False
        if self.__reciever_role != other.reciever_role:
            return False
        if self.__metadata != other.metadata:
            return False
        if self.__body != other.body:
            return False

        return True

    def toJSON(self):
        return {"sender_role": self.sender_role, "reciever_role": self.reciever_role, "metadata": self.metadata,
                "body": self.body}

    @staticmethod
    def fromJSON(json_dict: Dict):
        return Rule(**json_dict)

    def __str__(self):
        return json.dumps(self.toJSON())

    def match(self, sender_role, reciever_role, metadata, body):
        """
        means that the message and the rule match, 
        so the message that you are trying to send is NOT allowed.
        """
        if self.__reciever_role and reciever_role != self.__reciever_role:
            return False

        if self.__sender_role and sender_role != self.__sender_role:
            return False

        if self.__metadata and not self.match_metadata(metadata):
            return False

        if self.__body and body != self.__body:
            return False

        return True

    def match_metadata(self, metadata):
        if len(self.__metadata) != len(metadata):
            return False

        shared_items = {key: metadata[key] for key in metadata if
                        key in self.__metadata and metadata[key] == self.__metadata[key]}
        return len(shared_items) == len(metadata)
