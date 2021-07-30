

def load_resource(): 
    # import resources.data as d
    import pkg_resources
    
    files = pkg_resources.resource_listdir('resources', 'data')
    f = files[0]
    
    fl = pkg_resources.resource_stream('resources', 'data\\'+f)
    
    
load_resource()