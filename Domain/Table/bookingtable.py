import json
import os
from datetime import datetime, timedelta

bookingFile = "Database/booking.json"

TIME_SLOTS = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
MAX_SEATS_PER_TABLE = 6

def loadBooking():
    if not os.path.exists(bookingFile):
        return []
    with open(bookingFile, "r") as f:
        return json.load(f)

def saveBooking(bookings):
    with open(bookingFile, "w") as f:
        json.dump(bookings, f, indent=4)

def viewAllBooking():
    bookings = loadBooking()
    if not bookings:
        print("No bookings yet.")
        return

    bookingDate = input("Enter date to view bookings (YYYY-MM-DD): ").strip()
    filtered = [b for b in bookings if b.get("bookingDate") == bookingDate]

    if not filtered:
        print(f"No bookings found on {bookingDate}")
        return

    print("\n------ All Bookings on", bookingDate, "------")
    for b in filtered:
        print(f"Table {b['tableNo']} | Customer: {b['customerName']} | Time Slot: {b['timeSlot']} | Duration: {b.get('duration', 1)} hr(s)")

def isTimeOverlap(start1, duration1, start2, duration2):
    """Returns True if two time windows overlap"""
    fmt = "%H:%M"
    end1 = (datetime.strptime(start1, fmt) + timedelta(hours=duration1)).time()
    end2 = (datetime.strptime(start2, fmt) + timedelta(hours=duration2)).time()
    s1 = datetime.strptime(start1, fmt).time()
    s2 = datetime.strptime(start2, fmt).time()
    return s1 < end2 and s2 < end1

def bookTable():
    bookings = loadBooking()
    allTables = list(range(1, 11)) 

    bookingDate = input("Enter booking date (YYYY-MM-DD): ").strip()

    try:
        booking_dt = datetime.strptime(bookingDate, "%Y-%m-%d").date()
        today = datetime.now().date()
        if booking_dt < today:
            print(" You cannot book a past date! ")
            return
        
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD. ")
        return

    print("Available time slots:", TIME_SLOTS)
    timeSlot = input("Enter start time (HH:MM): ").strip()

    if timeSlot not in TIME_SLOTS:
        print("Invalid time slot.")
        return

    try:
        duration = int(input("Enter how many hours to book (1-3): "))
        if not 1 <= duration <= 3:
            print("Duration must be between 1 to 3 hours.")
            return
    except ValueError:
        print("Invalid duration.")
        return

    availableTables = []
    tableSeatsStatus = {}

    for table in allTables:
        totalSeatsBooked = 0
        conflict = False

        for b in bookings:
            if b["bookingDate"] == bookingDate and b["tableNo"] == table:
                if isTimeOverlap(timeSlot, duration, b["timeSlot"], b.get("duration", 1)):
                    totalSeatsBooked += b.get("seats", 0)
                    if totalSeatsBooked >= MAX_SEATS_PER_TABLE:
                        conflict = True
                        break

        if not conflict:
            remainingSeats = MAX_SEATS_PER_TABLE - totalSeatsBooked
            if remainingSeats > 0:
                availableTables.append(table)
                tableSeatsStatus[table] = remainingSeats

    if not availableTables:
        print("No tables available for the selected time and duration.")
        return

    print("Available tables (with reamaining seats): ")
    for t in availableTables:
        print(f"Table {t} -> {tableSeatsStatus[t]} seats left ")

    customerName = input("Enter customer name: ").strip()
    if not customerName:
        print("Customer name cannot be empty. ")
        return

    try:
        tableNo = int(input("Enter table number to book: "))
        if tableNo not in availableTables:
            print("Table already booked or invalid.")
            return
    except ValueError:
        print("Invalid table number.")
        return
 
    try:
        seats = int(input("Enter number of seats to book: "))
        if seats <= 0 or seats > tableSeatsStatus[tableNo]:
            print(f"Only {tableSeatsStatus[tableNo]} seats are available on this table. ")
    except ValueError:
        print("Invalid seat number. ")
        return

    dateTime = datetime.now().strftime("%Y-%m-%d %H:%M")

    bookings.append({
        "tableNo": tableNo,
        "customerName": customerName,
        "seats" : seats,
        "timeSlot": timeSlot,
        "duration": duration,
        "bookingDate": bookingDate,
        "dateTime": dateTime
    })

    saveBooking(bookings)
    print(f"Table {tableNo} booked for {customerName} on {bookingDate} at {timeSlot} for {duration} hour(s).")

def cancelBooking():
    bookings = loadBooking()

    customerName = input("Enter customer name: ").strip()
    try:
        tableNo = int(input("Enter table number to cancel: "))
    except ValueError:
        print("Invalid table number.")
        return

    timeSlot = input("Enter time slot to cancel (HH:MM): ").strip()
    bookingDate = input("Enter booking date (YYYY-MM-DD): ").strip()

    updated = [
        b for b in bookings
        if not (b["tableNo"] == tableNo and b["timeSlot"] == timeSlot and
                b["customerName"] == customerName and b["bookingDate"] == bookingDate)
    ]

    if len(updated) == len(bookings):
        print("No matching booking found.")
    else:
        saveBooking(updated)
        print(f"Booking for Table {tableNo} on {bookingDate} at {timeSlot} cancelled.")

def tableBookingMenu():
    while True:
        print("\n--- Table Booking Menu ---")
        print("1. Book a Table")
        print("2. View All Bookings")
        print("3. Cancel a Booking")
        print("4. Back to Previous Menu")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            bookTable()
        elif choice == '2':
            viewAllBooking()
        elif choice == '3':
            cancelBooking()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")