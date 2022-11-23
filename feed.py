# Copyright Yahoo. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.

import random
import json
import sys


def generate_documents(num_docs, tensor_size):
    docs = []
    for n in range(1, num_docs+1):
        docs.append({
            "put": "id:mynamespace:vector::{}".format(n),
            "fields": {
                "id": n,
                "tags": ["tag1", "tag2"],
                "vector": {
                    "values": [random.random() for i in range(tensor_size)]
                }
            }
        })
    return json.dumps(docs, indent=2)


def main():
    num_docs = 1
    tensor_size = 768
    if len(sys.argv) > 1:
        num_docs = int(sys.argv[1])
    if len(sys.argv) > 2:
        tensor_size = int(sys.argv[2])
    print(generate_documents(num_docs, tensor_size))


if __name__ == "__main__":
    main()
