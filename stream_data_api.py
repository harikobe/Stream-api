
#import the needed libraries ==>
#for async programming
import asyncio 
# async for postgres
import asyncpg 
import json
from datetime import datetime,date
from  decimal import Decimal
import os
from dotenv import load_dotenv
from fastapi import FastAPI,Depends,Path


app = FastAPI()

#-------------------------------------------------------------------#


#load environment variables from .env file
load_dotenv()


# Access the environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT=os.getenv('DB_PORT')

#------------------------------------------------------------------------

#custom encoder for handling specific data types in JSON serialization
class CustomEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,(datetime,date)):
            return obj.isoformat()
        if isinstance(obj,Decimal):
            return float(obj)
        """
        # Add custom handling for additional types
        
        if isinstance(obj, YourCustomType):
            return obj.to_json()  # Replace YourCustomType with the actual type and method
        
        # Add more custom type handling as needed
        """
        return super().default(obj)

#-----------------------------------------------------------------------           
#DB connection pool

#Dependency to create the database connection pool:
async def create_db_pool(db_name: str = Path(..., title="Database Name")):
     db_config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'database':db_name,
        'port':DB_PORT
       }
        
     # Establish a connection pool to the PostgreSQL database
     pool = await asyncpg.create_pool(**db_config)
     return pool


#------------------------------------------------------------------------------------
#Routes:

#Route to stream data with pagination support:
@app.get("/stream-data/{db_name}")
async def stream_data(
    #pagination -->
    page:int = 1,  #page number(default :1)
    page_size:int = 10, #number of item per page (default:10)
    #db dependency
    db_pool: asyncpg.pool.Pool = Depends(create_db_pool)):
    
    result_data = [] #storing the data 
    
    try:
        # Execute a query to stream data 
        
        #obtain connection from the pool is assigned as "connection"
        async with db_pool.acquire() as connection:
            #context manager for the connection is properly execute and release back to pool
            async with connection.transaction():
                 
            
            #Get all the table names in the given database
                """
                The result (tables) is a list of dictionaries where each dictionary contains information about a table
                such as the 'table_name'.
                """
                tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
                tables = await connection.fetch(tables_query)
            #Loop through each table and get column headers    
                for table in tables:
                    table_name = table['table_name']
                    
                    
            #Get column headers for each table
                    """
                The result (columns) is a list of dictionaries where each dictionary contains information about a column
                such as the 'column_name'.
                   """
                    columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}';"   
                    columns =  await connection.fetch(columns_query)
                    
            #query to fetch all the data:
                    select_query = f"SELECT * FROM {table_name} LIMIT $1 OFFSET $2;"
                    
                    table_data = [] #List to store the rows of data 
                    
                    async for row in connection.cursor(select_query,page_size,(page - 1) * page_size):
                        #Serialize the row under column as dict
                        data_row = {
                            #dict comprehension:
                            column['column_name']: #key
                                row[column['column_name']] #value
                                for column in columns
                            }
    
                        table_data.append(data_row)
                        
                    # Append the table data to the result
                    result_data.append({
                        "table_name": table_name,
                        "columns": [column['column_name'] for column in columns],
                        "data": table_data
                    })
                        
                        
    except Exception as e:
        print(f"Error: {e}")
        
    #if there is no data:
    if not result_data:
        return {"message":"No data found in the specified database tables"}
        
        
#Data serialization:
      # Serialize the result using the custom encoder
    result_json = json.dumps(result_data, cls=CustomEncoder,indent=3)
    
    return json.loads(result_json)
 
#-------------------------------------------------------------------------------------------------           

