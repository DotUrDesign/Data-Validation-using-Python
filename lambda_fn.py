import json

burger_sizes = ['single', 'double', 'triple']
burger_franchises = ['best burger', 'burger palace', 'flaming burger']
best_burger_types = ['plain', 'cheese', 'bacon']
burger_palace_types = ['fried egg', 'fried pickle', 'fried green tomatoes']
flaming_burger_types = ['chilli', 'jalapeno', 'peppercorn']

def validate_order(slots):
    # Validate BurgerSize
    # 1. Check whether there exists any slot named as 'BurgerSize'
    if not slots['BurgerSize']:
        print('Validating BurgerSize slot')
        return {
            'isValid' : False,
            'invalidSlot' : 'BurgerSize'
        }

    # 2. Now check whether the customer typed 'BurgerSize' exists in the list of the array of the 'BurgerSize'
    if slots['BurgerSize']['value']['originalValue'].lower() not in burger_sizes :
        print('Invalid BurgerSize')
        return {
            'isValid' : False,
            'invalidSlot' : 'BurgerSize',
            'message' : 'Please select a {} burger size.'.format(", ".join(burger_sizes))  
                # {} denotes a dynamic placeholder which is to be filled later and format is the method which is used to fill the dynamic placeholder and join operation will the join all the contents of the array burger_sizes. So, the end result will be -> "Please select a single, double, triple burger size."
        }
    
    # Validate BurgerFranchise
    # 1. check whether the slot of BurgerFranchise is valid or not
    if not slots['BurgerFranchise']:
        print('Vaidating BurgerFranchise slot')
        return {
            'isValid' : False,
            'invalidSlot' : 'BurgerFranchise'
        }
    
    # 2. check whether the user's typed BurgerFranchise is present in the list of BurgerFranchise or not
    if slots['BurgerFanchise']['value']['originalValue'].lower() not in burger_franchises :
        print('Invalid BurgerFranchise')
        return {
            'isValid' : False,
            'invalidSlot' : 'BurgerFranchise',
            'message' : 'Please select from {} burger franchises'.format(", ".join(burger_franchises))
        }
    
    # Validate BurgerType
    # 1. check whether the slot of BurgerFranchise is valid or not
    if not slots['BurgerType']:
        print('Vaidating BurgerType slot')
        return {
            'isValid' : False,
            'invalidSlot' : 'BurgerType'
        }
    
    # Validate BurgerType for BurgerFranchise
    # BurgerFranchise - best burger
    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'best burger':
        if slots['BurgerType']['value']['originalValue'].lower() not in best_burger_types:
            print('Invalid BurgerType for Best burger')
            return {
                'isValid' : False,
                'invalidSlot' : 'BurgerType',
                'message' : 'Please select a best burger of {}'.format(", ".join(best_burger_types))
            }
        
    # BurgerFranchise - burger palace
    if slots['BurgerFranchise']['value']['originalValue'] == 'burger palace':
        if slots['BurgerType']['value']['originalValue'].lower() not in burger_palace_types:
            print('Invalid burger type for burger palace')
            return {
                'isValid' : False,
                'invalidSlot' : 'BurgerType',
                'message' : 'Please select a valid Burger palace type of {}.'.format(", ".join(burger_palace_types))
            }

    # BurgerFranchise - flaming burger   
    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'flaming burger':
        if slots['BurgerType']['value']['originalValue'].lower() not in flaming_burger_types:
            print('Invalid BurgerType for Flaming Burger')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'message': 'Please select a Flaming Burger type of {}.'.format(", ".join(flaming_burger_types))
            }
        
    # Valid order
    return {'isValid' : True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState" :{
                        "dialogAction" : {
                            "slotTooElicit" : order_validation_result['invalidSlot'],
                            "type" : "ElicitSlot"
                        },

                        "intent" : {
                            "name" : intent,
                            "slots" : slots
                        }
                    },
                    "messages" : [
                        {
                            "ContentType" : "PlainText",
                            "content" : order_validation_result['message']
                        }
                    ]
                }
            # if message does not exists
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        # if isValid is true
        else:
            response = {
                "sessionState" : {
                    "dialogAction" : {
                        "type" : "Delegate"
                    },
                    "intent" : {
                        "name" : intent,
                        "slots" : slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response