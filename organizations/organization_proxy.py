from pipes import Template
import string
from tokenize import String
from .owner import MyDecoder
from .rule import Rule
from aioxmpp import JID 
from typing import List
from typing import Dict
from spade.message import Message
from .organization import Organization
from .utils import SendMsgBehav
from spade.behaviour import OneShotBehaviour
import json
from typing import TYPE_CHECKING
if(TYPE_CHECKING): 
    from .member import Member


# class SendMsgBehav(OneShotBehaviour):

#     def __init__(self, msg, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.msg = msg

#     async def run(self):
#         await self.send(self.msg)
        
Rules = List[Rule] 
class OrganizationProxy(Organization):

    @property
    def members(self):
        return self.__members

    @property
    def rules(self):
        return self.__rules

    @property
    def owner(self):
        return self.__owner

    def __init__(self, owner, agent):
        self.__owner: JID = owner
        self.__agent: Member = agent
        self.__members: Dict[JID, str] = {}
        self.__rules: Rules = []
        

    def async_send(self, msg: Message):
        b = SendMsgBehav(msg)
        self.__agent.add_behaviour(b)

    def join(self, role):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"performative":"request", "org_action":"join"}
        msg.body = json.dumps({"jid":str(self.__agent.jid.bare()), "role":role})
        print("Request: The member {} wants to join to organization {} with role {}".format(self.__agent.jid, self.__owner, role))

        self.async_send(msg)

    def add_rule(self, rule:Rule):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"performative":"request", "org_action":"add_rule"}
        msg.body = json.dumps({"rule":rule.toJSON()})
        print("Request: The member {} wants to add the rule {}".format(self.__agent.jid, rule))

        self.async_send(msg)

    def add_member(self, member_jid: str, member_role: str):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"performative":"request", "org_action":"add_member"}
        msg.body = json.dumps({"jid":member_jid, "role":member_role})
        print("Request: The member {} wants to add the member {}".format(self.__agent.jid, member_jid))

        self.async_send(msg)

    def update_member(self, member_jid: str, member_role: str):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"performative":"request", "org_action":"update_member"}
        msg.body = json.dumps({"jid":member_jid, "role":member_role})
        print("Request: The member {} wants to udapte the member {} to {}".format(self.__agent.jid, member_jid, member_role))

        self.async_send(msg)

    def remove_rule(self, rule:Rule):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"org_action":"remove_rule"}
        msg.body = json.dumps({"rule": rule.toJSON()})
        print("Request: The member {} wants to delete the rule {}".format(self.__agent.jid, rule))

        self.async_send(msg)

    def remove_member(self, member_jid: str):
        msg = Message(sender=str(self.__agent.jid.bare()), to=self.__owner)
        msg.metadata = {"org_action":"remove_member"}
        msg.body = json.dumps({"jid":member_jid})
        print("Request: The member {} wants to delete the member {}".format(self.__agent.jid, member_jid))

        self.async_send(msg)

    def update(self, body: String):
        try:
            dict = json.loads(body, cls=MyDecoder)
            rules = [Rule.fromJSON(rule) for rule in dict["rules"]]
            self.__rules = rules # Copy existing rules
            members = dict["members"]
            self.__members = members # Copy existing members
            print("Update: Update for {} successfully completed!!!".format(self.__agent.jid))
        except ValueError: 
            print('Attention!: Decoding JSON has failed when informing about an update')
        


    