from spade.behaviour import OneShotBehaviour

class SendMsgBehav(OneShotBehaviour):

    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg

    async def run(self):
        await self.send(self.msg)