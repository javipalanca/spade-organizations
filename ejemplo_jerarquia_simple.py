import asyncio
import time

import spade
from spade.message import Message
from spade.template import Template

from organizations.member import Member
from organizations.owner import Owner
from organizations.rule import Rule


class CheckOrganization(spade.behaviour.CyclicBehaviour):
    async def run(self):
        print(self.agent.organization.members)
        print(self.agent.organization.rules)
        await asyncio.sleep(1)


class Receive(spade.behaviour.CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=100)
        if msg:
            print("Message received: {}".format(msg))


class Send(spade.behaviour.OneShotBehaviour):
    def __init__(self, to, sender=None, body=None, metadata=None):
        super().__init__()
        self.to = to
        self.sender = sender
        self.body = body
        self.metadata = {"test": "jerarquía"}

    async def run(self):
        print("Agent {} is trying to send a message".format(self.agent.jid))
        msg = Message(to=self.to, sender=self.sender, body=self.body, metadata=self.metadata)
        await asyncio.sleep(3)
        await self.send(msg)


"""
Probando ejemplo de Jerarquía Simple

"""

owner_agent = Owner("monica_owner@10.10.1.43", password="MMC")
supervisor_1 = Member("monica_supervisor_1@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")
subordinado_1 = Member("monica_subordinado_1@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")
subordinado_2 = Member("monica_subordinado_2@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")
subordinado_3 = Member("monica_subordinado_3@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")

template = Template(metadata={"test": "jerarquía"})
supervisor_1.add_behaviour(Receive(), template)
subordinado_1.add_behaviour(Receive(), template)
subordinado_2.add_behaviour(Receive(), template)
subordinado_3.add_behaviour(Receive(), template)

owner_agent.start().result()
supervisor_1.start().result()
subordinado_1.start().result()
subordinado_2.start().result()
subordinado_3.start().result()

print(owner_agent.organization)
owner_agent.organization.add_member(member_jid="monica_supervisor_1@10.10.1.43", member_role="Supervisor")
owner_agent.organization.add_member(member_jid="monica_subordinado_1@10.10.1.43", member_role="Subordinado")
owner_agent.organization.add_member(member_jid="monica_subordinado_2@10.10.1.43", member_role="Subordinado")
subordinado_3.organization.join("Subordinado")

# solo pueden enviarse mensajes de supervisor a Subordinado
r1 = Rule("Subordinado", "Subordinado", None, None)
r2 = Rule("Subordinado", "Supervisor", None, None)

# los subordinados no pueden añadir ni actualizar miembros ni eliminar miembros
r3 = Rule("Subordinado", "Owner", {"performative": "request", "org_action": "add_member"}, None)
r4 = Rule("Subordinado", "Owner", {"performative": "request", "org_action": "update_member"}, None)
r5 = Rule("Subordinado", "Owner", {"performative": "request", "org_action": "remove_member"}, None)

# los subordinados no pueden añadir reglas ni eliminar reglas
r6 = Rule("Subordinado", "Owner", {"performative": "request", "org_action": "add_rule"}, None)
r7 = Rule("Subordinado", "Owner", {"performative": "request", "org_action": "remove_rule"}, None)

# los supervisores no pueden actualizar miembros
r8 = Rule("Supervisor", "Owner", {"performative": "request", "org_action": "update_member"}, None)
r9 = Rule("Supervisor", "Owner", {"performative": "request", "org_action": "add_member"}, None)

# los supervisores no pueden añadir miembros supervisores
# duda: preguntar a javi si esto está bien o si me puedo hacer algo más genérico con expresiones regulares?? o si no vale la pena a estas alturas
# r6 = Rule("Supervisor", "Owner", {"performative":"request", "org_action":"add_member"}, cualiquier jid role "Supervisor")


owner_agent.organization.add_rule(r1)
owner_agent.organization.add_rule(r2)
owner_agent.organization.add_rule(r3)
owner_agent.organization.add_rule(r4)
owner_agent.organization.add_rule(r5)
owner_agent.organization.add_rule(r6)
owner_agent.organization.add_rule(r7)
owner_agent.organization.add_rule(r8)
owner_agent.organization.add_rule(r9)

# duda: preguntar a javi por qué cuando es str no funciona y cuando es json.dumps sí
subordinado_1.organization.update_member("monica_subordinado_1@10.10.1.43", "Supervisor")

subordinado_4 = Member("monica_subordinado_4@10.10.1.43", password="MMC", organization_owner="monica_owner@10.10.1.43")
subordinado_4.start().result()
subordinado_1.organization.add_member("monica_subordinado_4@10.10.1.43", "Supervisor")

subordinado_1.organization.update_member("monica_subordinado_3@10.10.1.43", "Supervisor")

r10 = Rule("Supervisor", "Owner", None, None)
subordinado_2.organization.add_rule(r10)

subordinado_3.add_behaviour(Send(to="monica_owner@10.10.1.43"))
subordinado_3.add_behaviour(Send(to="monica_subordinado_2@10.10.1.43", body="estoy harto del jefe"))
subordinado_3.add_behaviour(Send(to="monica_supervisor_1@10.10.1.43", body="súbeme el sueldo"))
supervisor_1.add_behaviour(Send(to="monica_subordinado_2@10.10.1.43", body="TRABAJA!!!"))

while owner_agent.is_alive():
    time.sleep(1)
