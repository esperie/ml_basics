from datetime import datetime, date, time, timedelta
from pydantic import BaseModel, Field


class QueryBase(BaseModel):
	area_sqm: int = Field(title='Area in square meters', default=80)
	area_type: str = Field(..., title='Area Type: Strata, Land')
	sale_date: date = Field(..., title='Date of Intended Sale')
	is_leasehold: bool = Field(..., title='1 if leasehold, 0 if freehold.')
	property_type: str = Field(
		...,
		title='Choose from: Condominium, Apartment, Executive Condominium')
	completion_date: int = Field(title='Year of completion', default=2023)
	sale_type: str = Field(
		..., title='Choose from: Resale, Sub Sale, New Sale')
	purchaser_address: str = Field(..., title='Choose from: HDB, N.A, Private')
	postal_code: str = Field(..., title='6-digit postal code')
