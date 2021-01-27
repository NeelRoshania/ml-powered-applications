# dependencies
from bokeh.models import CustomJS

## calback functions
def checkbox_categorical_filter(src_ans): 
 return CustomJS(
    args=dict(source=src_ans), 
    code="""
        
        // initialize
        var primary_id = [];
        var x = [];
        var y = [];
        var post_title = [];
        var cluster = [];
        
        // define active checkboxes
        let selected_categories = this.active
        
        // iterate through rows of data source and see if each satisfies some constraint
        for (var i = 0; i < source.get_length(); i++){
            if (selected_categories.includes(parseInt(source.data['cluster'][i]))){
                primary_id.push(source.data['PrimaryId'][i])
                x.push(source.data['x'][i])
                y.push(source.data['y'][i])
                post_title.push(source.data['post_title'][i])
                cluster.push(source.data['cluster'][i])
            }
        }
        
        console.log(this.active)
        console.log(x.length)

        // update source
        source.data = {
            'PrimaryId': primary_id,
            'post_title': post_title,
            'x': x,
            'y': y,
            'cluster': cluster
        }
        
        // source.change.emit();
        return source
""")