import string
from typing_extensions import Self

from organizations.organizational_agent import SendMsgToEveryoneBehav
from .rule import Rule
from aioxmpp import JID 
from typing import Iterable, List
from typing import Dict
from spade.message import Message

Rules = List[Rule] 

class Organization:

    def __init__(self) -> None:
        self.__members = {}
        self.__owner = None
        self.__rules = []

    def __str__(self):
        return str(self.__dict__)

    @property
    def members(self):
        return self.__members

    @property
    def rules(self):
        return self.__rules

    @property
    def owner(self):
        return self.__owner

    def get_role(self, jid:str):
        role = self.members[jid]
        return role

    def is_allowed(self, msg: Message):
        for r in self.rules:
            # print("Checking the rule: {}".format(r))
            if(r.match(self.get_role(str(msg.sender.bare())), self.get_role(str(msg.to.bare())), msg.metadata, msg.body)):
                return False
        return True

    def add_rule(self, r: Rule):
        # add a rule to Rules,
        # only the owner can add rules, members have to send a message to the owner asking him to add a rule
        pass

    def add_member(self, member_jid: JID, member_role: str):
        # add a member to members,
        # only the owner can add members, members have to send a message to the owner asking him to add a member
        pass

    def update_member(self, member_jid: JID, member_role: str):
        # update a member rol in members,
        # only the owner can update members roles, members have to send a message to the owner asking him to update a member role
        pass

    def remove_rule(self, r: Rule):
        # remove a rule from Rules,
        # only the owner can remove rules, members have to send a message to the owner asking him to remove a rule
        pass

    def remove_member(self, member_jid: JID):
        # remove a member from members,
        # only the owner can remove members, members have to send a message to the owner asking him to remove a member
        pass

    



    


