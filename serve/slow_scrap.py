from bs4 import BeautifulSoup
import pandas as pd
import requests

context = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.amazon.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


class Scrapper:
    """A class to scrap amazon data"""

    def __init__(self, user_name, category, pages):
        self.df = pd.DataFrame(
            columns=[
                'user_name',
                'brands',
                'categories',
                'names',
                'rating',
                'total_rating',
                'cost_price',
                'selling_price',
                'discount',
                'discount_per', 
                'links'
            ],
        )
        self.df = self.df.rename_axis('ID')
        self.category = category
        self.pages = int(pages)
        self.user_name = user_name
        self.data = dict()
        self.urls = list()

    def url_linker(self, *args):
        for page in range(0, self.pages):
            self.urls.append(f'https://www.amazon.in/s?k={self.category}&page={page+1}&ref=nb_sb_noss')

    def scrapper(self, urls):
        names = list()
        SP = list()
        CP = list()
        rating = list()
        people = list()
        discount = list()
        discount_per = list()
        brand_name = list()
        links = list()
        categories = list()
        user_names = list()
        for url in urls:
            response = requests.get(url, headers=context).content
            soup = BeautifulSoup(response, 'html.parser')
            all_blocks = soup.findAll('div', class_='s-asin')
            all_blocks = all_blocks[:5]
            for product in all_blocks:
                try:
                    name = product.find('h2').get_text()
                    selling_price = product.find(
                        'span', class_='a-price-whole').get_text()
                    cost_price = product.findAll(
                        'span', class_='a-offscreen')[-1].get_text().split('₹')[1]
                    rat = product.find(
                        'span', class_='a-icon-alt').get_text().split()[0]
                    peps = product.find(
                        'span', class_='a-size-base').get_text()
                    # Inside Link
                    link = 'https://www.amazon.in' + \
                        product.find('a', class_='a-link-normal').get('href')
                    new_res = requests.get(link, headers=context).content
                    new_soup = BeautifulSoup(new_res, 'html.parser')
                    disc, disc_per = new_soup.find(
                        'td', 'a-span12 a-color-price a-size-base priceBlockSavingsString').get_text().split()
                    disc = disc.split('₹')[1].replace(',', "")
                    disc_per = disc_per.lstrip('(').rstrip(')')[:2]
                    
                    brand = dict()
                    lst = []
                    for i in new_soup.findAll('tr', 'a-spacing-small'):
                        lst.append([i.get_text().strip()])
                    for i in lst:
                        i = i[0].split('\n')
                        brand[i[0]] = i[-1]

                    brand_ = brand.get('Brand')
                    if not brand_:
                        continue
                    else:
                        brand_name.append(brand_)

                    names.append(name)
                    SP.append(selling_price)
                    CP.append(cost_price)
                    rating.append(rat)
                    people.append(peps)
                    discount.append(disc)
                    discount_per.append(disc_per)
                    links.append(link)
                    categories.append(self.category)
                    user_names.append(self.user_name)

                except Exception as e:
                    print(e)

        self.data['user_name'] = user_names
        self.data['brands'] = brand_name
        self.data['categories'] = categories
        self.data['names'] = names
        self.data['rating'] = rating
        self.data['total_rating'] = people
        self.data['cost_price'] = CP
        self.data['selling_price'] = SP
        self.data['discount'] = discount
        self.data['discount_per'] = discount_per
        self.data['links'] = links
        

    def convert_to_df(self):
        df1 = pd.DataFrame(self.data)
        self.df = pd.concat((self.df, df1))

    def scrap(self):
        self.url_linker(self.category)
        self.scrapper(self.urls)
        self.convert_to_df()
        # self.save_to_csv()
        self.df.discount_per = self.df.discount_per.map(lambda x: x.split('%')[0])
        self.df['cost_price'] = self.df['cost_price'].map(lambda x: x.replace(',', ''))
        self.df['selling_price'] = self.df['selling_price'].map(lambda x: x.replace(',', ''))
        self.df['total_rating'] = self.df['total_rating'].map(lambda x: x.replace(',', ''))
        my_df = self.df
        return my_df

    def save_to_csv(self):
        self.df.to_csv('csv/' + self.user_name + '.csv')
    
if __name__ == '__main__':
    scrapper = Scrapper('jay', 'skincream', 1)
    scrapper.scrap()
   
    