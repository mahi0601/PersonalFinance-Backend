import csv
import io
from fastapi import APIRouter, Depends
from app.core.db import get_db_connection
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

class TransactionRequest(BaseModel):
    user_id: int
    amount: float
    category: str
    description: str


transaction_router = APIRouter()

@transaction_router.get("/")
def get_transactions(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return [dict(tx) for tx in transactions]

@transaction_router.post("/")
def create_transaction(request: TransactionRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO transactions (user_id, amount, category, description) 
           VALUES (?, ?, ?, ?)""",
        (request.user_id, request.amount, request.category, request.description)
    )
    conn.commit()
    transaction_id = cursor.lastrowid
    conn.close()
    return {"message": "Transaction created successfully", "transaction_id": transaction_id}


@transaction_router.get("/dashboard/data/")
def get_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    total_savings = cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ?", ("Savings",)).fetchone()[0] or 0
    monthly_expenses = cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ?", ("Expenses",)).fetchone()[0] or 0
    investment_growth = cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ?", ("Investments",)).fetchone()[0] or 0
    conn.close()
    return {
        "total_savings": total_savings,
        "monthly_expenses": monthly_expenses,
        "investment_growth": investment_growth
    }


@transaction_router.post("/transactions/import/")
async def import_transactions(file: UploadFile = File(...)):
    """
    Import transactions from an uploaded CSV file.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        contents = await file.read()
        decoded_contents = contents.decode('utf-8')
        reader = csv.reader(io.StringIO(decoded_contents))

        next(reader, None)
        
        for row in reader:
            if len(row) != 4:
                raise HTTPException(status_code=400, detail="Invalid CSV format. Each row must have 4 columns.")
            
            try:
                user_id = int(row[0])
                amount = float(row[1])
                category = row[2]
                description = row[3]
                
                cursor.execute(
                    "INSERT INTO transactions (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
                    (user_id, amount, category, description)
                )
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid data type in CSV file.")
        
        conn.commit()
        return {"message": "Transactions imported successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()


@transaction_router.get("/transactions/export/")
async def export_transactions():
    """
    Export transactions to a CSV file and provide a downloadable response.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    transactions = cursor.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    
    csv_content = "user_id,amount,category,description\n"
    for transaction in transactions:
        csv_content += ",".join(map(str, transaction)) + "\n"
    
    return {
        "file": csv_content
    }
