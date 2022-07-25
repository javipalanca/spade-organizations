from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from .organization_proxy import OrganizationProxy
from .organizational_agent import OrganizationalAgent


class Member(OrganizationalAgent):

    def __init__(self, jid: str, password: str, organization_owner, *args, **kwargs):

        super().__init__(jid, password, *args, **kwargs)

        self.organization = OrganizationProxy(organization_owner, agent=self)

        print("Agent member starting . . .")
        self.organizational_behavior = self.MemberOrganizationalBehaviour()

        template1 = Template(metadata={"performative": "inform", "inform": "update"})
        template2 = Template(metadata={"performative": "inform", "org_action": "leave"})
        template = template1 | template2
        self.add_behaviour(self.organizational_behavior, template)

    class MemberOrganizationalBehaviour(CyclicBehaviour):

        async def run(self):
            """
            Coroutine run cyclic.
            
            Report organizational changes to all members of the organization 
            """
            print("Organizational Behaviour of agent {} for receive info is running".format(self.agent.jid))
            msg = await self.receive(timeout=100)
            if msg:
                print("Update: Message received with performative: {}".format(msg.metadata))
                print("Update: Message received with content: {}".format(msg.body))
                if "inform" in msg.metadata.keys() and msg.metadata["inform"] == "update":
                    self.agent.update_organization(msg)
                elif "org_action" in msg.metadata.keys() and msg.metadata["org_action"] == "leave":
                    self.agent.leave_org()

    def update_organization(self, msg: Message):
        if str(msg.sender.bare()) != self.organization.owner:
            print("Alert: The sender of the update message does not have the permissions to perform the inform action")
            return

        if msg.metadata["inform"] == "update":
            self.organization.update(msg.body)

    def leave_org(self):
        print("I {} have left the organization".format(self.jid))
        self.organizational_behavior.kill()
        self.organization = None
