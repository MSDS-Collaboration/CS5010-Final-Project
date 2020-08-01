# Class to hold wine recommendation query functions
import pandas as pd

class WineRecommender:

    # construct the class
    def __init__(self, name, wine_type=None, flavor=None, country=None, price_min=0, price_max=9999999):
        self.name = name
        self.wine_type = wine_type
        self.flavor = flavor
        self.country = country
        self.price_min = price_min
        self.price_max = price_max
        self.wine_list = pd.read_csv('winemag-data-modified-utf8.csv')
        self.results = self.wine_list
        self.price_range_options = [
            {'name': 'Everyday', 'price_min': 1, 'price_max': 50},
            {'name': 'Occasional', 'price_min': 51, 'price_max': 200},
            {'name': 'Premium', 'price_min': 201, 'price_max': 500},
            {'name': 'Luxury', 'price_min': 501, 'price_max': 1000},
            {'name': 'Iconic', 'price_min': 1001, 'price_max': 3300}
        ]

    def __str__(self):
        return "Your Name: " + self.name + "\n" + \
        "Preferred type: " + self.wine_type + "\n" + \
        "Preferred Flavor: " + self.flavor + "\n" + \
        "Country of Origin: " + self.country

    def countries(self):
        string = ''
        options = self.results['country'].unique()
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['country'] == options[i]])} wines)\n"
        return string

    def wine_types(self):
        string = ''
        options = self.results['type'].unique()
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['type'] == options[i]])} wines)\n"
        return string

    def price_ranges(self):
        string = ''
        options = self.price_range_options
        print(options)
        for i in range(len(options)):
            print(options[i])
            print(options[i]['name'])
            string += f"{str(i+1)}: {options[i]['name']} ({len(self.results[(options[i]['price_min'] <= self.results['price']) & (self.results['price'] <= options[i]['price_max'])])} wines)\n"
        return string

    def set_price_range(self, index):
        self.price_min = self.price_range_options[index]['price_min']
        self.price_max = self.price_range_options[index]['price_max']

    def set_recommendations(self):
        results = self.wine_list
        if self.wine_type:
            results = results[self.wine_type == results['type']]
        if self.flavor:
            results = results[self.flavor in results['flavors'].split(',')]
        if self.country:
            results = results[self.country == results['country']]
        results = results[(self.price_min <= results['price']) & (results['price'] <= self.price_max)]
        self.results = results

    def get_recommendations(self):
        if len(self.results) == 0:
            string = 'No Results'
        else:
            # Shuffle randomly and choose 10
            self.results = self.results.sample(frac=1).reset_index(drop=True)
            string = f"\n{self.name}'s Top 10 Wine Recommendations\n----------------------\n\n"
            for index, result in self.results.head(10).iterrows():
                string += f"{result['title']}:\n{result['description']}\n\n"
        return string


def recommend():
    # Get user's name
    name = input('\nSo you are interested in selecting a new wine to try? '
        + 'Let me just ask you a few questions.\n'
        + 'What should I call you during this process?\n')
    recommender = WineRecommender(name)

    # Filter based on wine type/color
    wine_type_id = int(input(f'\nAlright {recommender.name}, we have a several types of wine to choose from. '
        + 'Enter the number for one of these options:\n'  \
        + f'0: No Preference\n{recommender.wine_types()}'))

    if wine_type_id:
        recommender.wine_type = recommender.results['type'].unique()[wine_type_id - 1]

    recommender.set_recommendations()

    if len(recommender.results) < 50:
        return recommender

    # Filter based on origin country
    country_id = int(input('\nIs there a particular country of origin you are interested in? '
        + 'Enter the number for one of these options:\n'  \
        + f'0: No Preference\n{recommender.countries()}'))

    if country_id:
        recommender.country = recommender.results['country'].unique()[country_id - 1]

    recommender.set_recommendations()
    if len(recommender.results) < 50:
        return recommender

    # Filter based on price range
    price_range_id = int(input('\nWhat price range would you like to limit this search to? '
        + 'Enter the number for one of these options:\n'  \
        + f'0: No Limit\n{recommender.price_ranges()}'))

    if price_range_id:
        recommender.set_price_range(price_range_id - 1)

    recommender.set_recommendations()
    if len(recommender.results) < 50:
        return recommender

    # # Filter based on flavors
    # flavor_id = int(input('\nWhich flavor are you in the mood for? '
    #     + 'Enter the number for one of these options:\n'  \
    #     + f'0: No Preference\n{recommender.flavors()}'))

    # if flavor_id:
    #     recommender.flavor = recommender.results['flavors'].unique()[flavor_id - 1]

    return recommender



# Uncomment this to start
recommender = recommend()
print(recommender.get_recommendations())
