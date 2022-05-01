import time
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    BigInteger,
    DateTime,
    Numeric,
    null,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from enum import Enum


class Inventory_Ticket_Status(Enum):
    reentry = "REENTRY"
    entry = "ENTRY"


class Ticket_Approval_Status(Enum):
    reentry = "REENTRY"
    entry = "ENTRY"


class Delivery_Ticket_Status(Enum):
    delivered = "DELIVERED"
    in_transit = "IN_TRANSIT"


class Generic_Ticket_Status(Enum):
    inventory = "INVENTORY"
    assigned = "ASSIGNED"
    out_for_delivery = "OUT_FOR_DELIVERY"


class UserType(Enum):
    manager = "MANAGER"
    dispatch = "DISPATCH"
    customer = "CUSTOMER"
    brooker = "BROKER"
    worker = "WORKER"


Base = declarative_base()


class Customers(Base):
    __tablename__ = "customers"
    customerId = Column(Integer, primary_key=True, autoincremenet=True)
    name = Column(String, nullable=False)


class Users(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, autoincremenet=True)
    userType = Column(Enum(UserType), nullable=False)
    username = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()))


class ShipperEvents(Base):
    __tablename__ = "shipperevents"
    shipperEventId = Column(Integer, primary_key=True, autoincremenet=True)
    shipperId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(String, ForeignKey(Users.userId))
    companyName = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False, default=int(time.time()))


class ConsigneeEvents(Base):
    __tablename__ = "consigneeevents"
    consigneeEventId = Column(Integer, primary_key=True, autoincremenet=True)
    consigneeId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(String, ForeignKey(Users.userId))
    companyName = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False, default=int(time.time()))


class TicketEvents(Base):
    __tablename__ = "ticketevents"
    ticketEventId = Column(Integer, primary_key=True, autoincremenet=True)
    ticketId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    shipperEventId = Column(Integer, ForeignKey(ShipperEvents.shipperEventId))
    consigneeEventId = Column(Integer, ForeignKey(ConsigneeEvents.consigneeEventId))
    userId = Column(String, ForeignKey(Users.userId))
    customerId = Column(Integer, ForeignKey(Customers.customerId))
    barcodeNumber = Column(Integer)
    houseReferenceNumber = Column(Integer)
    orderS3Link = Column(String)
    weight = Column(Integer)
    claimedNumberOfPieces = Column(Integer)
    BOLNumber = Column(Integer)
    specialServices = Column(String)
    specialInstructions = Column(String)


class GenericMilestones(Base):
    __tablename__ = "genericmilestones"
    milestoneId = Column(Integer, primary_key=True, autoincremenet=True)
    timestamp = Column(Integer, nullable=False)
    ticketEventId = Column(Integer, default=int(time.time()))
    customerId = Column(Integer, ForeignKey(Customers.customerId))
    userId = Column(String, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status), ForeignKey(Customers.customerId))


class InventoryMilestones:
    __tablename__ = "inventorymilestones"
    milestoneId = Column(Integer, primary_key=True, autoincremenet=True)
    timestamp = Column(Integer, nullable=False)
    ticketEventId = Column(Integer, default=int(time.time()))
    customerId = Column(Integer, ForeignKey(Customers.customerId))
    userId = Column(String, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status), ForeignKey(Customers.customerId))
    approvalStatus = Column(
        Enum(Ticket_Approval_Status), ForeignKey(Customers.customerId)
    )


class DeliveryMilestones:
    __tablename__ = "deliverymilestones"
    milestoneId = Column(Integer, primary_key=True, autoincremenet=True)
    timestamp = Column(Integer, nullable=False)
    ticketEventId = Column(Integer, default=int(time.time()))
    customerId = Column(Integer, ForeignKey(Customers.customerId))
    userId = Column(String, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status), ForeignKey(Customers.customerId))
    approvalStatus = Column(
        Enum(Ticket_Approval_Status), ForeignKey(Customers.customerId)
    )



CREATE TABLE IF NOT EXISTS DeliveryMilestones (
    milestoneId INT,
    timestamp INT,
    ticketEventId INT,
    customerId INT,
    userId INT,
    ticketStatus DELIVERY_TICKET_STATUS,
    approvalStatus TICKET_APPROVAL_STATUS,
    PODLink VARCHAR(50),
    signatureLink VARCHAR(50),
    picture1Link VARCHAR(50),
    picture2Link VARCHAR(50),
    picture3Link VARCHAR(50),
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
  );


class GeonameCountry(GeonameBase):
    __tablename__ = "geonamecountry"

    iso = Column(String(2), primary_key=True)
    iso3 = Column(String(3), nullable=False)
    iso_numeric = Column(Integer, nullable=False)
    fips = Column(String(2), nullable=False)
    country = Column(String(255), nullable=False)
    capital = Column(String(255), nullable=False)
    area_in_sq_km = Column(Integer)
    population = Column(Integer, nullable=False)
    continent = Column(String(255), nullable=False)
    tld = Column(String(3), nullable=False)
    currency_code = Column(String(3), nullable=False)
    currency_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    postal_code_format = Column(String(255), nullable=False)
    postal_code_regex = Column(String(255), nullable=False)
    languages = Column(String(255), nullable=False)
    geonameid = Column(Integer)
    neighbours = Column(String(255), nullable=False)
    equivalent_fips_code = Column(String(255), nullable=False)


class GeonameTimezone(GeonameBase):
    __tablename__ = "geonametimezone"
    __repr__ = simple_repr("timezone_id")

    # the timezone id (see file timeZone.txt) varchar(40)
    # (Renamed from timezone)
    timezone_id = Column(String(40), primary_key=True)

    country_code = Column(String(2), nullable=False)
    gmt_offset = Column(Numeric(3, 1), nullable=False)
    dst_offset = Column(Numeric(3, 1), nullable=False)
    raw_offset = Column(Numeric(3, 1), nullable=False)


class GeonameFeature(GeonameBase):
    __tablename__ = "geonamefeature"
    __repr__ = simple_repr("name")

    # see http://www.geonames.org/export/codes.html, varchar(10)
    feature_code = Column(String(10), primary_key=True)

    # see http://www.geonames.org/export/codes.html, char(1)
    feature_class = Column(String(1), nullable=False)

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)


class Geoname(GeonameBase):
    __tablename__ = "geoname"
    __repr__ = simple_repr("name")

    # integer id of record in geonames database
    geonameid = Column(Integer, primary_key=True)

    # name of geographical point (utf8) varchar(200)
    name = Column(String(200), nullable=False)

    # name of geographical point in plain ascii characters, varchar(200)
    asciiname = Column(String(200), nullable=False)

    # alternatenames, comma separated varchar(5000)
    alternatenames = Column(Text, nullable=False)

    # latitude in decimal degrees (wgs84)
    # latitude = Column(Numeric(10, 7), nullable=False)

    # longitude in decimal degrees (wgs84)
    # longitude = Column(Numeric(10, 7), nullable=False)

    # Custom. A point made from `latitude` and `longitude`.
    # SRID #4326 = WGS84
    point = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    feature_code = Column(String(10), ForeignKey(GeonameFeature.feature_code))
    feature = relationship(GeonameFeature)

    # ISO-3166 2-letter country code, 2 characters
    country_code = Column(String(2), ForeignKey(GeonameCountry.iso))
    country = relationship(GeonameCountry)

    # alternate country codes, comma separated, ISO-3166 2-letter country
    # code, 60 characters
    cc2 = Column(String(60), nullable=False)

    # fipscode (subject to change to iso code), see exceptions below, see
    # file admin1Codes.txt for display names of this code; varchar(20)
    admin1_code = Column(String(20), nullable=False)

    # code for the second administrative division, a county in the US, see
    # file admin2Codes.txt; varchar(80)
    admin2_code = Column(String(80), nullable=False)

    # code for third level administrative division, varchar(20)
    admin3_code = Column(String(20), nullable=False)

    # code for fourth level administrative division, varchar(20)
    admin4_code = Column(String(20), nullable=False)

    # bigint (8 byte int)
    population = Column(BigInteger, nullable=False)

    # in meters, integer
    elevation = Column(Integer)

    # digital elevation model, srtm3 or gtopo30, average elevation
    # of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in
    # meters, integer. srtm processed by cgiar/ciat.
    dem = Column(Integer, nullable=False)

    # (Renamed from timezone)
    timezone_id = Column(String(40), ForeignKey(GeonameTimezone.timezone_id))
    timezone = relationship(GeonameFeature)
