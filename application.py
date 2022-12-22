from flask import Flask, render_template, request

import anime_images
import anime_list
import image_maker

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    image_maker.delete_images()
    if request.form.get("home") == "home":
        image_maker.delete_images()
        return render_template('index.html')
    return render_template('index.html')


@app.route('/animelist', methods=["POST"])
def animelist():
    if request.form.get("go") == "go":
        search = request.form.get("search")
        global label_search
        label_search = f"List of animes from {search}: "
        anime_list.user = search

        anime_list.init()
        anime_list.main()

        with open("./static/list_of_animes.txt") as file:
            global content
            content = file.read().splitlines()

        return render_template('searchlist.html', mal_username=label_search, anime_list=' \n'.join(content))


@app.route('/animeimages', methods=["POST"])
def animeimages():
    if request.form.get("button-anime-images") == "button-anime-images":
        anime_images.init()
        anime_images.main()
        global valid_files
        valid_files = f"Number of images downloaded: {anime_images.valid_files()}"
        return render_template("searchimages.html", valid_files=valid_files, mal_username=label_search,
                               anime_list=' \n'.join(content))


@app.route("/make_grid", methods=["POST"])
def make_grid():
    if request.form.get("button-grid") == "button-grid" or request.form.get("button-regrid") == "button-regrid":
        row = request.form.get("row")
        col = request.form.get("col")
        grid_size = request.form.get("grid")
        padding = request.form.get("padding")
        padding_color = request.form.get("padding-color")
        padding_cells = request.form.get("padding-cells")
        padding_cells_color = request.form.get("padding-cells-color")

        print(row,col,grid_size,padding, padding_color, padding_cells, padding_cells_color)

        image_maker.GRID_SIZE = int(grid_size)
        image_maker.ROW = int(row)
        image_maker.COLUMN = int(col)
        image_maker.PADDING = int(padding)
        image_maker.PADDING_COLOR = padding_color
        image_maker.PADDING_CELLS = int(padding_cells)
        image_maker.PADDING_CELL_COLOR = padding_cells_color

        image_maker.init()
        image_maker.main()

        return render_template("grid.html", grid_image="./static/image.jpg",valid_files=valid_files, mal_username=label_search,
                               anime_list=' \n'.join(content))


if __name__ == '__main__':
    app.run(debug=True)
