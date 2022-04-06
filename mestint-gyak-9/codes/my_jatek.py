from ast import literal_eval as make_tuple
import random


# KIEGESZITO FUGGVENYEK/OSZTALYOK
def update(x, **entries):
    """Asszociatív tömb, struct értékeinek frissítése."""
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


def cmp(a, b):
    return (a > b) - (a < b)


def if_(test, result, alternative):
    """Háromágú értékadás."""
    if test:
        if callable(result):
            return result()
        return result
    else:
        if callable(alternative):
            return alternative()
        return alternative


class Struct:
    """Pehelykönnyű osztály, metódusok nélkül."""

    def __init__(self, **entries):
        """Megadott attribútumok rögzítese."""
        self.__dict__.update(entries)

    def __repr__(self):
        """Megjeleníti a struktúrát."""
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)


def jatssz(jatek, *jatekosok):
    """n személyes, felváltva lépő játékmenet."""
    allapot = jatek.kezdo
    jatek.kiir(allapot)
    while True:
        for jatekos in jatekosok:
            lepes = jatekos(jatek, allapot)
            allapot = jatek.lep(lepes, allapot)
            jatek.kiir(allapot)
            if jatek.levele(allapot):
                return jatek.hasznossag(allapot, jatekosok[0])


def num_or_str(x):
    """Lehetőség szerint számmá alakít."""
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x).strip()


# KERESESEK
# Minimax keresés
def minimax(allapot, jatek):
    """Legjobb lépés meghatározása teljes kereséssel."""
    jatekos = jatek.kovetkezik(allapot)

    # definiáljuk a keresési fa egyes szintjein használatos címkézést.
    def max_ertek(allapot):
        if jatek.levele(allapot):
            return jatek.hasznossag(allapot, jatekos)
        return max([min_ertek(s) for (_, s) in jatek.rakovetkezo(allapot)])

    def min_ertek(allapot):
        if jatek.levele(allapot):
            return jatek.hasznossag(allapot, jatekos)
        return min([max_ertek(s) for (_, s) in jatek.rakovetkezo(allapot)])

    # minimax lényege
    fiai_ertekei = [(a, min_ertek(s)) for (a, s) in jatek.rakovetkezo(allapot)]
    lepes, ertek = max(fiai_ertekei, key=lambda a_s: a_s[1])
    return lepes


def alfabeta_kereses(allapot, jatek, d=4, levagas_teszt=None, kiertekel=None):
    """A játékfa keresése adott mélységig."""
    jatekos = jatek.kovetkezik(allapot)

    def max_ertek(allapot, alfa, beta, melyseg):
        if levagas_teszt(allapot, melyseg):
            return kiertekel(allapot)
        v = float("-inf")
        for (a, s) in jatek.rakovetkezo(allapot):
            v = max(v, min_ertek(s, alfa, beta, melyseg+1))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v

    def min_ertek(allapot, alfa, beta, melyseg):
        if levagas_teszt(allapot, melyseg):
            return kiertekel(allapot)
        v = float("inf")
        for (a, s) in jatek.rakovetkezo(allapot):
            v = min(v, max_ertek(s, alfa, beta, melyseg+1))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return v

    # Alfabéta keresés
    levagas_teszt = levagas_teszt or \
        (lambda allapot, melyseg: melyseg > d or jatek.levele(allapot))
    kiertekel = kiertekel or \
        (lambda allapot: jatek.hasznossag(allapot, jatekos))
    alfa = float("-inf")
    legjobb_lepes = None
    for a, s in jatek.rakovetkezo(allapot):
        v = min_ertek(s, alfa, float("inf"), 0)
        if v > alfa:
            alfa = v
            legjobb_lepes = a
    return legjobb_lepes


# JATEKOSOK
# Játékosok típusai
def kerdez_jatekos(jatek, allapot):
    """Felhasználói input."""
    return num_or_str(input('Mit lép? '))


def random_jatekos(jatek, allapot):
    """Véletlen választ a lehetőségek közül."""
    return random.choice(jatek.legalis_lepesek(allapot))


def alfabeta_jatekos(jatek, allapot):
    """Játékfában keres."""
    return alfabeta_kereses(allapot, jatek)


def minimax_jatekos(jatek, allapot):
    """Játékfában keres."""
    return minimax(allapot, jatek)


# JATEK ALAPOSZTALY
class Jatek:
    """Absztrakt osztály a játékok megadására."""

    def legalis_lepesek(self, allapot):
        """Adott állapotban megtehető lépések listája."""
        raise NotImplementedError()

    def lep(self, lepes, allapot):  # NOQA
        """Aktuális állapotban megtett lépés eredménye."""
        raise NotImplementedError

    def hasznossag(self, allapot, jatekos):
        """A játékos számára ekkora haszna volt (nyereség/veszteség)."""
        raise NotImplementedError()

    def levele(self, allapot):
        """A játékfa terminális csúcsa az állapot."""
        return not self.legalis_lepesek(allapot)

    def kovetkezik(self, allapot):
        """Soron következő játékos meghatározása."""
        return allapot.kovetkezik

    def kiir(self, allapot):
        """Az állás megmutatása."""
        print(allapot)

    def rakovetkezo(self, allapot):
        """Rákövetkező (lépés, állapot) párok listája."""
        return [(lepes, self.lep(lepes, allapot))
                for lepes in self.legalis_lepesek(allapot)]

    def __repr__(self):
        """Játék nevének kiírása."""
        return '<%s>' % self.__class__.__name__


# TIC-TAC TOE OSZTALY
class TicTacToe(Jatek):
    """Általánosított 3x3-as amőba."""

    def __init__(self, h=3, v=3, k=3):
        """Játék alapstrukturájának kialakítása."""
        update(self, h=h, v=v, k=k)
        lepesek = [(x, y) for x in range(1, h+1) for y in range(1, v+1)]
        self.kezdo = Struct(
            kovetkezik='X', eredmeny=0, tabla={}, lepesek=lepesek)

    def legalis_lepesek(self, allapot):
        """Minden üres mező lehetséges lépést jelent."""
        return allapot.lepesek

    def lep(self, lepes, allapot):
        """Lépés hatása."""
        if type(lepes) is str:
            lepes = make_tuple(lepes)
        if lepes not in allapot.lepesek:
            return allapot  # téves lépés volt
        tabla = allapot.tabla.copy()
        tabla[lepes] = allapot.kovetkezik
        lepesek = list(allapot.lepesek)
        lepesek.remove(lepes)
        return Struct(
            kovetkezik=if_(allapot.kovetkezik == 'X', 'O', 'X'),
            eredmeny=self.ertekel(tabla, lepes, allapot.kovetkezik),
            tabla=tabla, lepesek=lepesek)

    def hasznossag(self, allapot, jatekos):
        """X értékelése: 1, ha nyer; -1, ha veszít, 0 döntetlenért."""
        return if_(jatekos == "X", allapot.eredmeny, -allapot.eredmeny)

    def levele(self, allapot):
        """A nyert állás vagy a tele tábla a játék végét jelenti."""
        return allapot.eredmeny != 0 or len(allapot.lepesek) == 0

    def kiir(self, allapot):
        """Lássuk az aktuális állást."""
        tabla = allapot.tabla
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(tabla.get((x, y), '.'), end=" ")
            print()
        print(allapot.eredmeny)
        print()

    def ertekel(self, tabla, lepes, jatekos):
        """Ha X nyer ezzel a lépéssel, akkor 1, ha O, akkor -1, különben 0."""
        if (self.k_egy_sorban(tabla, lepes, jatekos, (0, 1)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, 0)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, -1)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, 1))):
            return if_(jatekos == 'X', +1, -1)
        else:
            return 0

    def k_egy_sorban(self, tabla, lepes, jatekos, irany):
        """Igaz, ha van a lépéstől adott irányba k azonos figura."""
        delta_x, delta_y = irany
        x, y = lepes
        n = 0
        while tabla.get((x, y)) == jatekos:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = lepes
        while tabla.get((x, y)) == jatekos:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1   # lépés duplán számolva
        return n >= self.k


def main():
    tto = TicTacToe()

    # Ket random jatekos egymas ellen
    # jatssz(tto, random_jatekos, random_jatekos)

    # X -> minimax_jatekos 0 -> random_jatekos
    # jatssz(tto, minimax_jatekos, random_jatekos)

    # X -> random_jatekos 0 -> minimax_jatekos
    # jatssz(tto, random_jatekos, minimax_jatekos)

    # X -> minimax_jatekos 0 -> minimax_jatekos
    # jatssz(tto, minimax_jatekos, minimax_jatekos)

    # X -> random_jatekos 0 -> alfabeta_jatekos
    # jatssz(tto, random_jatekos, alfabeta_jatekos)

    # X -> alfabeta_jatekos 0 -> random_jatekos
    # jatssz(tto, alfabeta_jatekos, random_jatekos)

    # X -> alfabeta_jatekos 0 -> alfabeta_jatekos
    # jatssz(tto, alfabeta_jatekos, alfabeta_jatekos)


if __name__ == '__main__':
    main()
