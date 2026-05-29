// Verifica daca un numar este prim
int n = 17;
int i = 2;
int este_prim = 1;

while (i < n) {
    rest = n % i;
    if (rest == 0) {
        este_prim = 0;
    }
    i = i + 1;
}

if (este_prim == 1) {
    print(n);
    print(1);
} else {
    print(n);
    print(0);
}

// Primele 10 patrate perfecte
int j = 1;
while (j <= 10) {
    patrat = j * j;
    print(patrat);
    j = j + 1;
}

// Sirul Fibonacci primii 8 termeni
int a = 0;
int b = 1;
int k = 0;
while (k < 8) {
    print(a);
    int c = a + b;
    a = b;
    b = c;
    k = k + 1;
}