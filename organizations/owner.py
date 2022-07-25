import asyncio
import json

from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from .organization_mngt import OrganizationMngt
from .organizational_agent import OrganizationalAgent
from .rule import Rule


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Rule):
            return o.toJSON()
        return o


class MyDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if isinstance(o, Rule):
            return Rule.fromJSON(o)
        return o


class Owner(OrganizationalAgent):

    def __init__(self, jid: str, password: str, *args, **kwargs):
        super().__init__(jid, password, *args, **kwargs)

        self.organization = OrganizationMngt(str(self.jid.bare()), self)

        print("Agent owner starting . . .")
        self.organizational_behavior = self.OwnerOrganizationalBehaviour()
        self.organizational_inform_behavior = self.OwnerInformBehaviour()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(self.organizational_behavior)
        self.add_behaviour(self.organizational_inform_behavior)

    def add_behaviour(self, behaviour, template=None):
        super().add_behaviour(behaviour, template)

    class OwnerInformBehaviour(CyclicBehaviour):
        """
            Coroutine run cyclic.
        """

        async def run(self):
            print("Owner {} Inform Behaviour for send is running".format(self.agent.jid))

            if (self.agent.organization.need_updates):
                print("Update: The rganization needs to be updateds")
                msg_to_broadcast = Message()
                msg_to_broadcast.set_metadata("performative", "inform")
                msg_to_broadcast.set_metadata("inform", "update")
                msg_to_broadcast.body = json.dumps(
                    {"members": self.agent.organization.members, "rules": self.agent.organization.rules}, cls=MyEncoder)

                self.agent.send_to_everyone(msg_to_broadcast)
                self.agent.organization.need_updates = False
            await asyncio.sleep(0.5)

    class OwnerOrganizationalBehaviour(CyclicBehaviour):
        async def run(self):
            """
            Coroutine run cyclic.
            """

            print("Owner {} Organizational Behaviour for receive is running".format(self.agent.jid))
            msg = await self.receive(timeout=100)
            if (msg):
                if (("org_action", "join") in msg.metadata.items()):
                    # duda: preguntar a javi si aquí no tengo que revisar las reglas también 
                    # if(self.agent.check_rules(msg)):
                    dict = json.loads(msg.body)
                    jid = dict["jid"]
                    role = dict["role"]
                    self.agent.organization.add_member(jid, role)
                    # else: else: print("Attention!: Agent {} request '{}' failed because there is a rule that forbids the join".format(msg.sender, msg.metadata["org_action"]))
                elif (str(msg.sender.bare()) in self.agent.organization.members.keys()):
                    # print("The member who made the request is inside of the organization")
                    if (self.agent.check_rules(msg)):
                        if (("org_action", "add_rule") in msg.metadata.items()):
                            dict = json.loads(msg.body)
                            rule = Rule.fromJSON(dict["rule"])
                            self.agent.organization.add_rule(rule)
                        elif (("org_action", "add_member") in msg.metadata.items()):
                            dict = json.loads(msg.body)
                            jid = dict["jid"]
                            role = dict["role"]
                            self.agent.organization.add_member(jid, role)
                        elif (("org_action", "update_member") in msg.metadata.items()):
                            dict = json.loads(msg.body)
                            jid = dict["jid"]
                            role = dict["role"]
                            self.agent.organization.update_member(jid, role)
                        elif (("org_action", "remove_rule") in msg.metadata.items()):
                            dict = json.loads(msg.body)
                            rule = Rule.fromJSON(dict["rule"])
                            self.agent.organization.remove_rule(rule)
                        elif (("org_action", "remove_member") in msg.metadata.items()):
                            dict = json.loads(msg.body)
                            jid = dict["jid"]
                            if (jid == self.agent.organization.owner):
                                print("Attention!: The owner cannot be excluded from the organization")
                                return
                            self.agent.organization.remove_member(jid)

                        else:
                            print(
                                "Attention!: The owner is unable to process the message {} because he cannot recognize the metadata".format(
                                    msg))
                            return
                    else:
                        print("Attention!: Agent {} request '{}' failed because there is a rule that forbids the action".format(
                            msg.sender, msg.metadata["org_action"]))
                else:
                    print("Attention!: To request the owner you, {}, MUST be a member of the organization".format(msg.sender))
