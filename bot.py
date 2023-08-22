import time
from datetime import datetime
import discord
 
TOKEN = 'MTE0MzE0NjM3NzQwNTI3NjI3Mw.GZhA6a.2-lmFpbAOjYak9izAo9iSj1xJASrMMD8Lmxluo'
 
table = {'우월코드 데미지 증가': [10, 1,  10, [9.54,  10.94, 12.34, 13.75, 15.15, 16.55, 17.95, 19.35, 20.75, 22.15, 23.56, 24.96, 26.36, 27.76, 29.16]],
         '명중률 증가':          [12, 11, 22, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '최대 장탄수 증가':     [12, 23, 34, [27.84, 31.95, 36.06, 40.17, 44.28, 48.39, 52.50, 56.50, 60.71, 64.82, 68.93, 73.04, 77.15, 81.26, 85.37]],
         '공격력 증가':         [10, 35, 44, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '차지 데미지 증가':    [12, 45, 56, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '차지 속도 증가':      [12, 57, 68, [1.98,  2.28,  2.57,  2.86,  3.16,  3.45,  3.75,  4.04,  4.33,  4.63,  4.92,  5.21,  5.51,  5.80,  6.09 ]],
         '크리티컬 데미지 증가': [12, 69, 80, [6.64,  7.62,  8.60,  9.58,  10.56, 11.54, 12.52, 13.50, 14.48, 15.46, 16.44, 17.42, 18.40, 19.38, 20.36]],
         '크리티컬 확률 증가':   [10, 81, 90, [2.30,  2.64,  2.98,  3.32,  3.66,  4.00,  4.35,  4.69,  5.03,  5.37,  5.70,  6.05,  6.39,  6.73,  7.07 ]],
         '방어력 증가':          [10, 91, 100,[4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]]}
         
import random, sys
from operator import itemgetter, attrgetter

def getRatioIndex():
    howProb = random.randint(0, 99)
    getIdx = 0
    if howProb < 60:
        getIdx = int(howProb/12)
    elif howProb < 95:
        getIdx = 5+int((howProb-60)/7)
    else:
        getIdx = 10+howProb-95

    return getIdx

def getOption(prob, obtained):
    if random.randint(1, 100) <= prob:
        while True:
            whichProb = random.randint(1, 100)            
            for k, v in table.items():
                if whichProb >= v[1] and whichProb <= v[2]:
                    break

            if k not in obtained:
                break
            
        idx = getRatioIndex()
        ratio = v[3][idx]
        obtained.append(k)
        return obtained, k, ratio, idx
    else:
        obtained.append('효과 미획득')
        return obtained, '효과 미획득', -1, -1

dUserModule = {}
dUserObtained = {}
dUserLastAccess = {}

def clamp(num, min, max):
    return min if num < min else max if num > max else num

def processModulel(account):
    if account not in dUserModule:
        dUserModule[account] = 10
    else:
        dUserModule[account] = clamp(dUserModule[account] + int((datetime.now() - dUserLastAccess[account]).seconds/60), 0, 10)
    
    if dUserModule[account] > 0:
        dUserLastAccess[account] = datetime.now()
        dUserModule[account] = dUserModule[account]-1
        return True, 0
    else:
        return False, 60-(datetime.now() - dUserLastAccess[account]).seconds

def over(account):
    success, timeToCharge = processModulel(account)
    if success:
        out = ''
        obtained = []
        for prob in [100, 50, 30]:
            obtained, name, ratio, idx = getOption(prob, obtained)
            if name == '효과 미획득':
                out += name+'\n'
            else:
                out += '[%s] %.2f'%(name, ratio)+'%'+' (%dLv)'%(idx+1)+'\n'

        dUserObtained[account] = obtained
        #out += '------------------------------\n'
        out += '남은 커스텀 모듈 갯수: %d'%(dUserModule[account])
        return out
    else:
        return '커스텀 모듈 갯수가 부족합니다.\n커스텀 모듈은 1분에 1개씩 충전됩니다. 남은시간 %d초'%(timeToCharge)

def cali(account):
    if account in dUserObtained:    
        success, timeToCharge = processModulel(account)
        if success:
            out = ''
            obtained = dUserObtained[account]
            for name in obtained:
                if name == '효과 미획득':
                    out += name+'\n'
                else:
                    idx = getRatioIndex()
                    ratio = table[name][3][idx]
                    out += '[%s] %.2f'%(name, ratio)+'%'+' (%dLv)'%(idx+1)+'\n'

            #out += '------------------------------\n'
            out += '남은 커스텀 모듈 갯수: %d'%(dUserModule[account])
            return out
        else:
            return '커스텀 모듈 갯수가 부족합니다.\n커스텀 모듈은 1분에 1개씩 충전됩니다. 남은시간 %d초'%(timeToCharge)
    else:
        return '먼저 오버 명령어를 사용해서 오버로드를 해주세요.'


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기"))
 
    async def on_message(self, message):
        if message.author == self.user:
            return
 
        command = message.content.replace(" ", "")

        if command in ['오버', '수치']:
            print(message.author, command)
            if command == '오버':
                answer = over(message.author)
                await message.channel.send(answer)
            elif command == '수치':
                answer = cali(message.author)
                await message.channel.send(answer)
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)