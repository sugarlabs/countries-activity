# pages.py
import utils
import g
import buttons


class Pages:
    def __init__(self):
        self.current = None
        self.img = None
        self.xy = (g.sx(0), g.sy(.1))
        self.textxy = (g.sx(1), g.sy(20))

    def draw(self):
        g.screen.fill((100, 0, 100))
        if self.current is None:
            self.current = 1
        if self.img is None:
            file1 = str(self.current) + '.png'
            self.img = utils.load_image(file1, False, 'pages')
        g.screen.blit(self.img, self.xy)
        buttons.on(('fd', 'bk'))
        if self.current == 1:
            buttons.off('bk')
        if self.current == 10:
            buttons.off('fd')
        s = 'The Flags of the World page ' + str(self.current)
        utils.text_blit1(g.screen, s, g.font1, self.textxy, utils.CREAM, False)

    def fd(self):
        self.current += 1
        self.img = None

    def bk(self):
        self.current -= 1
        self.img = None

    def which(self):
        page = 1
        ind = 0
        while page < self.current:
            nr = 4
            if page == 6:
                nr = 3
            for r in range(nr):
                for c in range(6):
                    ind += 1
            page += 1
        y = 0
        dx = g.sy(32) / 6
        dy = g.sy(18.5) / 4
        nr = 4
        if page == 6:
            nr = 3
        for r in range(nr):
            x = g.sx(0)
            for c in range(6):
                if utils.mouse_in(x, y, x + dx, y + dy):
                    country = g.countries[ind][0]
                    return country
                x += dx
                ind += 1
                if ind == len(g.countries):
                    return None
            y += dy
        return None
