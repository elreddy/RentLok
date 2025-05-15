from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Float, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime, date
from typing import Optional, List

DATABASE_URL = "postgresql://rentlok:rentlok@192.168.56.101:5432/rentlok"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# ================== Database Tables ==================
class Property(Base):
    __tablename__ = "properties"
    property_id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    no_of_rooms = Column(Integer, nullable=False)
    owner_id = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)

    rooms = relationship("Room", back_populates="property")
    bookings = relationship("Booking", back_populates="property")

class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True, index=True)
    room_no = Column(String(20), nullable=False)
    floor_no = Column(Integer, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.property_id"), nullable=False)
    operational_status = Column(String(20), nullable=False)
    room_type = Column(String(50))
    rent_per_month = Column(Float, nullable=False)
    is_active = Column(Integer, default=1)

    property = relationship("Property", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

    __table_args__ = (
        CheckConstraint(
            "operational_status IN ('vacant', 'occupied', 'damaged')",
            name="check_operational_status"
        ),
    )

class Tenant(Base):
    __tablename__ = "tenants"
    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_no = Column(String(20), nullable=False)
    details = Column(Text)
    is_active = Column(Integer, default=1)

    bookings = relationship("Booking", back_populates="tenant")

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.property_id"), nullable=False)
    move_in_date = Column(Date, default=date.today)
    move_out_date = Column(Date)
    status = Column(String(20), nullable=False)
    is_active = Column(Integer, default=1)

    room = relationship("Room", back_populates="bookings")
    tenant = relationship("Tenant", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'terminated')",
            name="check_booking_status"
        ),
    )

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
    payment_type = Column(String(20), nullable=False)
    payment_status = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, default=date.today)
    is_active = Column(Integer, default=1)

    booking = relationship("Booking", back_populates="payments")

class Request(Base):
    __tablename__ = "requests"
    request_id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.property_id"), nullable=False)  # Added this line
    tenant_name = Column(String(100), nullable=False)
    phone_no = Column(String(20), nullable=False)
    details = Column(Text)
    request_date = Column(Date, default=date.today)
    is_active = Column(Integer, default=1)

    property = relationship("Property")  # Added relationship

Base.metadata.create_all(bind=engine)

# ================== Dependency ==================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================== Pydantic Models ==================
class PropertyBase(BaseModel):
    property_name: str
    address: str
    no_of_rooms: int

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class PropertyResponse(PropertyBase):
    property_id: int
    owner_id: int
    created_at: datetime
    is_active: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    room_no: str
    floor_no: int
    property_id: int
    operational_status: str
    room_type: Optional[str] = None
    rent_per_month: float

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomResponse(RoomBase):
    room_id: int
    is_active: int

    class Config:
        orm_mode = True

class TenantBase(BaseModel):
    name: str
    phone_no: str
    details: Optional[str] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class TenantResponse(TenantBase):
    tenant_id: int
    is_active: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    room_id: int
    tenant_id: int
    property_id: int
    move_out_date: Optional[date] = None
    status: str

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    pass

class BookingResponse(BookingBase):
    booking_id: int
    move_in_date: date
    is_active: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    booking_id: int
    payment_type: str
    payment_status: str
    amount: float

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    payment_id: int
    payment_date: date
    is_active: int

    class Config:
        orm_mode = True

class RequestBase(BaseModel):
    property_id: int  
    tenant_name: str
    phone_no: str
    details: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class RequestUpdate(RequestBase):
    pass

class RequestResponse(RequestBase):
    request_id: int
    request_date: date
    is_active: int

    class Config:
        orm_mode = True

# ================== Property Endpoints ==================
@app.post("/properties/", response_model=PropertyResponse)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@app.get("/properties/", response_model=List[PropertyResponse])
def read_properties(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Property)
    if active_only:
        query = query.filter(Property.is_active == 1)
    properties = query.all()
    return properties

@app.get("/properties/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    if property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    db_property = db.query(Property).filter(Property.property_id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@app.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property: PropertyUpdate, db: Session = Depends(get_db)):
    if property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    db_property = db.query(Property).filter(Property.property_id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for key, value in property.dict().items():
        setattr(db_property, key, value)

    db.commit()
    db.refresh(db_property)
    return db_property

@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    if property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    db_property = db.query(Property).filter(Property.property_id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Soft delete property and its rooms
    db_property.is_active = 0

    # Soft delete all rooms belonging to this property
    db.query(Room).filter(Room.property_id == property_id).update({"is_active": 0})

    db.commit()
    return {
        "message": "Property and its rooms marked as inactive",
        "inactivated_rooms": db.query(Room).filter(Room.property_id == property_id).count()
    }

# ================== Room Endpoints ==================
@app.post("/rooms/", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    if room.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    if room.operational_status not in ['vacant', 'occupied', 'damaged']:
        raise HTTPException(status_code=400, detail="Invalid operational status")

    db_property = db.query(Property).filter(
        Property.property_id == room.property_id,
        Property.is_active == 1
    ).first()
    if not db_property:
        raise HTTPException(status_code=400, detail="Property not found or inactive")

    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/rooms/", response_model=List[RoomResponse])
def read_rooms(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Room)
    if active_only:
        query = query.filter(Room.is_active == 1)
    rooms = query.all()
    return rooms

@app.get("/rooms/{room_id}", response_model=RoomResponse)
def read_room(room_id: int, db: Session = Depends(get_db)):
    if room_id == 0:
        raise HTTPException(status_code=400, detail="Room ID cannot be 0")

    db_room = db.query(Room).filter(Room.room_id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@app.put("/rooms/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_db)):
    if room_id == 0:
        raise HTTPException(status_code=400, detail="Room ID cannot be 0")

    db_room = db.query(Room).filter(Room.room_id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.operational_status not in ['vacant', 'occupied', 'damaged']:
        raise HTTPException(status_code=400, detail="Invalid operational status")

    if room.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    db_property = db.query(Property).filter(
        Property.property_id == room.property_id,
        Property.is_active == 1
    ).first()
    if not db_property:
        raise HTTPException(status_code=400, detail="Property not found or inactive")

    for key, value in room.dict().items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)
    return db_room

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    if room_id == 0:
        raise HTTPException(status_code=400, detail="Room ID cannot be 0")

    db_room = db.query(Room).filter(Room.room_id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db_room.is_active = 0
    db.commit()
    return {"message": "Room marked as inactive"}

# ================== Tenant Endpoints ==================
@app.post("/tenants/", response_model=TenantResponse)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = Tenant(**tenant.dict())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@app.get("/tenants/", response_model=List[TenantResponse])
def read_tenants(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Tenant)
    if active_only:
        query = query.filter(Tenant.is_active == 1)
    tenants = query.all()
    return tenants

@app.get("/tenants/{tenant_id}", response_model=TenantResponse)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    if tenant_id == 0:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be 0")

    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

@app.put("/tenants/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: int, tenant: TenantUpdate, db: Session = Depends(get_db)):
    if tenant_id == 0:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be 0")

    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    for key, value in tenant.dict().items():
        setattr(db_tenant, key, value)

    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@app.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    if tenant_id == 0:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be 0")

    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    db_tenant.is_active = 0
    db.commit()
    return {"message": "Tenant marked as inactive"}

# ================== Booking Endpoints ==================
@app.post("/bookings/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    if booking.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")
    if booking.room_id == 0:
        raise HTTPException(status_code=400, detail="Room ID cannot be 0")
    if booking.tenant_id == 0:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be 0")

    db_property = db.query(Property).filter(
        Property.property_id == booking.property_id,
        Property.is_active == 1
    ).first()
    if not db_property:
        raise HTTPException(status_code=400, detail="Property not found or inactive")

    db_room = db.query(Room).filter(
        Room.room_id == booking.room_id,
        Room.is_active == 1,
        Room.property_id == booking.property_id
    ).first()
    if not db_room:
        raise HTTPException(status_code=400, detail="Room not found, inactive, or doesn't belong to property")

    db_tenant = db.query(Tenant).filter(
        Tenant.tenant_id == booking.tenant_id,
        Tenant.is_active == 1
    ).first()
    if not db_tenant:
        raise HTTPException(status_code=400, detail="Tenant not found or inactive")

    if booking.status not in ['active', 'completed', 'terminated']:
        raise HTTPException(status_code=400, detail="Invalid booking status")

    db_room.operational_status = 'occupied'

    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/bookings/", response_model=List[BookingResponse])
def read_bookings(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Booking)
    if active_only:
        query = query.filter(Booking.is_active == 1)
    bookings = query.all()
    return bookings

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    if booking_id == 0:
        raise HTTPException(status_code=400, detail="Booking ID cannot be 0")

    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@app.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    if booking_id == 0:
        raise HTTPException(status_code=400, detail="Booking ID cannot be 0")

    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.room_id == 0:
        raise HTTPException(status_code=400, detail="Room ID cannot be 0")
    if booking.tenant_id == 0:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be 0")
    if booking.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    if booking.room_id != db_booking.room_id:
        db_room = db.query(Room).filter(
            Room.room_id == booking.room_id,
            Room.is_active == 1
        ).first()
        if not db_room:
            raise HTTPException(status_code=400, detail="New room not found or inactive")

    if booking.tenant_id != db_booking.tenant_id:
        db_tenant = db.query(Tenant).filter(
            Tenant.tenant_id == booking.tenant_id,
            Tenant.is_active == 1
        ).first()
        if not db_tenant:
            raise HTTPException(status_code=400, detail="New tenant not found or inactive")

    if booking.property_id != db_booking.property_id:
        db_property = db.query(Property).filter(
            Property.property_id == booking.property_id,
            Property.is_active == 1
        ).first()
        if not db_property:
            raise HTTPException(status_code=400, detail="New property not found or inactive")

    if booking.status in ['completed', 'terminated']:
        db_room = db.query(Room).filter(Room.room_id == db_booking.room_id).first()
        if db_room:
            db_room.operational_status = 'vacant'

    for key, value in booking.dict().items():
        setattr(db_booking, key, value)

    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    if booking_id == 0:
        raise HTTPException(status_code=400, detail="Booking ID cannot be 0")

    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Free up the room
    db_room = db.query(Room).filter(Room.room_id == db_booking.room_id).first()
    if db_room:
        db_room.operational_status = 'vacant'

    # Soft delete booking and its payments
    db_booking.is_active = 0

    # Soft delete all payments for this booking
    db.query(Payment).filter(Payment.booking_id == booking_id).update({"is_active": 0})

    db.commit()
    return {
        "message": "Booking and its payments marked as inactive",
        "inactivated_payments": db.query(Payment).filter(Payment.booking_id == booking_id).count()
    }

# ================== Payment Endpoints ==================
@app.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    if payment.booking_id == 0:
        raise HTTPException(status_code=400, detail="Booking ID cannot be 0")

    db_booking = db.query(Booking).filter(
        Booking.booking_id == payment.booking_id,
        Booking.is_active == 1
    ).first()
    if not db_booking:
        raise HTTPException(status_code=400, detail="Booking not found or inactive")

    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/", response_model=List[PaymentResponse])
def read_payments(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Payment)
    if active_only:
        query = query.filter(Payment.is_active == 1)
    payments = query.all()
    return payments

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    if payment_id == 0:
        raise HTTPException(status_code=400, detail="Payment ID cannot be 0")

    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@app.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    if payment_id == 0:
        raise HTTPException(status_code=400, detail="Payment ID cannot be 0")

    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.booking_id == 0:
        raise HTTPException(status_code=400, detail="Booking ID cannot be 0")

    db_booking = db.query(Booking).filter(
        Booking.booking_id == payment.booking_id,
        Booking.is_active == 1
    ).first()
    if not db_booking:
        raise HTTPException(status_code=400, detail="Booking not found or inactive")

    for key, value in payment.dict().items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    if payment_id == 0:
        raise HTTPException(status_code=400, detail="Payment ID cannot be 0")

    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    db_payment.is_active = 0
    db.commit()
    return {"message": "Payment marked as inactive"}

# ================== Request Endpoints ==================
@app.post("/requests/", response_model=RequestResponse)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    if request.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")
        
    db_property = db.query(Property).filter(
        Property.property_id == request.property_id,
        Property.is_active == 1
    ).first()
    if not db_property:
        raise HTTPException(status_code=400, detail="Property not found or inactive")

    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.get("/requests/", response_model=List[RequestResponse])
def read_requests(active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Request)
    if active_only:
        query = query.filter(Request.is_active == 1)
    requests = query.order_by(Request.request_date.desc()).all()
    return requests

@app.get("/requests/{request_id}", response_model=RequestResponse)
def read_request(request_id: int, db: Session = Depends(get_db)):
    if request_id == 0:
        raise HTTPException(status_code=400, detail="Request ID cannot be 0")

    db_request = db.query(Request).filter(Request.request_id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request
@app.put("/requests/{request_id}", response_model=RequestResponse)
def update_request(request_id: int, request: RequestUpdate, db: Session = Depends(get_db)):
    if request_id == 0:
        raise HTTPException(status_code=400, detail="Request ID cannot be 0")

    db_request = db.query(Request).filter(Request.request_id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.property_id == 0:
        raise HTTPException(status_code=400, detail="Property ID cannot be 0")

    if request.property_id != db_request.property_id:
        db_property = db.query(Property).filter(
            Property.property_id == request.property_id,
            Property.is_active == 1
        ).first()
        if not db_property:
            raise HTTPException(status_code=400, detail="New property not found or inactive")

    for key, value in request.dict().items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)
    return db_request

@app.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    if request_id == 0:
        raise HTTPException(status_code=400, detail="Request ID cannot be 0")

    db_request = db.query(Request).filter(Request.request_id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    db_request.is_active = 0
    db.commit()
    return {"message": "Request marked as inactive"}
