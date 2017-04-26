int main() {
	for (int n = 2; n < 100; n++){
		int prime = 1;
		for (int i = 2; i < n; i++){
			if (n % i == 0){
				prime = 0;
				break;
			}
		}
		if (prime)
			print(n);
	}
	return 0;
}

