import nltk
import urllib2
import goose
import pandas as pd
qqll='https://en.wikipedia.org/wiki/Vaccine'
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
response = opener.open(qqll)
rt=response
raw_html = response.read()
g = goose.Goose()
a = g.extract(raw_html=raw_html)
my_sent=a.cleaned_text
my_sent=my_sent.encode('utf-8')

parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(my_sent.split()), binary=True)  # POS tagging before chunking!

named_entities = []

for t in parse_tree.subtrees():
    if t.label() == 'NE':
        named_entities.append(t)


z=named_entities
my_count = pd.Series(z).value_counts()
df = pd.DataFrame(my_count)
df.columns = ['Count']
df['entity'] = df.index
za=df.assign(entity=[', '.join([x[0] for x in r]) for r in df.entity])
df['entities'] = pd.DataFrame(za['entity'])
del df['entity']
#df=df.assign(entity=[', '.join([x[0] for x in r]) for r in df.entity])
df.to_csv('entities.csv', index=False)
