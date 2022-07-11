from tokenize import String
from typing import Container
from aioxmpp import JID 
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import OneShotBehaviour
import json
import re


class SendMsgToEveryoneBehav(OneShotBehaviour):

    def __init__(self, msg, receivers_list,  *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.msg = msg
        self.receivers_list = receivers_list

    async def run(self):
        self.msg.sender = str(self.agent.jid.bare())
        for jid in self.receivers_list:
            if(jid == str(self.agent.jid.bare())):
                continue
            self.msg.to = jid
            if(self.agent.check_rules(self.msg)):
                await self.send(self.msg)
                print("Msg send to {} content {}".format(self.msg.to, self.msg.body))
            else: print("Attention!: The message to {} was not sent because exist a rule thats forbids it".format(self.msg.to))


class OrganizationalAgent(Agent):

    def __init__(self, jid: str, password: str, *args, **kwargs):
        super().__init__(jid, password, *args, **kwargs)
        send_container = self.container.send
        
        async def rule_send(msg, behavior):
            if(self.organization):
                if(behavior.agent.check_rules(msg)):
                    await send_container(msg, behavior)
                else: print("Attention!: The message to {} was not sent because exist a rule thats forbids it".format(msg.to))
            else: await send_container(msg, behavior)

        self.container.send = rule_send
        print("Agent starting . . .")


    def check_rules(self, msg: Message):
        if(self.organization):
            return self.organization.is_allowed(msg)
        return True

    def send_to_everyone(self, msg: Message, role: str = ""):
        if (self.organization):
            if (role != ""): receivers_list = [k for k,v in self.organization.members.items() if v == role]
            else: receivers_list = list(self.organization.members.keys())

            print("receivers list", receivers_list)
            self.add_behaviour(SendMsgToEveryoneBehav(msg, receivers_list))
        else: 
            print("Attention!: The agent is not in a organization")


    # def loads_add_rule(self, msg: Message):
    #     dict = json.loads(msg.body)
    #     rule = dict["rule"]
    #     self.organization.internal_add_rule(rule)

    # def loads_add_member(self, msg: Message):
    #     dict = json.loads(msg.body)
    #     jid = dict["jid"]
    #     role = dict["role"]

    #     if(not self.is_valid_JID(jid)):
    #         raise Exception("Check JID of the member you are trying to add")
    #     self.organization.internal_add_member(jid, role)

    # def loads_update_member(self, msg: Message):
    #     dict = json.loads(msg.body)
    #     jid = dict["jid"]
    #     role = dict["role"]

    #     if(not self.is_valid_JID(jid)):
    #         raise Exception("Check JID of the member you are trying to add")
    #     self.organization.internal_update_member(jid, role)

    # def loads_remove_rule(self, msg: Message):
    #     dict = json.loads(msg.body)
    #     rule = dict["rule"]
    #     self.organization.internal_remove_rule(rule)
    
    # def loads_remove_rule(self, msg: Message):
    #     dict = json.loads(msg.body)
    #     rule = dict["rule"]
    #     self.organization.internal_remove_rule(rule)

    # def loads_remove_member(self, msg: Message):
    #     #duda: preguntar a javi por qué no llega hasta aquí cuando lo eliminan
    #     dict = json.loads(msg.body)
    #     jid = dict["jid"]
    #     if(not self.is_valid_JID(jid)):
    #         raise Exception("Check JID of the member you are trying to add")
    #     print(self.jid, type(self.jid))
    #     print(jidd, type(jid))
    #     if self.jid == jid:
    #         print("You {} have been removed from the organization".format(self.jid))
    #         del self.organization
    #         self.remove_behaviour(self.organizational_behavior)
        
    #     self.organization.internal_remove_member(jid)

    # def is_valid_JID(jid:str) -> bool: 
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     return re.search(regex, jid)
