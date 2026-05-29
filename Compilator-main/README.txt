Cum sa rulezi:

Deschizi terminalul, intri in folderul unde e proiectul si folosesti comanda: python compiler.py test_complet.ml --run
test_complet.ml este doar un fisier test. Puteti ca sa scrieti propriul cod intr-un fisier text si sa scrieti numele fisierului in loc de test_complet.ml si se va executa. Programul arata doar valori numerice si bool.

Exemple:
  python compiler.py prog.ml              # compilare + generare .asm
  python compiler.py prog.ml --run        # interpretare directa
  python compiler.py prog.ml --tokens     # afiseaza tokenii
  python compiler.py prog.ml --ast        # afiseaza AST-ul
  python compiler.py prog.ml --ir         # afiseaza IR-ul (TAC)
  python compiler.py prog.ml --asm        # afiseaza Assembly-ul
  python compiler.py prog.ml -o myapp     # scrie myapp.asm