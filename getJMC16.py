from TIMBER.Tools.Common import GetJMETag, _year_to_thousands_str

#for year in ['16','16APV','17','18']:
year = '16'
print("-------------------------- {} --------------------------".format(year))
print("MC:")
yr = _year_to_thousands_str(year)
print(year)
print(yr)
jestag = GetJMETag("JES",yr,"MC",ULflag=True)
jertag = GetJMETag("JER",yr,"MC",ULflag=True)
print("\tJES: {}".format(jestag))
print("\tJER: {}".format(jertag))
print("Data:")
#for era in ['A','B','C','D','E','F','G','H']:
for era in ['F','G','H']:
    jestag = GetJMETag("JES",year,era,ULflag=True)
    if (jestag):
        print("\t{}{}: {}".format(year, era, jestag))
    else:
        print("\t{}{}: no tarball found".format(year,era))
