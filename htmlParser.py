import sys
import re
import requests

# The purpose of main() is to test the functions
def main(args):
    with open(args[1]) as infile:
        #print('\n'.join(getTableHeaders(infile.read())))
        tables = get_tables(infile.read(),{'summary':'Results'})
        print(len(tables))
        filterCrit = {'Type':['10-Q','EX-10.1'], 
                'Description':'Complete submission text file'}
        for t in tables:
            headers = get_th(t)
            print(headers)
            filter_table(t,cols=filterCrit)

def filter_table(table,cols={},row={}):
    table = table_to_dicts(table)
    res = []
    for row in table:
        for col in iter(cols):
            if row[col] in cols[col]:
                res.append(row)
    return res

def decode_table(table, removeTH=False):
    res = re.findall(r'<tr.*?/tr>',table,flags=re.DOTALL) 
    for i in range(0,len(res)):
        res[i] = [re.sub(r'<td.*?>|</td>','',x,flags=re.DOTALL).strip()
                for x in re.findall(r'<td.*?/td>',res[i],flags=re.DOTALL)]
    # this is unsafe! needs to be fixed
    if removeTH:
        return res[1:]
    return res

def table_to_dicts(table):
    headers = get_th(table)
    res = re.findall(r'<tr.*?/tr>',table,flags=re.DOTALL)[1:] 
    for i in range(len(res)):
        res[i] = dict(zip(headers, [re.sub(r'<td.*?>|</td>','',x,flags=re.DOTALL).strip()
                for x in re.findall(r'<td.*?/td>',res[i],flags=re.DOTALL)]))
    return res

def get_td(table):
    res = re.findall(r'<td.*?/td>',table,flags=re.DOTALL)
    for i in range(0,len(res)):
        res[i] = re.sub(r'<td.*?>|</td>','',res[i],flags=re.DOTALL)
    return res

def get_tr(table):
    res = re.findall(r'<tr.*?/tr>',table,flags=re.DOTALL)
    for i in range(0,len(res)):
        res[i] = re.sub(r'<tr.*?>|</tr>','',res[i],flags=re.DOTALL)
    return res

def get_th(s):
    res = re.findall(r'<th.*?</th>',s,flags=re.DOTALL)
    for i in range(0,len(res)):
        res[i] = re.sub(r'<.*?>','',res[i],flags=re.DOTALL)
    return res

def get_tables(s, tags={}):
    if not tags:
        return re.findall(r'<table.*?</table>',s,flags=re.DOTALL)
    res = []
    for table in re.findall(r'<table.*?</table>',s,flags=re.DOTALL):
        if check_tags(table,tags):
            res.append(table)
    return res
            
def has_attr(s,tags={}):
    for key in iter(tags):
        tmp='{}="{}".*?>'.format(key,tags[key],flags=re.DOTALL)
        pat=re.compile(tmp)
        if not re.search(pat,s):
            # print('tags not found')
            return False
    return True

def get_elements(s, tag, attr={}, contains=''):
    if tag in ['img']:
        pat = re.compile('<{}.*?>'.format(tag,tag),flags=re.DOTALL)
    else:
        pat = re.compile('<{}.*?</{}>'.format(tag,tag),flags=re.DOTALL)
    
    res = []
    for elem in re.findall(pat,s):
        if has_attr(elem,attr) and has_text(elem,contains):
            res.append(elem)
    return res

# def get_element_texts(s, text, attr={}):


def has_text(s,text):
    return re.search(re.compile(text),s)

def is_link(s):
    if re.match(r'<a.*?</a>',s):
        return True
    return False

def get_link_text(s):
    res = re.findall(r'<a.*?/a>',s,flags=re.DOTALL)
    for i in range(0,len(res)):
        res[i] = re.sub(r'<a.*?>|</a>','',res[i],flags=re.DOTALL)
    return res
    
def get_ul_as_list(s):
    res = re.findall(r'<li.*?/li>',s,flags=re.DOTALL)
    for i in range(0,len(res)):
        res[i] = re.sub(r'<li.*?>|</li>','',res[i],flags=re.DOTALL)
    return res

def get_link(s):
    m = re.search(r'href=".*?"',s)
    if m:
        return s[m.start()+6:m.end()-1]
    m = re.search(r'src=".*?"',s)
    if m:
        return s[m.start()+5:m.end()-1]

if __name__ == '__main__':
    main(sys.argv)
