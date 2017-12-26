# Customer_Service_Url_Classification

Cusotmer service staffs uses FAQ urls to answer customer questions. We create a task that classifies a customer question/inquiry 
into specific FAQ pages.

The dataset is based on the DSTC6 end-to-end conversational modeling data collection code. But we use restrictions to collect the desired dataset:

1. First utterance in the dialogue is customer utterance
2. Second utterance is the response from the customer service, which contains an FAQ url.
