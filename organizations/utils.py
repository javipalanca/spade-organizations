from spade.behaviour import OneShotBehaviour


class SendMsgBehav(OneShotBehaviour):

    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    async def run(self):
        await self.send(self.msg)
