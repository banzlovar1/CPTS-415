import pandas as pd

df = pd.read_csv("airports.csv")
rt = pd.read_csv("new_routes.csv")
nf = pd.DataFrame()

src = rt['src'].tolist()
dst = rt['dst'].tolist()
h=[]
for f in src:
    if f not in h:
        h.append(f)
for a in dst:
    if a not in h:
        h.append(a)

nf['id'] = h


# for g in h:
#     a = df.loc[df['id'] == g]
#     newID = a['id'].values[0]
#     print(newID)
#     newName = a['name']
#     newCountry = a['Country']
#     #print(a)
#     #newObject = {'id':newID, 'name':newName, 'country':newCountry}
#     #print(newObject)
#     #nf.append(newObject)

nf.to_csv("new.csv", index=False)
