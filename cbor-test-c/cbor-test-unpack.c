// export LD_LIBRARY_PATH=/usr/local/lib
// cc -std=c99 -O3 cbor-test-unpack.c -o cbor-test-unpack -lcbor

#include "cbor.h"
#include <stdio.h>
#include <time.h>

#define TEST_COUNT 1000

int main(int argc, char * argv[])
{
    FILE * f = fopen("test.cbor", "rb");
    fseek(f, 0, SEEK_END);
    size_t length = (size_t)ftell(f);

    fseek(f, 0, SEEK_SET);
    unsigned char * buffer = malloc(length);
    fread(buffer, length, 1, f);

    /* Assuming `buffer` contains `info.st_size` bytes of input data */
    struct cbor_load_result result;

    clock_t begin = clock();
    for (int i = 0; i < TEST_COUNT; ++i) {
        cbor_item_t * item = cbor_load(buffer, length, &result);
        /* Deallocate the result */
        cbor_decref(&item);
    }
    clock_t end = clock();


    double time_spent = ((double)(end - begin) / CLOCKS_PER_SEC) / TEST_COUNT;
    double performance = length / time_spent;
    
    printf("Unpacking: %f\n", performance);

    /* Pretty-print the result */
    // cbor_describe(item, stdout);
    // fflush(stdout);
    fclose(f);
}