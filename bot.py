import re
import pickle
import discord

import over


TOKEN = 'MTE0MzE0NjM3NzQwNTI3NjI3Mw.GZhA6a.2-lmFpbAOjYak9izAo9iSj1xJASrMMD8Lmxluo'

class MyClient(discord.Client):
    def loadAccount(self):
        try:
            with open('./account', 'rb') as f:
                print('load account')
                self.dAccount = pickle.load(f)
        except:
            print('account 파일 없음')

    def saveAccount(self):
        with open('./account', 'wb') as f:
            print('save account')
            pickle.dump(self.dAccount, f)

    def getTopAccount(self, nikke):
        topScore = -1
        topAccount = None
        for name, account in self.dAccount.items():
            curScore = account.dNikke[nikke].score()
            if curScore > topScore:
                topAccount = account
                topScore = curScore

        return topAccount

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        if hasattr(self, 'overCount') == False:
            self.overCount = 0
            self.dAccount = {}
            self.loadAccount()
        
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기"))
 
    async def on_message(self, message):
        if message.author == self.user:
            return
 
        ret = False
        for c in ['오버', '수치', '잠금', '해제', '비틱', '관리', '리셋']:
            if c in message.content:
                ret = True

        if ret == False:
            return

        print(message.author.name, message.author.display_name, message.content)
        if message.author.name not in self.dAccount:
            account = over.Account(message.author.display_name)
            self.dAccount[message.author.name] = account
        else:
            account = self.dAccount[message.author.name]

        cmd = re.sub(r'\s+', ' ', message.content.strip())
        cmdList = cmd.split(' ')
        print(cmdList)
        cmd = cmdList[0]
        
        answer = ''
        if len(cmdList) == 1 and cmd in ['오버', '수치']:
            self.overCount += 1
            if self.overCount%10 == 0:
                self.saveAccount()

            if cmd == '오버':
                answer = account.over()
            elif cmd == '수치':
                answer = account.over(True)
        elif len(cmdList) == 2:
            if cmd == '오버' and cmdList[1] in over.NIKKES:
                answer = account.dNikke[cmdList[1]].info()
            elif cmd == '리셋' and cmdList[1] in over.NIKKES:
                answer = account.reset(cmdList[1])
            elif cmd == '잠금' and cmdList[1].isdigit():
                answer = account.lock(int(cmdList[1]))
            elif cmd == '해제' and cmdList[1].isdigit():
                answer = account.unlock(int(cmdList[1]))
            elif cmd == '비틱' and cmdList[1] in over.NIKKES:
                if len(self.dAccount) > 0:
                    topAccount = self.getTopAccount(cmdList[1])
                    answer = '비틱 1위 계정 : %s \n'%(topAccount.nick)
                    answer += topAccount.dNikke[cmdList[1]].info()
                else:
                    answer = '아직 아무도 오버를 안했습니다.'
            elif cmd == '관리' and cmdList[1] == '저장' and message.author.name == 'murloc1217':
                self.saveAccount()
                answer = '저장 성공'
        elif len(cmdList) == 3:
            if cmd == '오버' and cmdList[1] in over.NIKKES and cmdList[2] in over.PIECES:
                answer = account.changeCurNikkePiece(cmdList[1], cmdList[2])
            elif cmd == '관리' and cmdList[1] == '리젠' and cmdList[2].isdigit() and message.author.name == 'murloc1217':
                over.RECHARGE_SECONDS = int(cmdList[2])

        if answer != '':
            await message.channel.send(answer)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)