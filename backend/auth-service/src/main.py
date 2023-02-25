import fastapi
from cassandra.cluster import Cluster

cluster = Cluster()

session = cluster.connect()

app = fastapi.FastAPI()

@app.get("/")
def read_root(user_id: int):
    row = session.execute(f"SELECT * FROM store.shopping_cart WHERE userid='{user_id}'")
    user = row.one()
    return {"userId": str(user.userid), "itemCount": user.item_count, 'timestamp': str(user.last_update_timestamp)}

