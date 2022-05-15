# ########################################################################
# Disclaimer:
# Code for example use only, not for production use
# This code has not been thoroughly tested under all conditions so,
# please do your own verification before using this code.
#
# Amazon Web Services makes no warranties, express or implied, in this document.
# Amazon Web Services (AWS) may have patents, patent applications, trademarks,
# copyrights, or other intellectual property rights covering subject matter in
# this document. Except as expressly provided in any written license agreement
# from AWS, our provision of this document does not give you any license to these
# patents, trademarks, copyrights, or other intellectual property. The descriptions
# of other companies products in this document, if any, are provided only as a
# convenience to you. Any such references should not be considered an endorsement
# or support by AWS. AWS cannot guarantee their accuracy, and the products may
# change over time. Also, the descriptions are intended as brief highlights to aid
# understanding, rather than as thorough coverage. For authoritative descriptions
# of these products, please consult their respective manufacturers.
# Copyright © 2022 Amazon Web Services, Inc. and/or its affiliates. All rights reserved.
# ########################################################################

import json
import boto3
from datetime import date,datetime


clientShd = boto3.client('health')

def lambda_handler(event, context):
    eventTypeCodes = []
    
    nextTokenAvailable = True
    nextToken = None
    
    while nextTokenAvailable == True:
        if(nextToken):
            responseEventTypeCodes = clientShd.describe_event_types(
                    filter={
                        'eventTypeCategories': [
                            'issue',
                        ]
                    },
                    maxResults=100,
                    nextToken=nextToken
                )
            eventTypeCodes.append(responseEventTypeCodes.get("eventTypes"))
        else:
            responseEventTypeCodes = clientShd.describe_event_types(
                    filter={
                        'eventTypeCategories': [
                            'issue',
                        ]
                    },
                    maxResults=100
                )
            eventTypeCodes.append(responseEventTypeCodes.get("eventTypes"))
        
        nextToken = responseEventTypeCodes.get("nextToken")
        
        if(nextToken != None):
            nextTokenAvailable = True
        else:
            nextTokenAvailable = False
            
    # print(eventTypeCodes)
   
    bodyJson = {}
    bodyJson["message"] = "Succeeded"
    bodyJson["eventTypeCodes"] = eventTypeCodes

    return {
        'statusCode': 200,
        'body': json.dumps(bodyJson, default=str)
    }
    
