#from account.enums import MemberRole
from core.models.flexup_enum import FlexUpEnum
from django.utils.translation import gettext_lazy as _

#Trans = [MemberRole.ADMIN, MemberRole.EDITOR]
#Admin = [MemberRole.ADMIN]
#Sys  =  []


class Domain(FlexUpEnum):
    """ This is the list of all the key domain objects that are used in the system. """
    label: str
    plural: str
    class_name: object | str # is this a class or a string?
    #rights: list[MemberRole] 

    # name                      =  value,    label,                              plural,                              class_name,                    #rights,       # Additional sub-forms to show in main form (* see below)
    ACCOUNT                     =  'AC',     _('Account'),                       _('Accounts'),                       'Account',                     #Admin         # sections: individual | legal entity | grouping | sub-account
    ACCOUTING_DOCUMENT          =  'AD',     _('Accouting document'),            _('Accouting documents'),            'AccoutingDocument',           #Trans         # sections: order, commitment, payment, ...
    CHARTER                     =  'CH',     _('Charter'),                       _('Charters'),                       'Charter',                     #Admin         #
    COMMITMENT                  =  'CM',     _('Commitment'),                    _('Commitments'),                    'Commitment',                  #Trans         # related order, payment, tranches, lettering
    CONTRACT                    =  'CO',     _('Contract'),                      _('Contracts'),                      'Contract',                    #Trans         # tabs: orders, available products, available payment structures, default products, default payment structures, contract status log
    CONSTITUENT                 =  'CN',     _('Constituent'),                   _('Constituents'),                   'Constituent',                 #Admin         #
    CONTRACT_PAYMENT_STRUCTURE  =  'CS',     _('Contract payment structure'),    _('Contract payment structures'),    'ContractPaymentStructure',    #Admin         #
    CONTRACT_PRODUCT            =  'CP',     _('Contract product'),              _('Contract products'),              'ContractProduct',             #Trans         #
    CONTRACT_TEMPLATES          =  'CT',     _('Contract template'),             _('Contract templates'),             'ContractTemplate',            #Sys           # sections: parameters
    CUSTODIAN                   =  'CU',     _('Custodian'),                     _('Custodians'),                     'Custodian',                   #Sys           # sections: wallets ; tabs: pockets
    GROUPING                    =  'GR',     _('Grouping'),                      _('Groupings'),                      'Grouping',                    #Admin         #
    INDIVIDUAL                  =  'IN',     _('Individual'),                    _('Individuals'),                    'Individual',                  #Admin         #
    INTEREST_PAYMENT_TERM       =  'IP',     _('Interest payment term'),         _('Interest payment terms'),         'InterestPaymentTerm',         #Trans         #
    LEGAL_ENTITY                =  'LE',     _('Legal entity'),                  _('Legal entities'),                 'LegalEntity',                 #Admin         #
    LETTERING                   =  'LT',     _('Lettering'),                     _('Letterings'),                     'Lettering',                   #Trans         # related commitment & payment
    MEMBER                      =  'ME',     _('Account member'),                _('Account members'),                'Member',                      #Admin         # sections: user + individual
    MY_PAYMENT_TERM             =  'MP',     _('My payment term'),               _('My payment terms'),               'MyPaymentTerm',               #Trans         # related primary payment term, interest payment term & residue payment term
    ORDER                       =  'OR',     _('Order'),                         _('Orders'),                         'Order',                       #Trans         # related contract, order items, order status log, tranches, commitments, lettering
    ORDER_ITEM                  =  'OI',     _('Order item'),                    _('Order items'),                    'OrderItem',                   #Trans         # tabs: product, delivery status log
    PAYMENT                     =  'PA',     _('Payment'),                       _('Payments'),                       'Payment',                     #Trans         #
    PAYMENT_STRUCTURE           =  'PS',     _('Payment structure'),             _('Payment structures'),             'PaymentStructure',            #Trans         # related payment terms
    PAYMENT_TERM                =  'PT',     _('Payment term'),                  _('Payment terms'),                  'PaymentTerm',                 #Trans         # → only visible inside the payment term form
    POCKET                      =  'PO',     _('Pocket'),                        _('Pockets'),                        'Pocket',                      #Admin         #
    PRIMARY_PAYMENT_TERM        =  'PP',     _('Primary payment term'),          _('Primary payment terms'),          'PrimaryPaymentTerm',          #Trans         #
    PRODUCT                     =  'PR',     _('Product'),                       _('Products'),                       'Product',                     #Trans         #
    RESIDUE_PAYMENT_TERM        =  'RP',     _('Residue payment term'),          _('Residue payment terms'),          'ResiduePaymentTerm',          #Trans         #
    RESOLUTION                  =  'RE',     _('Resolution'),                    _('Resolutions'),                    'Resolution',                  #Admin         #
    STATUS_LOG                  =  'SL',     _('Status log'),                    _('Status logs'),                    'StatusLog',                   #Sys           #
    SUBACCOUNT                  =  'SA',     _('Subaccount'),                    _('Subaccounts'),                    'Subaccount',                  #Trans         #
    THIRD_PARTY                 =  'TP',     _('Third party'),                   _('Third parties'),                  'ThirdParty',                  #Trans         #
    TRANCHE                     =  'TR',     _('Tranche'),                       _('Tranches'),                       'Tranche',                     #Trans         #
    USER                        =  'US',     _('User'),                          _('Users'),                          'User',                        #Sys           #
    WALLET                      =  'WA',     _('Wallet'),                        _('Wallets'),                        'Wallet',                      #Admin         #
    UNSPECIFIED                 =  'UN',     _('Unspecified'),                   _('Unspecified'),                    'Unspecified',                 #Trans         #

    # The main form contains the domain specific field and properties. In some cases, the main form contains sub-forms related to other related domains. Sub-forms can as a section in the main form (ie. scroll down to see it) or as separate tabs
