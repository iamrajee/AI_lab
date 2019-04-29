for(int i = 0, j = m - 1; i < n && j >= 0;) {
    if(a[i] + b[j] > x) {
        j--;

    } else if(a[i] + b[j] < x) {
        i++;
    } else {
        printf("%d + %d = %d\n", a[i], b[j], x);
        i++; j--;
    }
}