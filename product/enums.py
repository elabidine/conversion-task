
from core.enums.general import Visibility
from core.models.flexup_enum import FlexUpEnum as FlexUpEnum
from core.enums.status import Status
from django.utils.translation import gettext_lazy as _

ProductVisibilities = Visibility.allowed_choices(Visibility.PRIVATE, Visibility.PUBLIC)

ProductStatuses = Status.allowed_choices(Status.DRAFT, Status.ACTIVE, Status.PAUSED, Status.EXPIRED, Status.SUSPENDED) # this does not work
# ProductStatuses = [Status.DRAFT, Status.ACTIVE, Status.PAUSED, Status.EXPIRED, Status.SUSPENDED]  - this does not work either

# class ProductStatus(FlexUpEnum):
#     """Product statuses enum class"""
#     description: str
#
#     # name     value                description
#     PENDING =   Status.PENDING,     _('The product is pending internal approval')
#     ACTIVE  =   Status.ACTIVE,      _('The product is available for sale')
#     PAUSED  =   Status.PAUSED,      _('The product is temporarily not available')
#     EXPIRED =   Status.EXPIRED,     _('The product is no longer available for sale')
#     SUSPENDED = Status.SUSPENDED,   _('The product is has been suspended by the system administrator')
#
#     @property
#     def value(self):
#         return str(self._value_)
#
#     @property
#     def label(self):
#         return self._value_.label

class Dimension(FlexUpEnum):
    """List of physical dimensions that a measurement unit can belong to"""
    label: str

    # name     value    label
    TIME      = 'T', _('Time'),
    MASS      = 'M', _('Mass')
    LENGTH    = 'L', _('Length')
    AREA      = 'A', _('Area')
    VOLUME    = 'V', _('Volume')
    DATA      = 'D', _('Data')
    DURATION  = 'R', _('Duration')
    ITEM      = 'I', _('Item')
    WEIGHT    = 'W', _('Weight')
    BANDWITH  = 'B', _('Bandwith')



class SystemUnit(FlexUpEnum):
    """List of physical measurement units provided by the system, allowing conversion between different units of the same dimension"""
    label: str
    symbol: str
    dimension: Dimension
    base_unit: str # the problem with an enum is that we cannot link the base unit to another system SystemUnit
    units_to_base: float
    can_be_priced: bool
    sort_factor: int

  # Name       =  value,  label,                        symbol,               dimension,           base_unit,  units_to_base,  can_be_priced,  sort_factor
    BARREL       =  'BAR',  _('Barrel'),                _('barrel'),          Dimension.VOLUME,    'LIT',      158.9872894,    True,           20,
    BIT          =  'BIT',  _('Binary digit'),          _('bit'),             Dimension.DATA,      'BYT',      0.125,          True,           36,
    B_S          =  'BIS',  _('Bits per second'),       _('bit-s'),           Dimension.BANDWITH,  'GBS',      1,              False,          41,
    BYTE         =  'BYT',  _('Byte'),                  _('byte'),            Dimension.DATA,      'BYT',      1,              True,           36,
    CL           =  'CL',   _('Centiliter'),            _('cl'),              Dimension.VOLUME,    'LIT',      0.01,           True,           21,
    CM           =  'CM',   _('Centimeter'),            _('cm'),              Dimension.LENGTH,    'M',        0.1,            True,           46,
    DAY          =  'DAY',  _('Day'),                   _('day'),             Dimension.DURATION,  'HR',       24,             True,           9,
    DL           =  'DL',   _('Deciliter'),             _('dl'),              Dimension.VOLUME,    'LIT',      0.100000001,    True,           22,
    DOZEN        =  'DOZ',  _('Dozen'),                 _('dozen'),           Dimension.ITEM,      'UNI',      0.083333333,    True,           7,
    FL_OZ_UK     =  'FLK',  _('Fluid ounce (uk)'),      _('fl-oz-uk'),        Dimension.VOLUME,    'LIT',      0.028413063,    True,           23,
    FL_OZ_US     =  'FLU',  _('Fluid ounce (us)'),      _('fl-oz-us'),        Dimension.VOLUME,    'LIT',      0.02957353,     True,           24,
    FT           =  'FT',   _('Foot'),                  _('ft'),              Dimension.LENGTH,    'M',        0.3048,         True,           47,
    FT2          =  'FT2',  _('Square foot'),           _('ft2'),             Dimension.AREA,      'M2',       0.09290304,     True,           55,
    FT3          =  'FT3',  _('Cubic foot'),            _('ft3'),             Dimension.VOLUME,    'LIT',      28.31684685,    True,           25,
    GRAM         =  'GRM',  _('Gram'),                  _('g'),               Dimension.WEIGHT,    'KG',       0.001,          True,           16,
    GALLON_UK    =  'GAK',  _('Gallon (uk)'),           _('gal-uk'),          Dimension.VOLUME,    'LIT',      4.546090126,    True,           26,
    GALLON_US    =  'GAS',  _('Gallon (us)'),           _('gal-us'),          Dimension.VOLUME,    'LIT',      3.785411835,    True,           27,
    GB           =  'GB',   _('Gigabyte'),              _('gb'),              Dimension.DATA,      'BYT',      1000000000,     True,           37,
    GB_S         =  'GBS',  _('Gigabytes per second'),  _('gb-s'),            Dimension.BANDWITH,  'GBS',      1000000000,     False,          42,
    HECT         =  'HEC',  _('Hectare'),               _('hectare'),         Dimension.AREA,      'M2',       10000,          True,           56,
    HR           =  'HR',   _('Hour'),                  _('hr'),              Dimension.DURATION,  'HR',       1,              True,           8,
    INCH         =  'INC',  _('Inch'),                  _('inch'),            Dimension.LENGTH,    'M',        0.0254,         True,           48,
    INCH_3       =  'IN3',  _('Cubic inch'),            _('inch3'),           Dimension.VOLUME,    'LIT',      0.016387064,    True,           28,
    KB           =  'KB',   _('Kilobyte'),              _('kb'),              Dimension.DATA,      'BYT',      1000,           True,           38,
    KB_S         =  'KBS',  _('Kilobytes per second'),  _('kb-s'),            Dimension.BANDWITH,  'GBS',      1000,           False,          43,
    KG           =  'KG',   _('Kilogram'),              _('kg'),              Dimension.WEIGHT,    'KG',       1,              True,           17,
    KM           =  'KM',   _('Kilometer'),             _('km'),              Dimension.LENGTH,    'M',        1000,           True,           49,
    LIT          =  'LIT',  _('Liter'),                 _('l'),               Dimension.VOLUME,    'LIT',      1,              True,           29,
    M            =  'M',    _('Meter'),                 _('m'),               Dimension.LENGTH,    'M',        1,              True,           50,
    M2           =  'M2',   _('Square meter'),          _('m2'),              Dimension.AREA,      'M2',       1,              True,           58,
    M3           =  'M3',   _('Cubic meter'),           _('m3'),              Dimension.VOLUME,    'LIT',      1000,           True,           30,
    MB           =  'MB',   _('Megabyte'),              _('mb'),              Dimension.DATA,      'BYT',      1000000,        True,           39,
    MB_S         =  'MBS',  _('Megabytes per second'),  _('mb-s'),            Dimension.BANDWITH,  'GBS',      1000000,        False,          44,
    MG           =  'MG',   _('Milligram'),             _('mg'),              Dimension.WEIGHT,    'KG',       0.000001,       True,           18,
    MILE         =  'MIL',  _('Mile'),                  _('mile'),            Dimension.LENGTH,    'M',        1609.34,        True,           51,
    MIN          =  'MIN',  _('Minute'),                _('min'),             Dimension.DURATION,  'HR',       0.016666667,    True,           10,
    ML           =  'ML',   _('Milliliter'),            _('ml'),              Dimension.VOLUME,    'LIT',      1,              True,           31,
    MM           =  'MM',   _('Millimeter'),            _('mm'),              Dimension.LENGTH,    'M',        0.001,          True,           52,
    MONTH        =  'MON',  _('Month'),                 _('month'),           Dimension.DURATION,  'HR',       730.5,          True,           11,
    AGE_MO       =  'AMO',  _('Age in months'),         _('month-age'),       None,                'AYR',      12,             False,          59,
    NAUT         =  'NAU',  _('Nautical mile'),         _('nautical-mile'),   Dimension.LENGTH,    'M',        1852,           True,           53,
    NR           =  'NR',   _('Number'),                _('nr'),              Dimension.ITEM,      'UNI',      1,              True,           3,
    PAIR         =  'PAI',  _('Pair'),                  _('pair'),            Dimension.ITEM,      'UNI',      2,              True,           5,
    PERSON       =  'PER',  _('Person'),                _('person'),          Dimension.ITEM,      'UNI',      1,              True,           6,
    PINT_UK      =  'PIK',  _('Pint (uk)'),             _('pint-uk'),         Dimension.VOLUME,    'LIT',      0.568261266,    True,           32,
    PINT_US_DRY  =  'PUD',  _('Pint (us dry)'),         _('pint-us-dry'),     Dimension.VOLUME,    'LIT',      0.473176479,    True,           33,
    PINT_US_LIQ  =  'PUL',  _('Pint (us liquid)'),      _('pint-us-liquid'),  Dimension.VOLUME,    'LIT',      0.550610483,    True,           34,
    QUARTER      =  'QUA',  _('Quarter'),               _('quarter'),         Dimension.DURATION,  'HR',       2191.5,         True,           12,
    SEC          =  'SEC',  _('Second'),                _('s'),               Dimension.DURATION,  'HR',       0.000277778,    True,           13,
    TON          =  'TON',  _('Metric ton'),            _('t'),               Dimension.WEIGHT,    'KG',       1000,           True,           19,
    TB           =  'TB',   _('Terabyte'),              _('tb'),              Dimension.DATA,      'BYT',      1E+12,          True,           40,
    TB_S         =  'TBS',  _('Terabytes per second'),  _('tb-s'),            Dimension.BANDWITH,  'GBS',      1E+12,          False,          45,
    TEN          =  'TEN',  _('Tens'),                  _('tens'),            Dimension.ITEM,      'UNI',      0.1,            True,           4,
    UNIT         =  'UNI',  _('Unit'),                  _('unit'),            Dimension.ITEM,      'UNI',      1,              True,           2,
    WEEK         =  'WEE',  _('Week'),                  _('week'),            Dimension.DURATION,  'HR',       168,            True,           14,
    YARD         =  'YAR',  _('Yard'),                  _('yard'),            Dimension.LENGTH,    'M',        0.9144,         True,           54,
    YARD2        =  'YA2',  _('Square yard'),           _('yard2'),           Dimension.AREA,      'M2',       0.83612736,     True,           57,
    YARD3        =  'YA3',  _('Cubic yard'),            _('yard3'),           Dimension.VOLUME,    'LIT',      764.5548706,    True,           35,
    YEAR         =  'YEA',  _('Year'),                  _('year'),            Dimension.DURATION,  'HR',       8766,           True,           15,
    AGE_YR       =  'AYR',  _('Age in years'),          _('year-age'),        None,                'AYR',      1,              False,          60,

    def __str__(self):
        return str(self.value)  # Ensure this returns a string
