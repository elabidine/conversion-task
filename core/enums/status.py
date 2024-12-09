
from core.models.flexup_enum import FlexUpEnum
from django.utils.translation import gettext_lazy as _

class Status(FlexUpEnum):
    """Generic status enum class"""
    label: str
    symbol: str
    color: str   # success, info, warning, danger, primary, secondary, dark
    description: str
    # name            =  value,  label,                  symbol,  color,        description
    NEW               =  'NW',   _('New'),               '🆕',     'info',       _('same as draft but has never been sent. Can still be deleted. Once sent you can no longer delete an object.')
    DRAFT             =  'DR',   _('Draft'),             '📄',     'secondary',  _('order/contract has not yet been confirmed/signed')
    PENDING           =  'PE',   _('Pending'),           '🕒',     'warning',    _('order/contract has been sent but not yet confirmed')
    REJECTED          =  'RJ',   _('Rejected'),          '🚫',     'info',       _('order/contract has been rejected')
    RETRACTED         =  'RT',   _('Retracted'),         '🔙',     'info',       _('order/contract has been retracted')
    SIGNED            =  'SI',   _('Signed'),            '🖊️',     'success',    _('contract has been signed')
    CONFIRMED         =  'CF',   _('Confirmed'),         '🔵',     'success',    _('order has been confirmed')
    NOT_STARTED       =  'NS',   _('Not started'),       '🔨',     'info',       _('delivery has not yet started')
    IN_PROGRESS       =  'IP',   _('In progress'),       '🚚',     'success',    _('delivery is ongoing')
    PAUSED            =  'PS',   _('Paused'),            '⏸️',     'primary',    _('contract order delivery has been paused jointly by all parties')
    COMPLETED         =  'CP',   _('Completed'),         '✅',     'warning',    _('delivery hs been completed')
    CLAIMS            =  'CA',   _('Claims'),            '❗',     'warning',    _('claims have been made by client following an order delivery')
    ACCEPTED          =  'AP',   _('Accepted'),          '👍',     'success',    _('delivery has been accepted')
    PENDING_DUE_DATE  =  'PU',   _('Pending due date'),  '🕘📆',   'warning',    _('order/contract has been sent but not yet confirmed')
    PENDING_AMOUNT    =  'PA',   _('Pending amount'),    '🕘💸',   'warning',    _('order/contract has been sent but not yet confirmed')
    NO_DUE_DATE       =  'ND',   _('No due date'),       '⌛',     'info',       _('order/contract has been sent but not yet confirmed')
    UPCOMING          =  'UP',   _('Upcoming'),          '🔜',     'info',       _('order/contract has been sent but not yet confirmed')
    OVERDUE           =  'OD',   _('Overdue'),           '🚨',     'danger',     _('order/contract has been sent but not yet confirmed')
    SCHEDULED         =  'SC',   _('Scheduled'),         '📅',     'info',       _('order/contract has been sent but not yet confirmed')
    ACTIVE            =  'AC',   _('Active'),            '🟢',     'success',    _('record is active')
    CANCELLED         =  'CN',   _('Cancelled'),         '❌',     'secondary',  _('order/contract has been cancelled by the parties')
    CLOSED            =  'CL',   _('Closed'),            '🛑',     'secondary',  _('was active but set to no longer active by the user')
    CONVERTED         =  'CV',   _('Converted'),         '🔄',     'success',    _('commitment has been converted into tokens')
    DELETED           =  'DE',   _('Deleted'),           '🗑️',     'danger',     _('record was deleted before being sent')
    EXPIRED           =  'EX',   _('Expired'),           '⌛',     'secondary',  _('product/contract has expired')
    FROZEN            =  'FZ',   _('Frozen'),            '❄️',     'info',       _('the order items and tranches are frozen due to the order status not being in a state that allows for changes')
    PAID              =  'PD',   _('Paid'),              '💵',     'success',    _('payment has been made')
    PAYABLE           =  'PY',   _('Payable'),           '💰',     'info',       _('commitment has been processed by resolution and a payable amount has been calculated')
    RESOLVED          =  'RS',   _('Resolved'),          '✔️',     'success',    _('commitment has been processed by resolution but the payable amount is 0')
    SUSPENDED         =  'SP',   _('Suspended'),         '⛔',     'danger',     _('record has been suspended')
    TERMINATED        =  'TM',   _('Terminated'),        '✖️',     'secondary',  _('contract has been terminated')

    def __str__(self):
        return str(self.label)
    
StatusShortList = Status.allowed_choices(Status.PENDING, Status.ACTIVE, Status.CLOSED, Status.SUSPENDED)


class Action(FlexUpEnum):
    """Generic actions enum class"""
    label: str

    # name     =  value,    label                                                               
    DELETE     =  "DE",     _("Delete")    # this does delete but makes it invisible for users  
    SEND       =  "SD",     _("Send")                                                           
    RETRACT    =  "RT",     _("Retract")                                                        
    REJECT     =  "RJ",     _("Reject")                                                         
    MODIFY     =  "MD",     _("Modify")                                                         
    SIGN       =  "SG",     _("Sign")                                                           
    CONFIRM    =  "CO",     _("Confirm")                                                        
    CANCEL     =  "CX",     _("Cancel")                                                         
    START      =  "ST",     _("Start")                                                          
    PAUSE      =  "PS",     _("Pause")                                                          
    RESUME     =  "RE",     _("Resume")                                                         
    COMPLETE   =  "CP",     _("Complete")                                                       
    CLAIM      =  "CL",     _("Claim")                                                          
    ACCEPT     =  "AC",     _("Accept")                                                         
    TERMINATE  =  "TR",     _("Terminate")                                                      

    def __str__(self):
        return str(self.label)  # Ensure this returns a string


class ActionType(FlexUpEnum):
    """Generic action types enum class"""
    label: str
    is_immediate: bool

    # name     value    label              is_immediate
    UNILATERAL  =  'U',  _('Unilateral'),  True
    JOINT           =  'J',  _('Joint'),       False
    SYSTEM          =  'S',  _('System'),      True

    def __str__(self):
        return str(self.value)  # Ensure this returns a string
