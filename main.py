from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
from bson import ObjectId  # Import ObjectId for MongoDB queries

# Initialize MongoDB client and database
client = MongoClient("mongodb://localhost:27017/")
db = client["todo"]
collection = db["tasks"]

# Initialize FastAPI application
app = FastAPI()


# Define the User model for request and response validation
class User(BaseModel):
    id: Optional[str] = None  # Optional ID field for MongoDB ObjectId
    name: str  # User's name
    email: str  # User's email
    age: int  # User's age


# Helper function to serialize MongoDB documents into Python dictionaries
def user_serializer(user):
    return {
        "id": str(user["_id"]),  # Convert ObjectId to string
        "name": user.get("name", ""),  # Handle missing 'name' key
        "email": user.get("email", ""),  # Handle missing 'email' key
        "age": user.get("age", 0),  # Default age to 0 if missing
    }


# Endpoint to create a new user
@app.post("/users", response_model=User)
async def create_user(user: User):
    user_dict = user.model_dump(
        exclude_unset=True
    )  # Convert Pydantic model to dictionary
    result = collection.insert_one(user_dict)  # Insert user into MongoDB
    user.id = str(result.inserted_id)  # Set the inserted ID
    return user


# Endpoint to update an existing user by ID
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    user_dict = user.model_dump(
        exclude_unset=True
    )  # Convert Pydantic model to dictionary
    result = collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_dict}
    )  # Update user in MongoDB
    if result.modified_count:  # Check if any document was modified
        return user
    raise HTTPException(
        status_code=404, detail="User not found"
    )  # Raise 404 if user not found


# Endpoint to retrieve all users
@app.get("/users", response_model=List[User])
async def get_users():
    users = []
    for user_data in collection.find():  # Fetch all users from MongoDB
        users.append(user_serializer(user_data))  # Serialize each user
    return users


# Endpoint to search for users by name (case-insensitive partial match)
@app.get("/user", response_model=List[User])
async def get_user_data(name: str):
    users = []
    for user_data in collection.find(
        {
            "name": {"$regex": name, "$options": "i"}
        }  # MongoDB regex for case-insensitive search
    ):
        users.append(user_serializer(user_data))  # Serialize each matching user
    if users:  # Return users if found
        return users
    raise HTTPException(
        status_code=404, detail="No users found"
    )  # Raise 404 if no users found


@app.delete("/users/{user_name}")
async def delete_user(user_name: str):
    # Find the user before deleting
    user = collection.find_one(
        {"name": {"$regex": user_name, "$options": "i"}}
    )  # Use find_one to get a single document
    if user:
        # Delete the user
        result = collection.delete_one({"_id": user["_id"]})
        if result.deleted_count:
            # Return the details of the deleted user
            return {
                "message": "User deleted successfully",
                "deleted_user": user_serializer(user),
            }
    # Raise 404 if user not found
    raise HTTPException(status_code=404, detail="User not found")
