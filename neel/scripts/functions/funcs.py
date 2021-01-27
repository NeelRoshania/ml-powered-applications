def export_df(df, cols, **kwargs):

    # rename and return a dataframe of those columns
    # choose to export or not
    
    _df = df.loc[:, cols]
    
    # rename dict
    if "rename_dict" in kwargs.keys() :
        _df.rename(columns=kwargs["rename_dict"], inplace=True)
        print('- Columns renamed.')
    
    # export data
    if kwargs["export_loc"]:
        
        # handle data export
        try:
            
            if "export_name" in kwargs.keys():
                _location = kwargs["export_loc"] + "\\{}".format(kwargs["export_name"]) + ".csv"
                _df.to_csv(_location)
                print(f"""- File exported to: {_location}""")
            else:
                _location = kwargs["export_loc"]+"\\adhoc_{}".format(datetime.today().strftime("%m%d%y"))+".csv"
                _df.to_csv(_location)
                print(f"""- File exported to: {_location}""")

        except:
            raise Exception(f"""export_loc must be of type str. Given: {type(kwargs["export_loc"])}""")
    
    print('\n')
    return _df

def test(str_great):
    print(str_great)
    pass

