
from django.utils.translation import gettext_lazy as _
from ..models.flexup_enum import FlexUpEnum

class Visibility(FlexUpEnum):
    """ Determines if the account is visible by other accounts in the public directory. Only accounts with a visibility of 'Public' will be visible in the public directory. Private can we found by typing the account code in the search bar. Offline accounts are not visible in the public directory, they are only visible in the account that created it. """
    label: str
    symbol: str

    # name  =  value,  label,         symbol
    PRIVATE =  'R',    _('Private'),  '🔒'     # Online: 1 or more member
    PUBLIC  =  'B',    _('Public'),   '🌍'     # Online: 1 or more member
    LOCAL =    'L',    _('Local'),    '📍'     # Offline: no member

V = Visibility


class Focus(FlexUpEnum):
    '''Focuses enum class'''
    label: str
    symbol: str
    color: str

    # name    value      label              symbol   color
    NORMAL   = 'N',     _('Normal'),        '',      '#3a60b1'
    STARRED  = 'S',     _('Starred'),       '⭐',   '#f9c74f'
    ARCHIVED = 'A',     _('Archived'),      '📦',   '#9ec1c7'

F = Focus

class FocusGroup(FlexUpEnum):
    '''Focus groups enum class'''
    label: str
    focuses: list[Focus]

    # name     value  label            focuses
    DEFAULT  =  'D',  _('Default'),    [F.NORMAL, F.STARRED]
    NORMAL   =  'N',  _('Normal'),     [F.NORMAL]
    STARRED  =  'S',  _('Starred'),    [F.STARRED]
    ARCHIVED =  'A',  _('Archived'),   [F.ARCHIVED]
    ALL      =  'L',  _('All'),        [F.NORMAL, F.STARRED, F.ARCHIVED]


class ContentOrigin(FlexUpEnum):
    '''Origins enum class'''
    label: str
    symbol: str

    # name     value    label            symbol
    SYSTEM     = 'S',   _('System'),     '🛡️'
    COMMUNITY  = 'C',   _('Community'),  ''
