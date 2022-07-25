from typing import List

from spade.message import Message

from .organization import Organization
from .rule import Rule
from .utils import SendMsgBehav

Rules = List[Rule]


class OrganizationMngt(Organization):

    def __init__(self, owner, agent):
        super().__init__(owner, agent)
        self.need_updates = False

    def add_rule(self, rule: Rule):
        self.__rules.append(rule)
        print("Org Action: The rule {} was successfully added".format(rule))
        self.need_updates = True

    def add_member(self, member_jid: str, member_role: str):
        self.__members.update({member_jid: member_role})
        print("Org Action: The member {} was successfully added".format({member_jid: member_role}))
        self.need_updates = True

    def update_member(self, member_jid: str, member_role: str):
        if member_jid in self.__members:
            self.__members.update({member_jid: member_role})
            print("Org Action: The member {} was successfully updated".format({member_jid: member_role}))
            self.need_updates = True
        print("Attention!: Member {} cannot be updated because he does not belong to the organization".format(member_jid))

    def remove_rule(self, rule: Rule):
        self.__rules.remove(rule)
        print("Org Action: The rule {} was successfully deleted".format(rule))
        self.need_updates = True

    def remove_member(self, member_jid: str):
        if member_jid == self.__owner:
            print("Attention!: The owner cannot eliminate himself")

        if member_jid in self.__members:
            exp_msg = Message(to=member_jid, metadata={"performative": "inform", "org_action": "leave"})
            self.agent.add_behaviour(SendMsgBehav(exp_msg))

            self.__members.pop(member_jid)
            print("Org Action: The member {} was successfully deleted".format(member_jid))
            self.need_updates = True
        else:
            print("Attention!: Member {} cannot be removed because he does not belong to the organization".format(member_jid))

    def destroy(self):
        self.agent.organization = None
        self.agent.organizational_behavior.kill()
        self.agent.organizational_inform_behavior.kill()

        for member_jid in list(self.__members):
            if member_jid != self.__owner:
                self.remove_member(member_jid)

        print("The organization has been destroyed")
