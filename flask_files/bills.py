import pandas as pd
import numpy as np
import flask
from flask import render_template, request, Flask
from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import transform
from bokeh.embed import components
import pdb
import pickle

topics_df = pd.read_csv('bill_details.csv',index_col=[0])
topics_df.date = pd.to_datetime(topics_df.date, format='%Y-%m-%d')


app = Flask(__name__)
app.debug=True

@app.route('/')
def intro():
    return render_template('circling.html')

@app.route('/data')
def data():
    return render_template('bill_sim.html')

@app.route('/nlp')
def nlp():
    return render_template('nlp.html')

@app.route('/nlp2')
def nlp2():
    return render_template('nlp2.html')

@app.route('/pie')
def pies():
    return render_template('topics.html')

@app.route('/heat', methods=["GET", 'post'])
def heat():
    topics = topics_df.topic.unique()
    checked = request.form.getlist('checkbox')
    type = request.form.get('law')

    if type == 'Became Law':
        df = topics_df[topics_df.track == 'Became Law']
    else:
        df = topics_df
    if checked:
        mask = eval('|'.join([f"(df.topic=='{i}')" for i in checked]))
        time_df = df[mask].groupby([df['date'].dt.strftime('%Y-%m'), 'topic']).size().unstack(fill_value=0)
    else:
        time_df = df.groupby([df['date'].dt.strftime('%Y-%m'), 'topic']).size().unstack(fill_value=0)
    time_df.index.name = 'Months'
    time_df.columns.name = 'Topics'

    time_df = time_df.stack().rename("value").reset_index()

    colors = ['#000000', '#330000', '#6F0606', '#C32B2B', '#F31E1E', '#FF9406', '#FC9207', '#F5C88D', '#FFFF01',
              '#FAF44B', '#F0F974', '#DCDCC8', '#F7F7EB']
    mapper = LinearColorMapper(
        palette=colors, low=time_df.value.min(), high=time_df.value.max())

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    p = figure(
        plot_width=1000,
        plot_height=500,
        x_range=list(time_df.Months.drop_duplicates()),
        y_range=list(time_df.Topics.drop_duplicates()),
        tools=TOOLS, toolbar_location='below',
        tooltips=[('Month', '@Months'), ('Bills', '@value')],
        x_axis_location="below")
    # Create rectangle for heatmap
    p.rect(
        x="Months",
        y="Topics",
        width=1,
        height=1,
        source=ColumnDataSource(time_df),
        line_color=None,
        fill_color=transform('value', mapper))
    # Add legend
    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        ticker=BasicTicker(desired_num_ticks=len(colors)))
    p.background_fill_color = '#DEDDDA'
    p.border_fill_color = '#DEDDDA'
    p.add_layout(color_bar, 'right')
    p.xaxis.major_label_orientation = 0.8
    javascript, div = components(p)
    
    
    return render_template('heatmap.html', topics=topics, javascript=javascript, div=div)

@app.route('/future')
def future():
    return render_template('further.html')

@app.route('/appendix')
def appendix():
    topics = topics_df.topic.unique()
    ind_topic = []
    for i, topic in enumerate(topics):
        ind_topic.append((i, topic))
    return render_template('appendix.html', topics=ind_topic)

@app.route('/end')
def end():
    return render_template('end.html')

@app.route('/appendix1')
def appendix1():
    return render_template('scatter_texts/tax.html')
@app.route('/appendix2')
def appendix2():
    return render_template('scatter_texts/election.html')
@app.route('/appendix3')
def appendix3():
    return render_template('scatter_texts/budget.html')
@app.route('/appendix4')
def appendix4():
    return render_template('scatter_texts/infrastructure.html')
@app.route('/appendix5')
def appendix5():
    return render_template('scatter_texts/regulations.html')
@app.route('/appendix6')
def appendix6():
    return render_template('scatter_texts/health_care.html')
@app.route('/appendix7')
def appendix7():
    return render_template('scatter_texts/labor.html')
@app.route('/appendix8')
def appendix8():
    return render_template('scatter_texts/nature.html')
@app.route('/appendix9')
def appendix9():
    return render_template('scatter_texts/business.html')
@app.route('/appendix10')
def appendix10():
    return render_template('scatter_texts/trump.html')
@app.route('/appendix11')
def appendix11():
    return render_template('scatter_texts/immigration.html')
@app.route('/appendix12')
def appendix12():
    return render_template('scatter_texts/medicine.html')
@app.route('/appendix13')
def appendix13():
    return render_template('scatter_texts/police.html')
@app.route('/appendix14')
def appendix14():
    return render_template('scatter_texts/military.html')
@app.route('/appendix15')
def appendix15():
    return render_template('scatter_texts/education.html')

if __name__ == '__main__':
    app.run()