from django.shortcuts import render
import datetime as dt
from trip.trip_api import get_route_list
from trip.trip_api import pretty_datetime

import json


def index(request):

    context = {
        'base_airport_value': f'value=UHWW',
        'minimum_departure_date_value': f'value=2021-10-01T00:00',
        'maximum_return_date_value': f'value=2021-10-02T00:00',
        'minimum_stay_value': f'value=5'
    }
    if request.method == 'POST':
        base_airport = request.POST['base_airport']
        minimum_departure_date = request.POST['minimum_departure_date']
        maximum_return_date = request.POST['maximum_return_date']
        minimum_stay = request.POST['minimum_stay']

        min_date = dt.datetime.strptime(minimum_departure_date, '%Y-%m-%dT%H:%M')
        max_date = dt.datetime.strptime(maximum_return_date, '%Y-%m-%dT%H:%M')
        delta_date = max_date-min_date
        if delta_date > dt.timedelta(days=10):
            max_date = min_date + dt.timedelta(days=10)
            maximum_return_date = max_date.strftime('%Y-%m-%dT%H:%M')

        print(delta_date)

        # print(f'{base_airport=}')
        # print(f'{minimum_departure_date=}')
        # print(f'{maximum_return_date=}')
        # print(f'{minimum_stay=}')

        json_res = get_route_list(base_airport, minimum_departure_date, maximum_return_date, minimum_stay)
        res_data = json.loads(json_res)
        # print(res_data)

        result_flight = ""

        for idx_airport, one_airport in enumerate(res_data, 1):
            # print(one_airport)
            # print(one_airport.keys())
            # print(one_airport['airport'])
            airport_name = one_airport['airport']['name']
            flight_list_outbound_count = len(one_airport['flight_list_outbound'])
            flight_list_inbound_count = len(one_airport['flight_list_inbound'])
            maximum_stay = one_airport['maximum_stay']

            head_str = f'<strong>{airport_name}</strong>. Максимальное пребывание: {maximum_stay} часов. Рейсов {flight_list_outbound_count}/{flight_list_inbound_count}'

            accordion_header = (
                f'<div class="accordion-item">\n'    
                    f'<h2 class="accordion-header" id="heading{idx_airport}">\n'
                        f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"\n'
                                f'data-bs-target="#collapse{idx_airport}"\n'
                                f'aria-expanded="false" aria-controls="collapse{idx_airport}">\n'
                            f'{head_str}\n'
                        f'</button>\n'
                    f'</h2>\n'
            )
            accordion_body_head = (
                f'<div id="collapse{idx_airport}" class="accordion-collapse collapse" aria-labelledby="heading{idx_airport}"\n'
                     f'data-bs-parent="#accordionExample">\n'
            )

            accordion_body_outbound_head = (
                f'<div class="accordion-body row gx-5 accordition-body-my">\n'
                    f'<div class="col">\n'
                        f'<div class="row">\n'
                            f'<div class="col-12 text-center"><strong>Вылет в {airport_name}</strong></div>\n'
                        f'</div>\n'
                        f'<div class="row">\n'
                            f'<table class="table">\n'
                                f'<thead>\n'
                                f'<tr>\n'
                                    f'<th scope="col">#</th>\n'
                                    f'<th scope="col">Отправление</th>\n'
                                    f'<th scope="col">Прибытие</th>\n'
                                    f'<th scope="col">Рейс</th>\n'
                                    f'<th scope="col">АК</th>\n'
                                    f'<th scope="col">Тип ВС</th>\n'
                                f'</tr>\n'
                                f'</thead>\n'
                                f'<tbody>\n'
            )
            accordion_body_outbound = ''
            for idx_flight, one_flight  in enumerate(one_airport['flight_list_outbound'], 1):
                accordion_body_outbound += (
                                f'<tr>\n'
                                    f'<th scope="row">{idx_flight}</th>\n'
                                    f'<td>{pretty_datetime(one_flight["time_departure"])}</td>\n'
                                    f'<td>{pretty_datetime(one_flight["time_arrival"])}</td>\n'
                                    f'<td>{one_flight["flight_number"]}</td>\n'
                                    f'<td>{one_flight["airline_name"]}</td>\n'
                                    f'<td>{one_flight["aircraft_model"]}</td>\n'
                                f'</tr>\n'
                )
            accordion_body_outbound_tail = (
                                f'</tbody>\n'
                            f'</table>\n'
                        f'</div>\n'
                    f'</div>\n'
            )

            accordion_body_inbound_head = (
                    f'<div class="col">\n'
                        f'<div class="row">\n'
                            f'<div class="col-12 text-center"><strong>Возвращение из {airport_name}</strong></div>\n'
                        f'</div>\n'
                        f'<div class="row">\n'
                            f'<table class="table">\n'
                                f'<thead>\n'
                                f'<tr>\n'
                                    f'<th scope="col">#</th>\n'
                                    f'<th scope="col">Отправление</th>\n'
                                    f'<th scope="col">Прибытие</th>\n'
                                    f'<th scope="col">Рейс</th>\n'
                                    f'<th scope="col">АК</th>\n'
                                    f'<th scope="col">Тип ВС</th>\n'
                                f'</tr>\n'
                                f'</thead>\n'
                                f'<tbody>\n'
            )

            accordion_body_inbound = ''
            for idx_flight, one_flight in enumerate(one_airport['flight_list_inbound'], 1):
                accordion_body_inbound += (
                                f'<tr>\n'
                                    f'<th scope="row">{idx_flight}</th>\n'
                                    f'<td>{pretty_datetime(one_flight["time_departure"])}</td>\n'
                                    f'<td>{pretty_datetime(one_flight["time_arrival"])}</td>\n'
                                    f'<td>{one_flight["flight_number"]}</td>\n'
                                    f'<td>{one_flight["airline_name"]}</td>\n'
                                    f'<td>{one_flight["aircraft_model"]}</td>\n'
                                f'</tr>\n'
                )
            accordion_body_inbound_tail = (
                                f'</tbody>\n'
                            f'</table>\n'
                        f'</div>\n'
                    f'</div>\n'
            )
            accordion_body_tail = (
                            f'</div>\n'
                        f'</div>\n'
                    f'</div>\n'
            )

            result_one_flight = (
                accordion_header +
                accordion_body_head +
                accordion_body_outbound_head +
                accordion_body_outbound +
                accordion_body_outbound_tail +
                accordion_body_inbound_head +
                accordion_body_inbound +
                accordion_body_inbound_tail +
                accordion_body_tail
            )
            result_flight += result_one_flight

        context = {
            'base_airport_value': f'value={base_airport}',
            'minimum_departure_date_value': f'value={minimum_departure_date}',
            'maximum_return_date_value': f'value={maximum_return_date}',
            'minimum_stay_value': f'value={minimum_stay}',
            'result_flight': result_flight
        }

    return render(request, 'homepage/index.html', context)
