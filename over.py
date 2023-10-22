from datetime import datetime
import random

table = {'우월': [10, 1,  10, [9.54,  10.94, 12.34, 13.75, 15.15, 16.55, 17.95, 19.35, 20.75, 22.15, 23.56, 24.96, 26.36, 27.76, 29.16]],
         '명중': [12, 11, 22, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '장탄': [12, 23, 34, [27.84, 31.95, 36.06, 40.17, 44.28, 48.39, 52.50, 56.50, 60.71, 64.82, 68.93, 73.04, 77.15, 81.26, 85.37]],
         '공증': [10, 35, 44, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '차뎀': [12, 45, 56, [4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]],
         '차속': [12, 57, 68, [1.98,  2.28,  2.57,  2.86,  3.16,  3.45,  3.75,  4.04,  4.33,  4.63,  4.92,  5.21,  5.51,  5.80,  6.09 ]],
         '크뎀': [12, 69, 80, [6.64,  7.62,  8.60,  9.58,  10.56, 11.54, 12.52, 13.50, 14.48, 15.46, 16.44, 17.42, 18.40, 19.38, 20.36]],
         '크확': [10, 81, 90, [2.30,  2.64,  2.98,  3.32,  3.66,  4.00,  4.35,  4.69,  5.03,  5.37,  5.70,  6.05,  6.39,  6.73,  7.07 ]],
         '방어': [10, 91, 100,[4.77,  5.47,  6.18,  6.88,  7.59,  8.29,  9.00,  9.70,  10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63]]}
         

abbr = {'홍': '홍련', '모': '모더니아', '앨': '앨리스', '백': '백설', '맥':'맥스웰', '누': '누아르', '도': '도로시', '순': '수니스', '길':'길로틴', '투': '2B', '에': 'A2',
        '뚝': '뚝배기', '갑': '갑빠', '장': '장갑', '신': '신발',
        '우월': '우월코드 데미지 증가', '명중': '명중률 증가', '장탄': '최대 장탄수 증가', '공증': '공격력 증가', '차뎀': '차지 데미지 증가', '차속': '차지 속도 증가', 
        '크뎀': '크리티컬 데미지 증가', '크확': '크리티컬 확률 증가', '방어': '방어력 증가'
}

effective = {'홍' : ['우월', '공증', '장탄', '명중'],
             '모' : ['우월', '공증', '장탄', '크확'],
             '앨' : ['우월', '공증', '장탄', '차속'],
             '백' : ['우월', '공증', '크뎀', '차속'],
             '맥' : ['우월', '공증', '장탄', '차뎀'],
             '누' : ['우월', '공증', '장탄', '명중'],
             '도' : ['우월', '공증', '명중'],
             '순' : ['우월', '공증', '명중'],
             '길' : ['우월', '공증', '장탄'],
             '투' : ['우월', '공증', '크확', '크뎀'],
             '에' : ['우월', '공증', '차속'],
}

NIKKES = ['홍', '모', '앨', '맥', '백', '볼', '누', '도', '순', '길', '투', '에']
PIECES = ['뚝', '갑', '장', '신']

def clamp(num, min, max):
    return min if num < min else max if num > max else num

MODULE_MAX = 20
RECHARGE_SECONDS = 180
#RECHARGE_SECONDS = 5

class Option():
    def __init__(self, prob):
        self.prob = prob
        self.reset()

    def reset(self):
        self.lock = False
        self.effect = '효과 미획득'
        self.rate = 0.0
        self.idx  = 0

    def desc(self):
        out = ''
        if self.effect == '효과 미획득':
            out = '효과 미획득'
        else:
            out = '[%s] %.2f'%(abbr[self.effect], self.rate)+'%'+' (%dLv)'%(self.idx+1)
            if self.lock:
                out = out + ' #'

        return out+'\n'

    def score(self, nikke):
        if self.effect in effective[nikke]:
            return 20 + (self.idx+1)**1.62
        else:
            return 0

class Piece():
    def __init__(self, name):
        self.name = name
        self.options = []
        
        for p in [100, 50, 30]:
            option = Option(p)
            self.options.append(option)

    def reset(self):
        for o in self.options:
            o.reset()

    def over(self):
        for o in self.options:
            if o.lock == False:
                o.reset()

        for o in self.options:
            if o.lock == False:
                ret, o.effect  = self.roleOption(o.prob)
                if ret:
                    o.idx   = self.roleRatio()
                    o.rate  = table[o.effect][3][o.idx]

    def cali(self):
        for o in self.options:
            if o.lock == False and o.effect != '효과 미획득':
                o.idx   = self.roleRatio()
                o.rate  = table[o.effect][3][o.idx]

    def desc(self):
        out = ''
        for o in self.options:        
            out += o.desc()

        return out

    def alreadyHas(self, effect):
        for o in self.options:
            if o.effect == effect:
                return True

        return False
    
    def roleRatio(self):
        howProb = random.randint(0, 99)
        getIdx = 0
        if howProb < 60:
            getIdx = int(howProb/12)
        elif howProb < 95:
            getIdx = 5+int((howProb-60)/7)
        else:
            getIdx = 10+howProb-95

        return getIdx
    
    def roleOption(self, prob):
        if random.randint(1, 100) <= prob:
            while True:
                whichProb = random.randint(1, 100)
                for effect, v in table.items():
                    if whichProb >= v[1] and whichProb <= v[2]:
                        break

                if self.alreadyHas(effect) == False:
                    break

            return True, effect
        else:
            return False, '효과 미획득'
    
    def getLockedCount(self):
        ret = 0
        for o in self.options:
            if o.lock:
                ret += 1

        return ret

    def calcOverNeedModule(self):
        lockCount = self.getLockedCount()
        if lockCount == 1:
            return 2
        elif lockCount == 2:
            return 3
        else:
            return 1

    def calcLockNeedModule(self):
        lockCount = self.getLockedCount()
        if lockCount == 1:
            return 3
        else:
            return 2

    def unlock(self, index):
        self.options[index].lock = False

    def unlockEnable(self, index):
        if index < 0 or index > 2:
            return False, '1,2,3 만 해제 가능'

        return True, ''
        
    def lock(self, index):
        lockCount = self.getLockedCount()
        if lockCount >= 2:
            return False
        else:
            self.options[index].lock = True

    def lockEnable(self, index):
        lockCount = self.getLockedCount()
        if lockCount >= 2:
            return False, '2부위 이상 잠금 불가'
        elif index < 0 or index > 2:
            return False, '1,2,3 만 잠금 가능'
        elif self.options[index].effect == '효과 미획득':
            return False, '효과 미획득은 잠금 불가'

        return True, ''

    def score(self, nikke):
        s = 0
        for o in self.options:
            s += o.score(nikke)
        
        return s

class Nikke():
    def __init__(self, name):
        self.usedModule = 0
        self.name = name
        self.dPiece = {}
        for n in PIECES:
            self.dPiece[n] = Piece(n)

        self.curPiece = self.dPiece['뚝']

    def reset(self):
        self.usedModule = 0
        for n in PIECES:
            self.dPiece[n].reset()

    def useModule(self, moduleCount):
        self.usedModule += moduleCount

    def desc(self):
        return '%s에 사용한 커스텀 모듈수: %d \n'%(abbr[self.name], self.usedModule)

    def scoreInfo(self):
        return '옵션 획득 점수: %d - 모듈 사용수: %d = 비틱점수: %d \n'%(self.optionScore(), self.usedModule, self.score())

    def info(self):
        out = self.scoreInfo()
        out += self.desc()

        for n, p in self.dPiece.items():
            out += '<< %s >>'%abbr[n] + '\n'
            out += p.desc()

        return out

    def optionScore(self):
        s = 0
        for n, p in self.dPiece.items():
            s += p.score(self.name)
        return s

    def score(self):
        return self.optionScore() - self.usedModule

class Account():
    def __init__(self, nick):
        self.module = MODULE_MAX
        self.lastAccess = datetime.now()
        self.nick = nick

        self.dNikke = {}
        for n in NIKKES:
            self.dNikke[n] = Nikke(n)

        self.curNikke = self.dNikke['홍']

    def reset(self, nikke):
        self.dNikke[nikke].reset()
        return '%s 리셋 성공'%(abbr[nikke])

    def rechargeModule(self):
        self.module = clamp(self.module + int((datetime.now() - self.lastAccess).seconds/RECHARGE_SECONDS), 0, MODULE_MAX)

    def processModule(self, needModule):
        self.rechargeModule()
        
        if self.module >= needModule:
            self.lastAccess = datetime.now()
            self.module = self.module - needModule
            self.curNikke.useModule(needModule)
            return True, 0
        else:
            return False, RECHARGE_SECONDS-(datetime.now() - self.lastAccess).seconds
        
    def desc(self):
        return '남은 커스텀 모듈 갯수: %d'%(self.module)

    def over(self, isCali=False):
        needModule = self.curNikke.curPiece.calcOverNeedModule()
        success, timeToCharge = self.processModule(needModule)
        
        if success:
            if isCali:
                self.curNikke.curPiece.cali()
            else:
                self.curNikke.curPiece.over()

            out = '%s %s 오버 성공 \n'%(abbr[self.curNikke.name], abbr[self.curNikke.curPiece.name])
            out += self.curNikke.desc()
            out += self.curNikke.curPiece.desc()
            out += self.desc()
            return out
        else:
            return self.moduleMsg(timeToCharge)

    def moduleMsg(self, timeToCharge):
        return '커스텀 모듈 갯수가 부족합니다.\n커스텀 모듈은 %d분에 1개씩 최대 %d개 충전됩니다. 남은시간 %d초'%(RECHARGE_SECONDS/60, MODULE_MAX, timeToCharge)

    def lock(self, index):
        index -= 1
        success, msg = self.curNikke.curPiece.lockEnable(index)
        if success == False:
            return msg

        needModule = self.curNikke.curPiece.calcLockNeedModule()
        success, timeToCharge = self.processModule(needModule)
        
        if success:
            self.curNikke.curPiece.lock(index)
            out = '잠금 성공\n'
            out += self.curNikke.desc()
            out += self.curNikke.curPiece.desc()
            out += self.desc()
            return out
        else:
            return self.moduleMsg(timeToCharge)

    def unlock(self, index):
        index -= 1

        success, msg = self.curNikke.curPiece.unlockEnable(index)
        if success == False:
            return msg

        self.curNikke.curPiece.unlock(index)
        out = '잠금 해제 성공\n'
        out += self.curNikke.curPiece.desc()
        
        return out

    def changeCurNikkePiece(self, nikke, piece):
        self.curNikke = self.dNikke[nikke]
        self.curNikke.curPiece = self.curNikke.dPiece[piece]
        out = ' %s %s로 오버할 장비 변경\n'%(abbr[nikke], abbr[piece])
        out += self.curNikke.desc()
        out += self.curNikke.curPiece.desc()

        return out