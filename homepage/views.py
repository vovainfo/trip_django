from django.shortcuts import render

def index(request):
    icecreams = ''
    friends = ''
    city_weather = ''
    friend_output = ''
    selected_icecream = ''
    # В переменную conclusion будет сохранен текст рекомендации
    conclusion = ''

    friends += (f'<input type="radio" name="friend"'
                f' required value="Жопа">Жопа1<br>')

    ice_form = (f'<input type="radio" name="icecream" required'
                f' value="Жопа2">Жопа3')

    ice_link = f'<a href="icecream/">Узнать состав</a>'
    icecreams += f'{ice_form} | {ice_link} <br>'


    if request.method == 'POST':
        friend_output = f'Жопа5, тебе прислали Жопа6!'
        city_weather = f'В городе Жопа7 погода: Жопа8'

    context = {
        'icecreams': icecreams,
        'friends': friends,
        'friend_output': friend_output,
        'city_weather': city_weather,
        'conclusion': conclusion,
        # Передайте значение conclusion в шаблон

    }
    return render(request, 'homepage/index.html', context)
