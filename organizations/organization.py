from abc import ABCMeta
from typing import List, Dict

from aioxmpp import JID
from spade.message import Message

from .organizational_agent import OrganizationalAgent
from .rule import Rule

Rules = List[Rule]


class Organization(metaclass=ABCMeta):

    def __init__(self, owner, agent):
        self.__owner: str = owner
        self.__agent: OrganizationalAgent = agent
        self.__members: Dict[str, str] = {owner: "Owner"}
        self.__rules: Rules = []

    @property
    def members(self):
        return self.__members

    @property
    def rules(self):
        return self.__rules

    @property
    def agent(self):
        return self.__agent

    @property
    def owner(self):
        return self.__owner

    def __str__(self):
        return str(self.__dict__)

    def get_role(self, jid: str):
        role = self.members[jid]
        return role

    def is_allowed(self, msg: Message):
        for r in self.rules:
            if r.match(self.get_role(str(msg.sender.bare())), self.get_role(str(msg.to.bare())), msg.metadata, msg.body):
                return False
        return True

    def add_rule(self, r: Rule):
        # add a rule to Rules,
        # only the owner can add rules, members have to send a message to the owner asking him to add a rule
        raise NotImplementedError

    def add_member(self, member_jid: JID, member_role: str):
        # add a member to members,
        # only the owner can add members, members have to send a message to the owner asking him to add a member
        raise NotImplementedError

    def update_member(self, member_jid: JID, member_role: str):
        # update a member rol in members,
        # only the owner can update members roles, members have to send a message to the owner asking him to update a member role
        raise NotImplementedError

    def remove_rule(self, r: Rule):
        # remove a rule from Rules,
        # only the owner can remove rules, members have to send a message to the owner asking him to remove a rule
        raise NotImplementedError

    def remove_member(self, member_jid: JID):
        # remove a member from members,
        # only the owner can remove members, members have to send a message to the owner asking him to remove a member
        raise NotImplementedError
