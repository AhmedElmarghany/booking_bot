from booking.booking import Booking
import time

place = input("Where do you want to go?\n")
check_in = input("Check in data:        __'YYYY-MM-DD'__\n")
check_out = input("Check out data:       __'YYYY-MM-DD'__\n")
adults = input("Number of adults:\n")
rooms = input("Number of rooms:\n")


with Booking() as bot:
    bot.land_first_page()
    bot.change_currency("USD")
    bot.select_place_to_go(place)
    bot.select_dates(check_in_date=check_in, 
                     check_out_date=check_out)
    bot.select_adults(int(adults))
    # bot.select_children(count=4, ages=[4,2,8,17])
    # bot.select_rooms(count=int(rooms))
    # bot.travel_for_work(True)
    # bot.show_vacation_rentals(True)
    # time.sleep(1)
    bot.click_search()
    # bot.apply_filterations()
    time.sleep(5)
    while True:
        bot.report_results()
        try:
            bot.next_page()
            time.sleep(5)
        except:
            print("All Pages Done!")
            break
