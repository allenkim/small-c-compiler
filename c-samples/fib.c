int main() {
	int a = 0;
	int b = 1;
	int c = 1;
	print(1);
	for (int i = 0; i < 20; i++){
		print(c);
		a = b;
		b = c;
		c = a + b;
	}
	return 0;
}

