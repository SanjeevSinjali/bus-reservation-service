from reportlab.pdfgen import canvas
from datetime import datetime

class TicketPDF:
    def __init__(self, seats, total_amount, bus_id, username,file_path=None):
        self.seats = seats
        self.total_amount = total_amount
        self.bus_id = bus_id
        self.username = username

        if file_path:
            self.pdf_filename = file_path
        else:
            self.pdf_filename = f"ticket_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    def generate_pdf(self):
        c = canvas.Canvas(self.pdf_filename)

        # Add content to the PDF
        c.drawString(100, 800, "Ticket Details:")
        c.drawString(100, 780, f"Username: {self.username}")
        c.drawString(100, 760, f"Bus ID: {self.bus_id}")
        c.drawString(100, 740, f"Seats: {', '.join(map(str, self.seats))}")
        c.drawString(100, 720, f"Total Amount: {self.total_amount}")

        # Save the PDF
        c.save()
        print(f"PDF generated: {self.pdf_filename}")