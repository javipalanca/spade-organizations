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

"""
Probando que un miembro elimine al owner:

"""
owner_agent = Owner("monica_owner@10.10.1.43", password="MMC")
member_1 = Member("monica_member_1@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")

owner_agent.start().result()
member_1.start().result()

owner_agent.organization.add_member(member_jid="monica_member_1@10.10.1.43", member_role = "Empleado")
print("Organization: ", owner_agent.organization)
member_1.organization.remove_member(member_jid="monica_owner@10.10.1.43")



while owner_agent.is_alive():
    time.sleep(1)