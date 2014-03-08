CFLAGS = -ggdb2

all:
	gcc $(CFLAGS) -c error.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -c safe.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -o os-detect os-detect.c -Wall -ansi -pedantic
	gcc $(CFLAGS) -lrt -lpthread -pthread -c safeexec.c `./os-detect` -Wall -ansi -pedantic
	gcc $(CFLAGS) -lrt -lpthread -pthread -o safeexec error.o safeexec.o safe.o -Wall -ansi -pedantic

install:
	cp -f safeexec /usr/bin/safeexec
	chmod +s /usr/bin/safeexec

uninstall:
	rm -f /usr/bin/safeexec

clean:
	rm -rf *.o safeexec os-detect
