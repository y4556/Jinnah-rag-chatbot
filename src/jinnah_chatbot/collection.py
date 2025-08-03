from chromadb import PersistentClient
db_path = r'D:\red_buffer\VS Code\Jinnah_ChatBot\chroma_db'

# Initialize the PersistentClient with the path
client = PersistentClient(path=db_path)

# List all collections in the DB
collections = client.list_collections()
print("Collections:", collections)

# Example: Load a specific collection by name
# Replace 'your_collection_name' with your actual collection name
# collection = client.get_collection(name='your_collection_name')

# Now you can use `collection` for queries, additions, etc.
