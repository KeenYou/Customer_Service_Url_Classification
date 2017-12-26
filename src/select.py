#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""view twitter dialogs.

   Copyright (c) 2017 Takaaki Hori  (thori@merl.com)

   This software is released under the MIT License.
   http://opensource.org/licenses/mit-license.php

"""

import json
import sys
import six

def get_content_url(atext):
   urls = []
   toks = atext.strip().split(' ')
   for tok in toks:
       if tok.startswith('https:'):
            urls.append(tok)
   ends_with_url = True if toks[-1].startswith('https:') else False
   if len(urls)==0: return None, None
   if len(urls)==1: return urls, ends_with_url
   if len(urls)>=2: return urls, ends_with_url 
    
if six.PY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

if len(sys.argv) < 2:
    print ('usage: view_dialogs.py dialogs.json ...')
    sys.exit(1)

names = {}
for fn in sys.argv[1:]:
    dialog_set = json.load(open(fn,'r'))
    for tid in sorted([int(s) for s in dialog_set.keys()]):
        dialog = dialog_set[str(tid)]
        lang = dialog[0]['lang']
        if lang == 'en':
            for utterance in dialog:
                screen_name = utterance['user']['screen_name']
		if screen_name not in names:
			names[screen_name]=1
		else:
			names[screen_name]+=1

import operator
service_name = max(names.iteritems(), key=operator.itemgetter(1))[0]

print('service_name is ', service_name)

f = open('testapple.tsv','w')

questions = []
urls = []
context = []

for fn in sys.argv[1:]:
    dialog_set = json.load(open(fn,'r'))
    for tid in sorted([int(s) for s in dialog_set.keys()]):
        dialog = dialog_set[str(tid)]
        lang = dialog[0]['lang']
        if lang == 'en':
            if len(dialog)<2: continue
            i=0
            tmpq=None
            tmpurl=None
            tmpcontext=None
            utter1 = dialog[0]
            utter2 = dialog[1]

            if utter1['user']['screen_name'] != service_name and utter2['user']['screen_name']== service_name:
                curls, end_is_url = get_content_url(utter2['text'])
                if curls is None: continue
                elif len(curls)>=2: theurl = curls[0]
                elif len(curls)==1: 
                    if end_is_url: continue
                    else: theurl = curls[0]
		else: continue

                questions.append(utter1['text'])
                urls.append(theurl)
                context.append(utter2['text'])

for i in range(len(questions)):
    f.write(questions[i])
    f.write('\t')
    f.write(urls[i])
    f.write('\t')
    f.write(context[i])
    f.write('\n')

f.close()
