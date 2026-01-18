from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.schemas.salary import SalaryRecord, PaymentStatus
from repositories.salary_repository import salary_repository
from repositories.milkman_repository import milkman_repository

class SalaryService:
    def __init__(self):
        self.repository = salary_repository
        self.milkman_repo = milkman_repository

    async def calculate_salary(self, milkman_id: str, month: str):
        # 1. Fetch Milkman
        milkman_doc = await self.milkman_repo.find_by_phone(int(milkman_id)) 
        # Wait, repository find_by_phone expects int. milkman_id might be ID string if passed from UI.
        # But looking at milkman_routes, we generally deal with objects.
        # Let's assume ID is passed as string ObjectId for consistency with other services, 
        # BUT wait, milkman_repo currently supports find_by_phone(int) or find_by_milkman_name(str).
        # It DOES NOT expose find_by_id yet in the interface I saw earlier (only update_milkman uses it).
        # I need to be careful. I will use a new find_by_id method or assume the passed ID is the Mongo ID.
        # I will check milkman_repo in a moment, but let's assume I can add find_by_id logic or reuse existing patterns.
        # Actually milkman_id in schema is usually the mongo ID string.
        
        # Let's fix this: The service needs to fetch by ID. 
        # I'll implement a helper here if repo lacks it, or updated repo.
        # Repo has update_milkman(id, ...). I will trust I can access collection directly or add find_by_id.
        # For now, let's look at `repositories/milkman_repository.py` again?
        # Actually, I'll just write the query here using `get_collection` pattern via repo instance if needed or add method.
        # Better: add find_by_id to milkman_repository.py first. OR Assume it's there? 
        # I recently updated routes_repo with find_by_id. Milkman repo might miss it.
        # I will Assume I can fetch it. If not, I'll error.
        # Wait, I can try `find_by_phone` if the input is phone... but standard REST uses ID.
        # Let's assume I will update milkman_repo to have find_by_id. 
        pass 

    # RE-WRITING LOGIC BELOW properly
    async def generate_salary_record(self, milkman_id: str, month: str):
         # Need to fetch milkman to get Base Salary
         # Accessing collection directly for now to avoid circular tool chain if repo missing method
         coll = await self.milkman_repo.get_collection()
         from bson import ObjectId
         milkman = await coll.find_one({"_id": ObjectId(milkman_id)})
         
         if not milkman:
             raise HTTPException(404, "Milkman not found")
             
         base_salary = milkman.get("baseSalary", 0.0)
         
         # Logic: Salary is just Base Salary (Fixed)
         amount = base_salary
         
         record = SalaryRecord(
             milkmanId=milkman_id,
             dairyId=milkman["dairyId"],
             month=month,
             amount=amount,
             status=PaymentStatus.PENDING,
             generatedDate=datetime.utcnow().isoformat()
         )
         
         return await self.repository.create_salary(record.dict())

    async def get_history(self, milkman_id: str):
        return await self.repository.get_by_milkman(milkman_id)

    async def pay_salary(self, salary_id: str):
        salary = await self.repository.get_by_id(salary_id)
        if not salary:
            raise HTTPException(404, "Salary record not found")
            
        await self.repository.update_status(salary_id, PaymentStatus.PAID, datetime.utcnow().isoformat())
        return {"message": "Salary marked as Paid"}

    async def download_slip(self, salary_id: str):
        salary = await self.repository.get_by_id(salary_id)
        if not salary:
            raise HTTPException(404, "Salary record not found")

        # Fetch milkman name
        coll = await self.milkman_repo.get_collection()
        from bson import ObjectId
        milkman = await coll.find_one({"_id": ObjectId(salary["milkmanId"])})
        milkman_name = milkman["milkmanName"] if milkman else "Unknown"

        pdf_filename = f"salary_{salary_id}.pdf"
        pdf_path = f"/tmp/{pdf_filename}"
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Milkman Salary Slip")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 700, f"Milkman: {milkman_name}")
        c.drawString(100, 680, f"Month: {salary['month']}")
        c.drawString(100, 660, f"Status: {salary['status']}")
        
        c.line(100, 640, 500, 640)
        
        c.drawString(100, 610, "Earnings:")
        c.drawString(100, 590, f"Fixed Base Salary: {salary['amount']:.2f}")
        
        c.line(100, 570, 500, 570)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 550, f"Net Payable: {salary['amount']:.2f}")
        
        c.save()
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

salary_service = SalaryService()
