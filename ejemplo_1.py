import asyncio
from spade.message import Message
import json
import spade
from organizations.owner import Owner
from organizations.member import Member
from organizations.organizational_agent import OrganizationalAgent
from organizations.rule import Rule
from organizations import rule
import time
import asyncio

class CheckOrganization(spade.behaviour.CyclicBehaviour):
    async def run(self):
        print(self.agent.organization.members)
        print(self.agent.organization.rules)
        await asyncio.sleep(1)

class Send(spade.behaviour.OneShotBehaviour):
    def __init__(self, to, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to = to

    async def run(self):
        print("{} está enviando un mensaje".format(self.agent.jid))
        msg = Message(to = self.to)
        await asyncio.sleep(3)
        await self.send(msg)

        
owner_agent = Owner("monica_owner@10.10.1.43", password="MMC")
member_1 = Member("monica_member_1@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")
member_2 = Member("monica_member_2@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")

owner_agent.start().result()
member_1.start().result()
member_2.start().result()

print(owner_agent.organization)
owner_agent.organization.add_member(member_jid="monica_member_1@10.10.1.43", member_role = "Empleado")
member_2.organization.join("Empleado")

r1 = Rule("Empleado", "Empleado", None, None)
r2 = Rule("Empleado", "Owner", None, None)
print(r1)
owner_agent.organization.add_rule(r1)
member_1.organization.add_rule(r2)

member_1.add_behaviour(Send(to="monica_member_2@10.10.1.43"))
member_1.add_behaviour(Send(to="monica_owner@10.10.1.43"))

# r2 = Rule("Empleado", "Owner", {"performative":"request", "org_action":"add_rule"})

# owner_agent.add_behaviour(CheckOrganization())
# member_1.add_behaviour(CheckOrganization())
# member_2.add_behaviour(CheckOrganization())

# owner_agent.start(auto_register=True).result()
# member_1.start(auto_register=True).result()
# member_2.start(auto_register=True).result()

while owner_agent.is_alive():
    time.sleep(1)