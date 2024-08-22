# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# --------------------------------------------------------------------------------------------------------


def fibonacci(maxelement):
    fibseries = []
    fibseries.append(0)
    fibseries.append(1)
    fibkminus2 = 0
    fibkminus1 = 1
    fibk = fibkminus2 + fibkminus1
    while fibk < maxelement:
        fibseries.append(fibk)
        fibkminus2 = fibkminus1
        fibkminus1 = fibk
        fibk = fibkminus2 + fibkminus1
    print(("fibonacci series:", fibseries))
    return fibseries


def fibsearch(iterable, query):
    fibseries = fibonacci(len(iterable) + 1)
    i = fibseries[len(fibseries)-1]
    p = fibseries[len(fibseries)-2]
    q = fibseries[len(fibseries)-3]
    exit = False
    while not exit:
        print(("i = ", i))
        print(("p = ", p))
        print(("q = ", q))
        try:
            if query < iterable[i-1]:
                print("query < iterable[i-1]")
                if q == 0:
                    print(("queried point does not exist:", query))
                    exit = True
                else:
                    i = (i - q)
                    tempp = p
                    p = q
                    q = (tempp - q)
            if query > iterable[i-1]:
                print("query > iterable[i-1]")
                if p == 1:
                    print(("queried point does not exist:", query))
                    exit = True
                else:
                    i = i + q
                    tempp = p
                    p = (tempp - q)
                    q = (q - p)
            if query == iterable[i-1]:
                print(("queried point exists:", iterable[i-1]))
                exit = True
        except:
            print(("queried point does not exist:", query))
            break


if __name__ == "__main__":
    for x in range(18):
        fibsearch([1, 2, 3, 4, 5, 7, 9, 10, 12, 14, 15, 18], x)
