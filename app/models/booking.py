#!/usr/bin/env python

from flask import current_app
from app import db
from app.models.user import User

class Booking(db.Model):
    __tablename__   = 'tblBooking' #What a long table with no relationship
    id              = db.Column(db.Integer, primary_key = True)
    UserId          = db.Column(db.Integer, db.ForeignKey('users.id'))
    BookingID       = db.Column(db.String)
    Locator         = db.Column(db.String(50))
    DFrom           = db.Column(db.String(50))
    Dto             = db.Column(db.String(50))
    DepDate         = db.Column(db.DateTime)
    RetDate         = db.Column(db.DateTime)
    Airline         = db.Column(db.String(50))
    TripType        = db.Column(db.String(50))
    FareType        = db.Column(db.String(50))
    Adt             = db.Column(db.Integer)
    Cnn             = db.Column(db.Integer)
    Inf             = db.Column(db.Integer)
    BaseFare        = db.Column(db.String(50)) #base Fare VarChar? Really?
    Tax             = db.Column(db.String(50))
    Total           = db.Column(db.String(50))
    FareCode        = db.Column(db.String(50))
    MerchantChrge   = db.Column(db.String(50))
    IpAdd           = db.Column(db.String(50))
    Source          = db.Column(db.String(50))
    DistributionCode= db.Column(db.String(50))
    BookingDate     = db.Column(db.DateTime)
    FirstName       = db.Column(db.String(200))
    LastName        = db.Column(db.String(200))
    BookStatus      = db.Column(db.String(50))
    QueStatus       = db.Column(db.String(50))
    PaxName         = db.Column(db.String(100))
    Address1        = db.Column(db.String(200))
    Address2        = db.Column(db.String(200))
    CityProvince    = db.Column(db.String(200))
    emailid         = db.Column(db.String(200))
    agencyAddress   = db.Column(db.String(300))
    Country         = db.Column(db.String(50))
    phone           = db.Column(db.String(20))
    InsPolicyNo     = db.Column(db.String(20))
    InduranceAmt    = db.Column(db.String(10))
    Cabin           = db.Column(db.String(20))
    PNRStatus       = db.Column(db.String(50))
    BaseFare_New    = db.Column(db.Numeric(10,2))
    Tax_New         = db.Column(db.Numeric(10,2))
    Farecode_new    = db.Column(db.Numeric(10,2))
    Total_new       = db.Column(db.Numeric(10,2))
    PNR             = db.Column(db.String(10))
    specialuserid   = db.Column(db.String(200))
    specialuserName = db.Column(db.String(200))
    Removeamt       = db.Column(db.Numeric(18,2))
    ServiceCharge   = db.Column(db.Numeric(18,2))
    FareCode_S      = db.Column(db.Numeric(18,2))
    Upsell          = db.Column(db.Numeric(18,2))
    user            = db.relationship('User', lazy = True, backref = db.backref('bookings', uselist = True))
    
    def __str__(self):
        return '<Booking : id %s PNR %s First Name %s Last Name %s PNR Status %s>'\
        % (self.id, self.PNR, self.FirstName, self.LastName, self.PNRStatus)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'id'                : self.id,
            'BookingID'         : self.BookingID,
            'Locator'           : self.Locator,
            'UserID'            : self.UserId,
            'query'             : {
                'from'  : self.DFrom,
                'to'    : self.Dto,
                'Depart Date'   : self.DepDate,
                'Return Date'   : self.RetDate,
                'Airline'       : self.Airline,
                'TripType'      : self.TripType,
                'FareType'      : self.FareType,
                'Adult'         : self.Adt,
                'Child'         : self.Cnn,
                'Infant'        : self.Inf
            },
            'Price'             : {
                'BaseFare'      : self.BaseFare,
                'Tax'           : self.Tax,
                'Total'         : self.Total,
                'FareCode'      : self.FareCode,
                'MerchantCharge': self.MerchantChrge,
                'BaseFare_New'  : self.BaseFare_New,
                'Tax_New'       : self.Tax_New,
                'Farecode_new'  : self.Farecode_new,
                'Total_new'     : self.Total_new,
                'Removeamt'     : self.Removeamt,
                'ServiceCharge' : self.ServiceCharge,
                'FareCode_S'    : self.FareCode_S,
                'Upsell'        : self.Upsell
            },
            'IP'                : self.IpAdd,
            'Source'            : self.Source,
            'DistributionCode'  : self.DistributionCode,
            'BookingDate'       : self.BookingDate,
            'FirstName'         : self.FirstName,
            'LastName'          : self.LastName,
            'BookStatus'        : self.BookStatus,
            'QueStatus'         : self.QueStatus,
            'Address'           : {
                'PaxName'       : self.PaxName,
                'Address1'      : self.Address1,
                'Address2'      : self.Address2,
                'CityProvince'  : self.CityProvince,
                'emailid'       : self.emailid,
                'agencyAddress' : self.agencyAddress,
                'Country'       : self.Country,
                'phone'         : self.phone,
            },
            'Insurance'         : {
                'InsPolicyNo'   : self.InsPolicyNo,
                'InsuranceAmt'  : self.InduranceAmt, #spell mistake in column name
            },
            'Cabin'             : self.Cabin,
            'PNRStatus'         : self.PNRStatus,
            'PNR'               : self.PNR,
            'specialuserid'     : self.specialuserid,
            'specialuserName'   : self.specialuserName,
       }