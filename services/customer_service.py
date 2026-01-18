import os
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.schemas.customer import CustomerModel, CustomerRequest, BillRequest
from repositories.customer_repository import customer_repository

class CustomerService:
    def __init__(self):
        self.repository = customer_repository
        
    async def create_customer(self, customer: CustomerRequest):
        data = customer.dict()
        data["createdDate"] = datetime.utcnow().isoformat()
        data["updatedDate"] = datetime.utcnow().isoformat()
        return await self.repository.create_customer(data)

    async def get_by_dairy(self, dairy_id: str):
        return await self.repository.find_by_dairy(dairy_id)

    def calculate_bill_amount(self, customer, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        days = (end_date - start_date).days + 1
        
        if days < 0:
             raise HTTPException(400, "Invalid Date Range")
             
        quantity = customer['dailyQuantity']
        price = customer['pricePerLiter']
        total = days * quantity * price
        return total, days

    async def generate_bill_pdf(self, bill_req: BillRequest):
        customer_doc = await self.repository.find_by_id(bill_req.customerId)
        if not customer_doc:
             raise HTTPException(404, "Customer not found")
        
        # Calculate Logic
        try:
             total_amount, days = self.calculate_bill_amount(customer_doc, bill_req.startDate, bill_req.endDate)
        except ValueError:
             raise HTTPException(400, "Invalid Date Format. Use YYYY-MM-DD")

        # Generate PDF
        pdf_filename = f"bill_{bill_req.customerId}_{bill_req.startDate}_{bill_req.endDate}.pdf"
        pdf_path = f"/tmp/{pdf_filename}" # Using tmp for now
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Milkman Dairy - Invoice")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 700, f"Customer Name: {customer_doc['customerName']}")
        c.drawString(100, 680, f"Phone Number: {customer_doc['phoneNumber']}")
        c.drawString(100, 660, f"Address: {customer_doc.get('address', 'N/A')}")
        
        c.line(100, 640, 500, 640)
        
        c.drawString(100, 610, f"Billing Period: {bill_req.startDate} to {bill_req.endDate}")
        c.drawString(100, 590, f"Total Days: {days}")
        c.drawString(100, 570, f"Daily Quantity: {customer_doc['dailyQuantity']} Liters")
        c.drawString(100, 550, f"Price Per Liter: {customer_doc['pricePerLiter']}")
        
        c.line(100, 530, 500, 530)
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 500, f"Total Amount Due: {total_amount:.2f}")
        
        c.save()
        
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

customer_service = CustomerService()
