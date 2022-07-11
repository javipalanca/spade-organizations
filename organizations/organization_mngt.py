import string
from .rule import Rule
from aioxmpp import JID 
from typing import Iterable, List
from typing import Dict
from spade.message import Message
from .organization import Organization
from .utils import SendMsgBehav
from typing import TYPE_CHECKING
if(TYPE_CHECKING): 
    from .owner import Owner

Rules = List[Rule] 

class OrganizationMngt(Organization):

    def __init__(self, owner, agent):
        self.__owner: str = owner
        self.__members: Dict[str, str] = {owner: "Owner"}
        self.__rules: Rules = []
        self.agent: Owner = agent
        self.need_updates = False

    @property
    def members(self):
        return self.__members

    @property
    def rules(self):
        return self.__rules

    @property
    def owner(self):
        return self.__owner

    def add_rule(self, rule:Rule):
        self.__rules.append(rule)
        print("Org Action: The rule {} was successfully added".format(rule))
        self.need_updates = True


    def add_member(self, member_jid: str, member_role: str):
        self.__members.update({member_jid:member_role})
        print("Org Action: The member {} was successfully added".format({member_jid:member_role}))
        self.need_updates = True


    def update_member(self, member_jid: str, member_role: str):
        if(member_jid in self.__members):
            self.__members.update({member_jid:member_role})
            print("Org Action: The member {} was successfully updated".format({member_jid:member_role}))
            self.need_updates = True
        print("Attention!: Member {} cannot be updated because he does not belong to the organization".format(member_jid))


    def remove_rule(self, rule: Rule):
        self.__rules.remove(rule)
        print("Org Action: The rule {} was successfully deleted".format(rule))
        self.need_updates = True


    def remove_member(self, member_jid: str):
        # duda: preguntar a javi si esta es la forma correcta
        # if(self.__owner == member_jid):
        #     for(member in self.__members):
        #         self.__members.pop(member.key)
        #     for(rule in self.__rules):
        #         self.remove_rule(rule)
        #     del self.organization
        #     self.remove_behaviour(self.organizational_behavior)
        
        if(member_jid == self.__owner):
            print("Attention!: The owner cannot eliminate himself")

        if(member_jid in self.__members):
            exp_msg = Message(to = member_jid, metadata={"performative":"inform", "org_action":"leave"})
            self.agent.add_behaviour(SendMsgBehav(exp_msg))

            self.__members.pop(member_jid)
            print("Org Action: The member {} was successfully deleted".format(member_jid))
            self.need_updates = True
        else: print("Attention!: Member {} cannot be removed because he does not belong to the organization".format(member_jid))

    def destroy(self):
        self.agent.organization = None
        self.agent.organizational_behavior.kill()
        self.agent.organizational_inform_behavior.kill()

        for member_jid in list(self.__members):
            if(member_jid != self.__owner):
                self.remove_member(member_jid)

        print("The organization has been destroyed")


        

