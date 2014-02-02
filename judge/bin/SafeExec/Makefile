CFLAGS = -ggdb2

all:
	gcc $(CFLAGS) -c error.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -c safe.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -o os-detect os-detect.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -lrt -lpthread -pthread -c safeexec.c `./os-detect` -Wall -ansi -pedantic
	gcc $(CFLAGS) -lrt -lpthread -pthread -o safeexec error.o safeexec.o safe.o -Wall -ansi -pedantic
	chmod +s safeexec

clean:
	rm -rf *.o safeexec os-detect
