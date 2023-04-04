from flask import Flask,  render_template
from dataset import *

app = Flask(__name__)

Filepath = 'Homo_sapiens.GRCh38.85.gff3.gz'
dataset = GFF3_dataset()
dataset.readDataframe(Filepath)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/operations')
def operation():
    return render_template('operations.html')


@app.route('/op1')
def table1():
    new_dataset = dataset.apply(BasicInfo())
    page = new_dataset.to_html()
    text_file = open("templates/op1.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op1.html')

@app.route('/op2')
def table2():
    new_dataset = dataset.apply(IdList())
    page = new_dataset.to_html()
    text_file = open("templates/op2.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op2.html')

@app.route('/op3')
def table3():
    new_dataset = dataset.apply(UniqueOperations())
    page = new_dataset.to_html()
    text_file = open("templates/op3.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op3.html')

@app.route('/op4')
def table4():
    new_dataset = dataset.apply(NFeatures())
    page = new_dataset.to_html()
    text_file = open("templates/op4.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op4.html')

@app.route('/op5')
def table5():
    new_dataset = dataset.apply(NEntries())
    page = new_dataset.to_html()
    text_file = open("templates/op5.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op5.html')

@app.route('/op6')
def table6():
    new_dataset = dataset.apply(DSChromosomes())
    page = new_dataset.to_html()
    text_file = open("templates/op6.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op6.html')

@app.route('/op7')
def table7():
    new_dataset = dataset.apply(UnassembledSeq())
    page = new_dataset.to_html()
    text_file = open("templates/op7.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op7.html')

@app.route('/op8')
def table8():
    new_dataset = dataset.apply(Filtered())
    page = new_dataset.to_html()
    text_file = open("templates/op8.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op8.html')

@app.route('/op9')
def table9():
    new_dataset = dataset.apply(FilteredEntries())
    page = new_dataset.to_html()
    text_file = open("templates/op9.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op9.html')

@app.route('/op10')
def table01():
    new_dataset = dataset.apply(FilteredGeneNames())
    page = new_dataset.to_html()
    text_file = open("templates/op10.html", "w")
    text_file.write(page)
    text_file.close()
    return render_template('op10.html')



@app.route('/ProjectDocumentation')
def projdoc():
    return render_template('ProjectDocumentation.html')

@app.route('/aboutus')
def abtus():
    return render_template('aboutus.html')

if __name__=='__main__':
    app.run(port=3000, debug=True)
    
