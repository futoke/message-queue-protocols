// export LD_LIBRARY_PATH=/usr/local/lib
// cc -std=c99 -O3 cbor-test-pack.c -o cbor-test-pack -lcbor

#include <string.h>
#include <math.h>
#include <time.h>
#include <float.h>
#include <cjson/cJSON.h>
#include "cbor.h"
#include "cbor/internal/builder_callbacks.h"
#include "cbor/internal/loaders.h"

#define TEST_COUNT 1000

typedef void(*cbor_load_callback_t)(cJSON *, const struct cbor_callbacks *, void *);

cbor_item_t * cjson_cbor_load(void *source, cbor_load_callback_t cbor_load_callback)
{
    static struct cbor_callbacks callbacks = {
        .uint64 = &cbor_builder_uint64_callback,
        .negint64 = &cbor_builder_negint64_callback,
        .string = &cbor_builder_string_callback,
        .array_start = &cbor_builder_array_start_callback,
        .map_start = &cbor_builder_map_start_callback,
        .null = &cbor_builder_null_callback,
        .boolean = &cbor_builder_boolean_callback,
        .float4 = &cbor_builder_float4_callback,
    };

    /* Context stack */
    struct _cbor_stack stack = _cbor_stack_init();

    /* Target for callbacks */
    struct _cbor_decoder_context context = (struct _cbor_decoder_context) {
        .stack = &stack,
    };

    cbor_load_callback(source, &callbacks, &context);

    return context.root;
}

void cjson_cbor_stream_decode(cJSON * source,
                              const struct cbor_callbacks *callbacks,
                              void * context)
{
    switch (source->type) {
        case cJSON_False:
        {
            callbacks->boolean(context, false);
            return;
        }
        case cJSON_True:
        {
            callbacks->boolean(context, true);
            return;
        }
        case cJSON_NULL:
        {
            callbacks->null(context);
            return;
        }
        case cJSON_Number:
        {
            // This is stupid -- ints and doubles cannot are not distinguished
            if (fabs(source->valuedouble - source->valueint) > DBL_EPSILON) {
                callbacks->float4(context, source->valuedouble);
            } else {
                // XXX: This is not portable
                if (source->valueint >= 0) {
                    callbacks->uint64(context, source->valueint);
                } else {
                    callbacks->negint64(context, source->valueint + 1);
                }
            }
            return;
        }
        case cJSON_String:
        {
            // XXX: Assume cJSON handled unicode correctly
            callbacks->string(context, (unsigned char *)source->valuestring, strlen(source->valuestring));
            return;
        }
        case cJSON_Array:
        {
            callbacks->array_start(context, cJSON_GetArraySize(source));
            cJSON *item = source->child;
            while (item != NULL) {
                cjson_cbor_stream_decode(item, callbacks, context);
                item = item->next;
            }
            return;
        }
        case cJSON_Object:
        {
            callbacks->map_start(context, cJSON_GetArraySize(source));
            cJSON *item = source->child;
            while (item != NULL) {
                callbacks->string(context, (unsigned char *) item->string, strlen(item->string));
                cjson_cbor_stream_decode(item, callbacks, context);
                item = item->next;
            }
            return;
        }
    }
}

void usage()
{
    printf("Usage: cjson [input JSON file]\n");
    exit(1);
}

int main(int argc, char * argv[])
{
    FILE * f = fopen("test.json", "rb");

    /* Read input file into a buffer (cJSON doesn't work with streams) */
    fseek(f, 0, SEEK_END);
    size_t length = (size_t)ftell(f);
    fseek(f, 0, SEEK_SET);
    char * json_buffer = malloc(length + 1);
    fread(json_buffer, length, 1, f);
    json_buffer[length] = '\0';

    clock_t begin = clock();
    for (int i = 0; i < TEST_COUNT; ++i) {
        cJSON * json = cJSON_Parse(json_buffer);
        cbor_item_t * cbor = cjson_cbor_load(json, cjson_cbor_stream_decode);

        cJSON_Delete(json);
        cbor_decref(&cbor);
    }
    clock_t end = clock();


    double time_spent = ((double)(end - begin) / CLOCKS_PER_SEC) / TEST_COUNT;
    double performance = length / time_spent;
    
    printf("Packing: %f\n", performance);

    /* Print out CBOR bytes */
    // unsigned char * buffer;
    // size_t buffer_size, cbor_length = cbor_serialize_alloc(cbor, &buffer, &buffer_size);
    // fwrite(buffer, 1, cbor_length, stdout);
    // free(buffer);
    // fflush(stdout);
}