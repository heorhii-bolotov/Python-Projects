Ход решения
===========

- mkdir W6T1git
- cd W6T1git/
1. git clone git@gitlab.com:abramovtv/git-test.git
    - cd git-test/
2. git checkout feature/rot13
    - `python -m unittest -v`
3. git checkout feature/vigenere
    - `python -m unittest -v`
4. git checkout master
5. git checkout -b dev
6. git merge --no-ff feature/rot13
7. git merge --no-ff feature/vigenere		`# conflict test.py and cipher.py`
    - emacs test.py		`# refactor file`
    - emacs cipher.py   `# refactor file`
    - `python -m unittest -v`
8. git add test.py
9. git add cipher.py
git commit -m `"bugfix in cipher.py & test.py"`
10. git checkout master
11. git merge --no-ff dev
    - `python -m unittest -v`

- zip -r git-test.zip git-test/

[![отчет](/Users/macair/Desktop/W6T1git/result.png)]

