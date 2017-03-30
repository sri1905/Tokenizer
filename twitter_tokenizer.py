import re
#do not process the units which start with "done" tag
done = '<///>'
#done pattern
donepat = '^(<///>|</s>|<s>)(.*)'

def apos(list1):
    # only for .*+"'"+alpha (they've)
    tokens = []

    for unit in list1:
        if "'" in unit:
            M = re.match('(.*[a-zA-Z])(\'[a-zA-Z]+)', unit)
            if M:
                tokens.append(M.group(1))
                tokens.append(done+M.group(2))
                continue     
        tokens.append(unit)

    return tokens

def asciiemo(list1):
    emo = [':)', ':-)', ':P', ':-P', ':D', ':-D', ';)', ';-)']
    tokens = []

    for unit in list1:
        for e in emo:
            if e in unit:
                new = unit.replace(e, ' '+e+' ')
                for tok in new.split():
                    if e in tok:
                        tokens.append(done+tok)
                    else:
                        tokens.append(tok)
                    continue
        tokens.append(unit)

    return tokens

def EAemo(list1):
    tokens = []
    flag = 0
    var = ''
    
    for unit in list1:
        if not re.match(donepat, unit):
            
            for ch in unit:
                if ord(ch)>127:
                    flag = 1
                    unit = unit.replace(ch, ' '+ch+' ')

            if flag:
                for tok in unit.split():
                    tokens.append(tok)
        
        if not flag:
            tokens.append(unit)

    return tokens

def partialurl(list1):
    tokens = []

    for unit in list1:
        if re.match('^(ht[t]?[p]?).*', unit):
            tokens.append(done+unit)
        else:
            tokens.append(unit)

    return tokens

# @xyz
def at_xyz(list1):
    tokens = []

    for unit in list1:
        if not re.match(donepat, unit):

            m = re.match('(.*)(@\w+)(.*)', unit)
            if m:
                unit = m.group(1)+' '+done+m.group(2)+' '+m.group(3)
                for tok in unit.split():
                    if tok:
                        tokens.append(tok)
                continue
        
        tokens.append(unit)

    return tokens

def figures(list1):
    tokens = []

    for unit in list1:
        if not re.match(donepat, unit):

            toks = ['', '', '']
            t = 0
            pat = [',.', '']
            tern = 0

            for i in range(len(unit)):
                
                if unit[i].isdigit():
                    if t==0:
                        t=1
                    toks[t]+=unit[i]

                elif unit[i] in pat[tern]:
                    if i==0:
                        toks[0]+=unit[i]
                    elif i==len(unit)-1:
                        if t==1:
                            t=2
                        toks[t]+=unit[i]
                    
                    elif unit[i+1].isdigit and unit[i-1].isdigit():
                        if unit[i]=='.':
                            tern = 1
                        toks[t]+=unit[i]
                    else:
                        if t==1:
                            t=2
                        toks[t]+=unit[i]

                else:
                    if t==1:
                        t=2
                    toks[t]+=unit[i]

            for i in range(len(toks)):
                if toks[i]:
                    if i==1:
                        toks[i]=done+toks[i]
                    tokens.append(toks[i])


        else:
            tokens.append(unit)

    return tokens

def specialchar(list1):
    tokens = []
    selected = ["'", '!', '"', '?', ':', '%', '$', '&', '[', ']', '-', '_', '(', ')', ',', '.', '{', '}']
    
    for unit in list1:
        inside = 0

        if not re.match(donepat, unit):
            inside = 1
            present = 0

            for s in selected:
                if s in unit:
                    present = 1
                    one = ''
                    two = ''
                    three = ''
                    s_occurred = 0
                    over = 0
                    for ch in unit:
                        if not ch==s and not s_occurred:
                            one+=ch
                        elif ch==s and not over:
                            s_occurred = 1
                            two+=ch
                        else:
                            over = 1
                            three+=ch
                    unit = one+' '+two+' '+three
                    
            if present:
                for tok in unit.split():
                    tokens.append(tok)
            else:
                tokens.append(unit)

        if not inside:     
            tokens.append(unit)

    return tokens

if __name__ == "__main__":

    fname = raw_input('Input the file name - ')
    fin = open(fname, 'r')
    data = fin.read()
    data = unicode(data, 'utf-8')
	
    
    # code for twitter tokenizer
    list1 = data.split()
    tokens = []

    for unit in list1:
        print unit
        
        # @name:
        if re.match('^@.*:$', unit):
            tokens.append(done+unit.split(':')[0])
            tokens.append(':')
            continue

        # #something 
        if re.match('^#.*', unit):
            tokens.append(done+unit)
            continue

        # complete URLs
        m = re.match('(.*)(https?://t.co/\w+)(.*)', unit)
        if m:
            print "here"
            tokens.append(m.group(1)+' '+done+m.group(2)+' '+m.group(3))
            continue

        # acronyms
        if re.match('^(?:[a-zA-Z]\.[a-zA-z]?)+$', unit):
            tokens.append(done+unit)
            continue

        # titles
        m = re.match('([mrdj]r|as|mrs?|prof)(\.)(.*)', unit, re.I)
        if m:
            one = m.group(1)+m.group(2)
            tokens.append(done+one)
            if m.group(3):
                tokens.append(m.group(3))
            continue
        
        tokens.append(unit)

    # selected apostrophe "'" cases, They'll, brother's etc
    tokens = apos(tokens)
    tokens = asciiemo(tokens) # :)
    tokens = EAemo(tokens)# Extended Ascii
    tokens = partialurl(tokens)
    tokens = at_xyz(tokens) # @something - no ':'
    tokens = figures(tokens) # only 55,000.147
    tokens = specialchar(tokens) 

    LIST = []
    for tok in tokens:
        tok = tok.split(done)
        i = len(tok)-1
        tok[i] = tok[i].encode('utf-8')
        LIST.append(tok[i])

    print "[",
    for l in LIST:
        print "'"+l+"',",
    print "]"

#input file name
