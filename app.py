from flask import Flask, render_template, abort

import data

app = Flask(__name__)


@app.route('/')
def render_main():
    tours = data.tours
    tours = {key:tours[key] for key in range(1, 7)}
    description = data.description
    subtitle = data.subtitle
    departures = data.departures
    title = data.title

    return render_template(
        'index.html',
        tours=tours,
        description=description,
        subtitle=subtitle,
        departures=departures,
        title=title,
    )


@app.route('/departures/<departure>/')
def render_departure(departure):
    departures = data.departures
    departure_full_name = data.departures.get(departure)
    title = data.title
    if departure is None:
        abort(404)
    
    filtered_tours = {}
    min_price = float('inf')
    max_price = float('-inf')
    min_nights = float('inf')
    max_nights = float('-inf')

    for key, tour in data.tours.items():
        if tour['departure'] != departure:
            continue
        filtered_tours[key] = tour
        
        if tour['price'] < min_price:
            min_price = tour['price']
        if tour['price'] > max_price:
            max_price = tour['price']
        if tour['nights'] < min_nights:
            min_nights = tour['nights']
        if tour['nights'] > max_nights:
            max_nights = tour['nights']

    return render_template(
        'departure.html',
        departure_full_name=departure_full_name,
        departures=departures,
        tours=filtered_tours,
        min_price=min_price,
        max_price=max_price,
        min_nights=min_nights,
        max_nights=max_nights,
        title=title,
    )


@app.route('/tours/<int:id_>/')
def render_tour(id_):
    current_tour = data.tours.get(id_)
    if current_tour is None:
        abort(404)
    
    departure = data.departures[current_tour['departure']]
    return render_template(
        'tour.html',
        tour=current_tour,
        departure=departure,
        title=data.title,
        departures=data.departures,
    )


if __name__ == '__main__':
    app.run()