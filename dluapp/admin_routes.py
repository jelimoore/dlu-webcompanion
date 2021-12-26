@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', name=current_user.name)
