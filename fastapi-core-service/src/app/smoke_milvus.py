import os
import traceback

print('Checking Milvus connection...')
try:
    from pymilvus import connections, utility
    host = os.getenv('MILVUS_HOST', 'localhost')
    port = os.getenv('MILVUS_PORT', '19530')
    print('Connecting to', host, port)
    connections.connect(host=host, port=port)
    cols = utility.list_collections()
    print('Milvus OK. Collections:', cols)
except Exception as e:
    print('Milvus connection error:', e)
    traceback.print_exc()
