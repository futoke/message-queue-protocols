/**
 * Created by ichiro on 09.03.17.
 */
var test_count = 1000;

$.getJSON("test.json", function(json_file) {
    var json_file_size = 14708665;
    var start = performance.now();
    for (i = 0; i < test_count; i++) {
        CBOR.encode(json_file);
    }
    var end = performance.now();
    console.log("Упаковка: " + ((json_file_size / ((end - start) / test_count)) * 1000).toString());

    var cbor = CBOR.encode(json_file);

    var cbor_file_size = cbor.byteLength;
    start = performance.now();
    for (i = 0; i < test_count; i++) {
        CBOR.decode(cbor);
    }
    end = performance.now();
    console.log("Распаковка : " + ((json_file_size / ((end - start) / test_count)) * 1000).toString());

});


