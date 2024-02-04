# ctry.py
import utils
import g
import os
import pygame

# x centre, y bottom on 1200x900 screen
letters_c = [(600, 86), (720, 96), (832, 127), (932, 177), (1011, 241), (1068, 318), (1096, 403), (1096, 489), (1068, 574), (1011, 651), (932, 715), (832, 765),
             (720, 796), (600, 806), (480, 796), (368, 765), (268, 715), (189, 651), (132, 574), (104, 489), (104, 403), (132, 318), (189, 241), (268, 177), (368, 127), (480, 96)]


class AZ:
    def __init__(self, l, x1, y1, x2, y2):
        self.l = l
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Ctry:
    def __init__(self):
        # oval letters
        self.azs = []
        self.dup_countries = []
        s = g.sy(1.1)
        dx = g.xy0[0]
        dy = g.sy(.5)
        for ind in range(26):
            l = chr(ind + 97)
            x, y = letters_c[ind]
            y2 = int(g.imgf * y + g.sy(.1) + .5)
            y1 = y2 - s - s
            x = int(g.imgf * x + dx + .5)
            az = AZ(l, x - s, y1, x + s, y2)
            self.azs.append(az)
        # user input
        self.answer = ''
        self.cxy = (g.sx(16), g.sy(16))
        self.message = None
        self.message_c = (g.sx(16), g.sy(11))
        fname = os.path.join('data', 'countries.txt')
        f = open(fname, 'r')
        self.countries = []
        letters = ''
        for line in f.readlines():
            ch = line[:1]
            if ch not in letters:
                letters += ch
            self.countries.append(line.rstrip().split(','))
        self.no = []
        for i in range(ord('A'), ord('Z') + 1):
            ch = chr(i)
            if ch not in letters:
                self.no.append(ch)
        f.close()
        self.setup()
        self.finished = False
        g.countries = self.countries
        # Create another list of countries for easier comparision
        for c in self.countries:
            for w in c:
                self.dup_countries.append(w)
        
        self.correct_ans_sound = pygame.mixer.Sound("data/sounds/correctans.ogg")
        self.wrong_ans_sound = pygame.mixer.Sound("data/sounds/wrongans.ogg")


    def setup(self):
        g.answers = [''] * 26
        g.bgd = utils.load_image('bgd.png', False)
        for ch in self.no:
            g.answers[ord(ch) - 65] = 'none'
            text(ch, 'none')
        g.pic = g.globe
        self.clear()

    def redraw(self):
        g.bgd = utils.load_image('bgd.png', False)
        for answer in g.answers:
            if answer not in ('', 'none'):
                letter = answer[:1]
                text(letter, answer)
        for ch in self.no:
            text(ch, 'none')

    def draw(self):
        utils.text_blit(
            g.screen,
            self.answer,
            g.font2,
            self.cxy,
            utils.BLUE,
            False)

    def clear(self):
        self.answer = ''
        self.message = None

    def which_oval(self):
        for ind in range(26):
            az = self.azs[ind]
            if utils.mouse_in(az.x1, az.y1, az.x2, az.y2):
                return az.l
        return None

    def do_letter(self, l):
        ln = len(self.answer)
        if l == '*':
            if ln > 0:
                self.answer = self.answer[:ln - 1]
        else:
            if ln == 0:
                self.answer += l.upper()
            elif self.answer[ln - 1:] in ('-', ' '):
                self.answer += l.upper()
            else:
                self.answer += l

    def try1(self):
        if len(self.answer) == 0:
            self.message = 'Please type in a country'
            return -1
        l = self.answer[:1]
        ind = ord(l) - 65
        answer_fix = fix(self.answer)
        value, ans = self.check(answer_fix)
        if ans is None or value == -1:
            self.message = 'Sorry, ' + self.answer + ' is not in my list'
            self.wrong_ans_sound.play()
            return -1
        if value == 0:
            self.message = 'Did you mean ' + ans + '? (y/n)'
            return 0
        if g.answers[ind] != '':
            g.answers[ind] = ''
            self.redraw()
        self.message = "Correct, you got it right"
        self.correct_ans_sound.play()
        g.answers[ind] = ans
        self.flag(ans)
        text(l, answer_fix)
        self.answer = ''
        return -1

    def check(self, ans):
        flag = 0
        for lst in self.countries:
            if ans in lst:
                flag = 1
                return 1, lst[0]
        if flag == 0:
            return self.check_similar(ans)

    def check_similar(self, ans):
        # REFERENCE:- https://norvig.com/spell-correct.html
        def edits_one(word):
            letters = 'abcdefghijklmnopqrstuvwxyz '
            splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]
            return list(deletes + replaces + inserts)

        def edits_two(word):
            return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))

        def ref_countries(words):
            match = list()
            for w in words:
                if(w in self.dup_countries):
                    match.append(w)
            return match

        def possible_countries(word):
            return (ref_countries([word]) or ref_countries(edits_one(word))
                   or ref_countries(edits_two(word)))

        def prediction(word):
            pred = possible_countries(word)
            if(len(pred) != 0):
                return 0, pred[0]
            else:
                return -1, None

        return prediction(ans)

    def get_ind(self, ans):
        ind = 0
        for lst in self.countries:
            if ans in lst:
                return ind
            ind += 1
        return -1

    def flag(self, ans):
        ind = self.get_ind(ans)
        fname = os.path.join('data', 'flags', str(ind) + '.png')
        try:
            img = pygame.image.load(fname)
        except BaseException:
            return
        if ans == 'Nepal':
            img = img.convert_alpha()
        else:
            img = img.convert()
        if abs(g.imgf - 1.0) > .1:  # only scale if factor <> 1
            w = img.get_width()
            h = img.get_height()
            try:
                img = pygame.transform.smoothscale(
                    img, (int(g.imgf * w), int(g.imgf * h)))
            except BaseException:
                img = pygame.transform.scale(
                    img, (int(g.imgf * w), int(g.imgf * h)))
        g.pic = img

    def complete(self):
        if self.finished:
            return True
        for answer in g.answers:
            if answer == '':
                return False
        self.finished = True
        return True


def text(letter, string):  # eg ctry.text('A','Austria')
    font = g.font1
    if len(string) > 14:
        font = g.font0
    txt = font.render(' ' + string + ' ', True, utils.BLACK, utils.CYAN)
    w = txt.get_width()
    h = txt.get_height()
    ind = ord(letter) - 65
    x, y = letters_c[ind]
    x = int(g.imgf * x + .5)
    y = int(g.imgf * y + .5) - g.sy(1.3)
    x -= int(w / 2)
    if letter == 'A':
        y -= g.sy(.5)
    if letter == 'N':
        y += g.sy(.55)
    txt.set_alpha(120)
    g.bgd.blit(txt, (x, y))


def fix(s0):  # replace And with and
    s = s0.replace(' And ', ' and ')
    s = s.replace(' The ', ' the ')
    s = s.replace(' Of ', ' of ')
    if s == 'Usa':
        s = 'USA'
    if s == 'Uk':
        s = 'UK'
    return s
