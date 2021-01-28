# dependencies
from bokeh.models import CustomJS

## calback functions
def checkbox_categorical_filter(src_ans, src_ans_orig): 

    # print(sns_ans)

    return CustomJS(

        args=dict(
            source=src_ans,
            source_ans_orig=src_ans_orig,
            source_nans_orig=src_ans_orig
            ),
            
        code="""
            
            // initialize
            var primary_id = [];
            var x = [];
            var y = [];
            var post_title = [];
            var cluster = [];

            // initialize
            let selected_categories = this.active
            const arr_src = [source_ans_orig, source_nans_orig]

            // iterate through each argument source
            arr_src.forEach(src => {

                console.log(src);

                // iterate through rows of data source and see if each satisfies some constraint
                for (var i = 0; i < src.get_length(); i++){
                    if (selected_categories.includes(parseInt(src.data['cluster'][i]))){
                        primary_id.push(src.data['PrimaryId'][i])
                        x.push(src.data['x'][i])
                        y.push(src.data['y'][i])
                        post_title.push(src.data['post_title'][i])
                        cluster.push(src.data['cluster'][i])
                    }
                }

            })
                
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
            return [source]
    """
    )