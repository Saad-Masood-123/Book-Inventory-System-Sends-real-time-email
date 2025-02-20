import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

class BookNode:
    def __init__(self, name, author, price, stock):
        self.name = name
        self.author = author
        self.price = price
        self.stock = stock
        self.next = None

class BookInventory:
    def __init__(self):
        self.head = None
        self.preload_books()

    def preload_books(self):
        self.add_book("The Great Gatsby", "F. Scott Fitzgerald", 10.99, 5)
        self.add_book("1984", "George Orwell", 8.99, 8)
        self.add_book("To Kill a Mockingbird", "Harper Lee", 12.49, 4)
        self.add_book("The Catcher in the Rye", "J.D. Salinger", 11.99, 6)
        self.add_book("Pride and Prejudice", "Jane Austen", 9.99, 10)

    def add_book(self, name, author, price, stock):
        new_book = BookNode(name, author, price, stock)
        if not self.head:
            self.head = new_book
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_book

    def display_books(self):
        if not self.head:
            print("No books in inventory.")
            return
        print("\nBooks in Inventory:")
        current = self.head
        while current:
            print(f"Name: {current.name}, Author: {current.author}, Price: ${current.price}, Stock: {current.stock}")
            current = current.next

    def search_book(self, name):
        current = self.head
        while current:
            if name.lower() in current.name.lower():
                return current
            current = current.next
        return None

    def delete_book(self, name):
        if not self.head:
            print("No books to delete.")
            return
        if self.head.name.lower() == name.lower():
            print(f"'{self.head.name}' deleted.")
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next.name.lower() != name.lower():
            current = current.next
        if current.next:
            print(f"'{current.next.name}' deleted.")
            current.next = current.next.next
        else:
            print(f"Book '{name}' not found.")

    def count_books(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        print(f"Total books in inventory: {count}")

    def buy_book(self, name, quantity, customer_email):
        book = self.search_book(name)
        if not book:
            print("Book not found.")
            return
        if book.stock >= quantity:
            book.stock -= quantity
            print(f"Purchased {quantity} copies of '{book.name}'.")
            self.send_email(customer_email, book.name, quantity)
        else:
            print(f"Insufficient stock. Available: {book.stock}")

    def send_email(self, customer_email, book_name, quantity):
        try:
            sender_email = "saadchahal000@gmail.com"
            sender_password = "USE SEND EMAIL PASSWORD"#i am use my personal email address but not given my pass (kindly for email purpose use your email,and password)
            subject = "Thank You for Your Purchase!"
            body = f"""Dear Customer,\n\nThank you for purchasing {quantity} copy/copies of '{book_name}'.\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nRegards,\nBook Inventory System"""
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = customer_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
                print(f"Email sent to {customer_email}.")
        except Exception as e:
            print(f"Email sending failed: {e}")

if __name__ == "__main__":
    inventory = BookInventory()
    while True:
        print("\nMenu:")
        print("1. Add Book\n2. Display Books\n3. Buy Book\n4. Delete Book\n5. Count Books\n6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter book name: ").strip()
            author = input("Enter author: ").strip()
            price = float(input("Enter price: ").strip())
            stock = int(input("Enter stock quantity: ").strip())
            inventory.add_book(name, author, price, stock)

        elif choice == "2":
            inventory.display_books()

        elif choice == "3":
            name = input("Enter book name: ").strip()
            quantity = int(input("Enter quantity: ").strip())
            email = input("Enter your email: ").strip()
            inventory.buy_book(name, quantity, email)

        elif choice == "4":
            name = input("Enter book name to delete: ").strip()
            inventory.delete_book(name)

        elif choice == "5":
            inventory.count_books()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
