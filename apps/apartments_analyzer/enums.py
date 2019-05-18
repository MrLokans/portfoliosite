import enum


class BulletinStatusEnum(enum.Enum):
    INACTIVE = 0
    ACTIVE = 1


class BulletinType(enum.Enum):
    FOR_RENT = "RENTED"
    FOR_SELL = "SOLD"
