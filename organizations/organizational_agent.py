from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SendMsgToEveryoneBehav(OneShotBehaviour):

    def __init__(self, msg, receivers_list):

        super().__init__()
        self.msg = msg
        self.receivers_list = receivers_list

    async def run(self):
        self.msg.sender = str(self.agent.jid.bare())
        for jid in self.receivers_list:
            if jid == str(self.agent.jid.bare()):
                continue
            self.msg.to = jid
            if self.agent.check_rules(self.msg):
                await self.send(self.msg)
                print("Msg send to {} content {}".format(self.msg.to, self.msg.body))
            else:
                print("Attention!: The message to {} was not sent because exist a rule thats forbids it".format(self.msg.to))


class OrganizationalAgent(Agent):

    def __init__(self, jid: str, password: str, *args, **kwargs):
        super().__init__(jid, password, *args, **kwargs)
        self.organization = None
        send_container = self.container.send

        async def rule_send(msg, behavior):
            if self.organization:
                if behavior.agent.check_rules(msg):
                    await send_container(msg, behavior)
                else:
                    print("Attention!: The message to {} was not sent because exist a rule thats forbids it".format(msg.to))
            else:
                await send_container(msg, behavior)

        self.container.send = rule_send
        print("Agent starting . . .")

    def check_rules(self, msg: Message):
        if self.organization:
            return self.organization.is_allowed(msg)
        return True

    def send_to_everyone(self, msg: Message, role: str = ""):
        if self.organization:
            if role != "":
                receivers_list = [k for k, v in self.organization.members.items() if v == role]
            else:
                receivers_list = list(self.organization.members.keys())

            print("receivers list", receivers_list)
            self.add_behaviour(SendMsgToEveryoneBehav(msg, receivers_list))
        else:
            print("Attention!: The agent is not in a organization")
