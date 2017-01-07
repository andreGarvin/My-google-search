from bs4 import BeautifulSoup as soup
import requests
import json
import sys
import os


# history dictionary
history = {
    'searchs': [],
    '_len_': 0,
    'bookmarks': {
        'pins': [],
        '_len_': 0
    }
}

with open('.~history.json', 'r') as f:
    
    history = json.loads( f.read() )
    f.close()


def Google( query ):
    
    resp = {
        'links': [],
        'count': 0
    }

    Google_url = 'https://www.google.com/search?q='

    request = requests.get( Google_url + query )
    source = soup( request.content )
    
    try:
        for l, i in zip( source.find_all('h3', { 'class': 'r' }), source.find_all('span', { 'class': 'st' })):
            for a in l:
                
                resp['count'] += 1
                if resp['count'] <= 5:
                    resp['links'].append({ 'title': a.text, 'url_': 'https://www.google.com' + a.get('href'), 'info': i.text })
    except:
        resp['error_message'] = 'No results found.'
        resp['status'] = False
        
        history['searchs'].append({ 'query': query, 'results': resp['count'] })
        print resp
        
    
    history['searchs'].append({ 'query': query, 'results': resp['count'] })
    resp['status'] = True
    return resp


req = sys.argv[1:]

def main( data ):
    
    if data[0] == '-h':
        os.system('clear')
        
        for i in history['searchs']:
            print '\n #', i['query']
        
        print '\n search:'
        req = raw_input('=> ')
        
        if req != 'q':
            Google( req )    
    
        else:
            os.system('clear')
            print '<Goodbye>'

    
    elif data[0] == '-b':
        
        if len( data ) >= 2:
            
            print history['bookmarks']['_len_']
            
            for p in history['bookmarks']['pins']:
                print '\n #', p['pin']
                print '\t url: ', p['url']
        
        history['bookmarks']['pins'].append({ 'pin': data[1], 'url': 'https://www.google.com/search?q=' + '+'.join( data[1:] ) })
        history['bookmarks']['_len_'] += 1    
    
    elif data[0] == '-q':
        if len( data[1:] ) > 1:
            data = '+'.join(data[1:])
        else:
            data = data[1]
    
        resp = Google( data )
    
        if resp['status']:
        
            os.system('clear')
            print 'Results: ', resp['count']
            
            
            for i in resp['links']:
                print '\n=> ', i['title'], ': ', i['info']
                print '\t ~ ', i['url_']
        
        else:
            print resp['error_message']

main( req )


with open('.~history.json', 'w') as f:
    
    f.write( json.dumps( history ) )
    f.close()
