from elasticsearch import Elasticsearch
import csv
def connect_to_elasticsearch():
    es = Elasticsearch(["http://localhost:9200"])
    try:
        if es.ping():
            print("Connected to Elasticsearch")
        else:
            print("Connection failed")
    except Exception as e:
        print("Error connecting to Elasticsearch:", e)
    return es

def list_all_indexes(host="http://localhost:9200"):
    """
    List all indexes in the Elasticsearch database.
    
    Args:
        host (str): Elasticsearch URL (e.g., http://localhost:9200).
        username (str): Elasticsearch username (default: elastic).
        password (str): Elasticsearch password.
    
    Returns:
        None: Prints the list of indexes or an error message.
    """
    # Connect to Elasticsearch
    es = Elasticsearch(
        host,
    )

    # Try to list indexes
    try:
        # Get all indexes in JSON format
        indexes = es.cat.indices(format="json")
        if indexes:
            print("Indexes in your Elasticsearch database:")
            for index in indexes:
                print(f"-> {index['index']} (Documents: {index['docs.count']})")
        else:
            print("No indexes found in the database.")
    except Exception as e:
        print(f"Error: {e}")
def checkIndexExists(index_name):
    """
    Check if an index exists in the Elasticsearch database.
    Args:
        index_name (str): Name of the index to check.
    Returns:
        bool: True if the index exists, False otherwise.
    """
    es = connect_to_elasticsearch()
    print("es: ", es)
    return es.indices.exists(index=index_name)


def view_Data_From_Index(index_name):
    print("Type of index_name:", type(index_name))
    es = connect_to_elasticsearch()
    flag = checkIndexExists(index_name)
    if flag:
        print(f"Index '{index_name}' exists.")
        # Fetch data from the index
        results = es.search(index=index_name, body={"query": {"match_all": {}}})
        # print("type of results :", type(results))
        hits = results['hits']['hits']
        print(len(hits))
        # print("Type of hits : ", type(hits))
        total = results['hits']['total']['value']
        # print("Type of total : ", type(total))
        print(f"Total documents in '{index_name}': {total}")
        if hits:
            print(f"Documents in {index_name} ({len(hits)} of {total} total):")
            with open("kibana_ecommerce_Data.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Data"])
                for hit in hits:
                    writer.writerow([hit['_id'], hit['_source']])
        else:
            print(f"No documents found in '{index_name}'.")

def list_all_ids_in_specific_index(index_name, size=5):
    es = connect_to_elasticsearch()
    try:
        if not checkIndexExists(index_name):
            print(f"Index '{index_name}' does not exists")
            return
        
        result = es.search(
            index=index_name,
            body={
                "query": {"match_all": {}},
                "_source": False   # Don't fetch document data, only IDs
            },
            size=size
        )
        # extract ids
        hits = result['hits']['hits']
        if hits:
            print(f"First {len(hits)} document IDs in {index_name} : ")
            with open("kibana_sample_data_ecommerce_ids.csv", '+a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['kibana_sample_data_ecommerce_ids'])
                for i, hit in enumerate(hits, 1):
                    writer.writerow({hit['_id']})
 
        else:
            print(f"No documents found in {index_name}")
    except Exception as e:
        print(f"Error :{e}")





def view_doc_by_id(index_name='kibana_sample_data_ecommerce', doc_id='8zXxzZYBPOfksx146VlD'):
    es = connect_to_elasticsearch()
    try:
        if not checkIndexExists(index_name):
            print(f"Index '{index_name}' does not exist.")
            return
        result = es.get(index=index_name, id=doc_id)
        if result["found"]:
            with open('kibana_sample_data_ecommerce_data_with_specific_id.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Document ID", result['_id']])
                writer.writerow(["Field", "Value"])
                for key, value in result['_source'].items():
                    writer.writerow([key, str(value)])
        else:
            print(f"Document with ID '{doc_id}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_Data_From_Index('kibana_sample_data_ecommerce')