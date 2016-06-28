from django.template import Library


register = Library()

@register.filter
def sum_rating(item_list):
	sum_rating = 0
	for i in item_list:
		if i.rating:
			sum_rating += i.rating
	return sum_rating


@register.filter
def percent_rating(item_list):
	sum_rating = 0
	len_rating = 0
	for i in item_list:
		if i.rating:
			sum_rating += i.rating
			len_rating += 1
	try:
		percent_rating = str(float(sum_rating) / len_rating)
	except ZeroDivisionError:
		percent_rating = None
	return percent_rating